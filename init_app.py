from flask import Flask
from extensions import db
from models.user import User
from models.website import Website
from models.cookie import Cookie
import os

def init_db(app):
    """初始化数据库"""
    with app.app_context():
        # 确保instance目录存在
        if not os.path.exists(app.instance_path):
            os.makedirs(app.instance_path)
            
        # 创建所有表
        db.create_all()
        
        # 检查是否存在管理员账号
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            # 创建默认管理员账号
            admin = User(
                username='admin',
                is_admin=True,
                is_active=True
            )
            admin.set_password('admin123')  # 设置默认密码
            db.session.add(admin)
            db.session.commit()
            print('Created default admin account:')
            print('Username: admin')
            print('Password: admin123')
        else:
            print('Admin account already exists')

def create_app():
    """创建Flask应用"""
    app = Flask(__name__)
    
    # 确保instance目录存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # 配置数据库
    db_path = os.path.join(app.instance_path, 'app.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev'
    
    # 初始化扩展
    db.init_app(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    init_db(app)
    print('Initialization completed successfully!') 