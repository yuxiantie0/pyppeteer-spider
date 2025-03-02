from extensions import db
from datetime import datetime

# 网站管理模型
class Website(db.Model):
    """网站模型
    用于管理不同网站的基本信息和配置
    """
    __tablename__ = 'website'
    __table_args__ = {
        'comment': '网站信息表'
    }

    # 基本信息
    id = db.Column(db.Integer, primary_key=True, comment='主键ID')  # 主键ID
    name = db.Column(db.String(100), nullable=False, comment='网站名称')  # 网站名称
    identifier = db.Column(db.String(50), unique=True, nullable=False, comment='网站唯一标识符，用于API调用')  # 网站唯一标识符，用于API调用
    homepage = db.Column(db.String(200), nullable=False, comment='网站首页URL')  # 网站首页URL

    # 关联字段
    cookies = db.relationship('Cookie', backref='website', lazy=True, cascade='all, delete-orphan')  # 关联的Cookie列表

    # 时间信息
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')  # 创建时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')  # 更新时间

    def __repr__(self):
        """模型的字符串表示"""
        return f'<Website {self.name}>'

    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'name': self.name,
            'identifier': self.identifier,
            'homepage': self.homepage,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }