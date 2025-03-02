import os
from flask import Flask, redirect, url_for
from flask_migrate import Migrate
from extensions import db
from config.config import config
from config.logging import init_logging

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
    from routes.website import bp as website_bp
    from routes.cookie import bp as cookie_bp
    from routes.spider import bp as spider_bp

    app.register_blueprint(website_bp)
    app.register_blueprint(cookie_bp)
    app.register_blueprint(spider_bp)

    # 添加根路由
    @app.route('/')
    def index():
        return redirect(url_for('website.website_list'))

    return app

app = create_app(os.getenv('FLASK_ENV', 'default'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # 导入并初始化定时任务
        from tasks import init_scheduler
        scheduler = init_scheduler()
        
        try:
            app.run(host='0.0.0.0', debug=True)
        finally:
            # 确保在应用退出时关闭定时任务
            scheduler.shutdown() 