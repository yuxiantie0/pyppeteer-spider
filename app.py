import os
from flask import Flask, redirect, url_for
from flask_migrate import Migrate
from extensions import db
from config.config import config
from config.logging import init_logging
from routes.auth import bp as auth_bp, login_required
from models import User
from routes import auth, website, cookie, spider
from init_app import init_db
from tasks import init_scheduler

def create_app(config_name='default'):
    """创建Flask应用"""
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(config[config_name])

    # 确保instance目录存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化扩展
    db.init_app(app)
    Migrate(app, db)

    # 初始化日志系统
    init_logging(app)

    # 注册蓝图
    app.register_blueprint(auth_bp)
    app.register_blueprint(website.bp)
    app.register_blueprint(cookie.bp)
    app.register_blueprint(spider.bp)

    # 确保数据库和管理员账号存在
    with app.app_context():
        db.create_all()
        init_db(app)

    # 初始化定时任务
    scheduler = init_scheduler()
    app.scheduler = scheduler  # 将scheduler保存到app实例中

    # 添加根路由
    @app.route('/')
    @login_required
    def index():
        return redirect(url_for('website.website_list'))

    return app

app = create_app(os.getenv('FLASK_ENV', 'default'))

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', debug=True)
    finally:
        # 确保在应用退出时关闭定时任务
        if hasattr(app, 'scheduler'):
            app.scheduler.shutdown() 