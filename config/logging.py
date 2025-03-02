import os
import logging
from logging.handlers import RotatingFileHandler

def init_logging(app):
    """初始化日志配置"""
    # 确保日志目录存在
    log_dir = os.path.join(app.instance_path, 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # 设置日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 文件处理器 - 应用日志
    app_log_file = os.path.join(log_dir, 'app.log')
    file_handler = RotatingFileHandler(
        app_log_file,
        maxBytes=1024 * 1024,  # 1MB
        backupCount=10
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # 文件处理器 - 错误日志
    error_log_file = os.path.join(log_dir, 'error.log')
    error_file_handler = RotatingFileHandler(
        error_log_file,
        maxBytes=1024 * 1024,  # 1MB
        backupCount=10
    )
    error_file_handler.setFormatter(formatter)
    error_file_handler.setLevel(logging.ERROR)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(error_file_handler)
    root_logger.addHandler(console_handler)

    # 配置Flask应用日志
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(error_file_handler)

    # 配置Werkzeug日志（Flask的内置服务器）
    logging.getLogger('werkzeug').setLevel(logging.INFO)
    logging.getLogger('werkzeug').addHandler(file_handler)

    # 配置SQLAlchemy日志
    logging.getLogger('sqlalchemy').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy').addHandler(error_file_handler)

    # 配置APScheduler日志
    logging.getLogger('apscheduler').setLevel(logging.INFO)
    logging.getLogger('apscheduler').addHandler(file_handler)

    app.logger.info('Logging system initialized') 