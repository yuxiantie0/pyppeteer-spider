from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    """用户模型
    用于管理系统用户账号信息和权限
    """
    __tablename__ = 'user'
    __table_args__ = {
        'comment': '用户信息表'
    }
    
    # 基本信息
    id = db.Column(db.Integer, primary_key=True, comment='主键ID')
    username = db.Column(db.String(80), unique=True, nullable=False, comment='用户名')
    password_hash = db.Column(db.String(128), comment='密码哈希值')
    email = db.Column(db.String(120), unique=True, comment='电子邮箱')
    
    # 权限信息
    is_admin = db.Column(db.Boolean, default=False, comment='是否为管理员')
    is_active = db.Column(db.Boolean, default=True, comment='账号是否激活')
    
    # 时间信息
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    last_login_at = db.Column(db.DateTime, comment='最后登录时间')
    
    def set_password(self, password):
        """设置用户密码"""
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """验证用户密码"""
        return check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        """更新最后登录时间"""
        self.last_login_at = datetime.utcnow()
        
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'is_active': self.is_active,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'last_login_at': self.last_login_at.strftime('%Y-%m-%d %H:%M:%S') if self.last_login_at else None
        }
    
    @staticmethod
    def get_admin():
        """获取管理员用户"""
        return User.query.filter_by(is_admin=True).first()
    
    @staticmethod
    def create_admin(username, password, email=None):
        """创建管理员账号"""
        admin = User(username=username, is_admin=True, email=email)
        admin.set_password(password)
        return admin
        
    def __repr__(self):
        """模型的字符串表示"""
        return f'<User {self.username}>' 