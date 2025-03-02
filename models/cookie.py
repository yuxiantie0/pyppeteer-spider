from extensions import db
from datetime import datetime
import json

# Cookie管理模型
class Cookie(db.Model):
    """Cookie模型
    用于管理和追踪网站的Cookie信息及其使用情况
    """
    __tablename__ = 'cookie'
    __table_args__ = {
        'comment': 'Cookie信息表'
    }

    # 基本信息
    id = db.Column(db.Integer, primary_key=True, comment='主键ID')
    website_id = db.Column(db.Integer, db.ForeignKey('website.id'), nullable=False, comment='关联的网站ID')
    account = db.Column(db.String(100), nullable=False, comment='账号信息')
    cookie_value = db.Column(db.Text, nullable=False, comment='Cookie值（JSON格式）')
    note = db.Column(db.String(200), comment='备注信息')

    # 状态信息
    is_valid = db.Column(db.Boolean, default=True, comment='Cookie是否有效')
    total_used = db.Column(db.Integer, default=0, comment='总使用次数')
    daily_used = db.Column(db.Integer, default=0, comment='当日使用次数')

    # 时间信息
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    last_used_at = db.Column(db.DateTime, comment='最后使用时间')

    def __repr__(self):
        """模型的字符串表示"""
        return f'<Cookie {self.account}>'

    def use(self):
        """使用Cookie并更新相关计数"""
        self.total_used += 1
        self.daily_used += 1
        self.last_used_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def reset_daily_usage(self):
        """重置每日使用计数"""
        self.daily_used = 0
        self.updated_at = datetime.utcnow()

    @property
    def cookie_dict(self):
        """获取Cookie的字典格式"""
        try:
            return json.loads(self.cookie_value)
        except json.JSONDecodeError:
            return {}

    @cookie_dict.setter
    def cookie_dict(self, value):
        """设置Cookie的字典格式"""
        self.cookie_value = json.dumps(value)

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'website_id': self.website_id,
            'account': self.account,
            'is_valid': self.is_valid,
            'note': self.note,
            'total_used': self.total_used,
            'daily_used': self.daily_used,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'last_used_at': self.last_used_at.strftime('%Y-%m-%d %H:%M:%S') if self.last_used_at else None
        } 