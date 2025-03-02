import os
import logging
from logging.handlers import RotatingFileHandler

def init_logging(app):
    """初始化日志系统"""
    if not os.path.exists('instance/logs'):
        os.makedirs('instance/logs')

    # 设置日志格式
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )

    # 应用日志
    app_handler = RotatingFileHandler(
        'instance/logs/app.log',
        maxBytes=1024 * 1024,  # 1MB
        backupCount=10
    )
    app_handler.setFormatter(formatter)
    app_handler.setLevel(logging.INFO)

    # 错误日志
    error_handler = RotatingFileHandler(
        'instance/logs/error.log',
        maxBytes=1024 * 1024,  # 1MB
        backupCount=10
    )
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)

    # 添加处理器到应用
    app.logger.addHandler(app_handler)
    app.logger.addHandler(error_handler)
    app.logger.setLevel(logging.INFO)

    # 记录初始化完成
    app.logger.info('Logging system initialized')

    # 配置Flask应用日志
    app.logger.addHandler(app_handler)
    app.logger.addHandler(error_handler)

    # 配置Werkzeug日志（Flask的内置服务器）
    logging.getLogger('werkzeug').setLevel(logging.INFO)
    logging.getLogger('werkzeug').addHandler(app_handler)

    # 配置SQLAlchemy日志
    logging.getLogger('sqlalchemy').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy').addHandler(error_handler)

    # 配置APScheduler日志
    logging.getLogger('apscheduler').setLevel(logging.INFO)
    logging.getLogger('apscheduler').addHandler(app_handler) 