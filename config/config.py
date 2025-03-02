import os
import secrets

class Config:
    """基础配置"""
    # 应用配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    
    # 数据库配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Cookie配置
    COOKIE_DAILY_LIMIT = 1000
    
    # 浏览器配置
    BROWSER_CONFIG = {
        'headless': True,
        'window_size': {'width': 1920, 'height': 1080},
        'disable_infobars': True
    }

    @staticmethod
    def get_database_path(filename):
        basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        return os.path.join(basedir, 'instance', filename)

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'instance', 'cookie_pool.db')
    
    # 日志配置
    LOG_LEVEL = 'DEBUG'

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'instance', 'test.db')
    
    # 禁用CSRF保护
    WTF_CSRF_ENABLED = False
    
    # 日志配置
    LOG_LEVEL = 'INFO'

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'instance', 'cookie_pool.db')
    
    # 安全配置
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    
    # 日志配置
    LOG_LEVEL = 'WARNING'

# 配置映射
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 