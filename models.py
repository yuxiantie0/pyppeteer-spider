from datetime import datetime
from extensions import db

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