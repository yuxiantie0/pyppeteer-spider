from datetime import datetime
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

# 网站管理模型
class Website(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    identifier = db.Column(db.String(50), unique=True, nullable=False)  # 英文标识符
    homepage = db.Column(db.String(200), nullable=False)  # 首页
    cookies = db.relationship('Cookie', backref='website', lazy=True)

    def __repr__(self):
        return f'<Website {self.name}>'

# Cookie管理模型
class Cookie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website_id = db.Column(db.Integer, db.ForeignKey('website.id'), nullable=False)
    account = db.Column(db.String(100), nullable=False)
    cookie_value = db.Column(db.Text, nullable=False)
    is_valid = db.Column(db.Boolean, default=True)
    note = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    total_used = db.Column(db.Integer, default=0)
    daily_used = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Cookie {self.account}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def init_admin():
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', is_admin=True)
            admin.set_password('admin123456')
            db.session.add(admin)
            db.session.commit() 