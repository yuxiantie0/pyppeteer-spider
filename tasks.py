from apscheduler.schedulers.background import BackgroundScheduler
from models.cookie import Cookie
from extensions import db
import logging

def reset_daily_usage():
    """重置所有Cookie的每日使用次数"""
    try:
        Cookie.query.update({Cookie.daily_used: 0})
        db.session.commit()
        logging.info("Successfully reset daily usage count for all cookies")
    except Exception as e:
        logging.error(f"Error resetting daily usage count: {str(e)}")
        db.session.rollback()
        raise e

def init_scheduler():
    """初始化定时任务调度器"""
    scheduler = BackgroundScheduler()
    
    # 每天凌晨重置使用次数
    scheduler.add_job(
        reset_daily_usage,
        'cron',
        hour=0,
        minute=0,
        id='Reset daily usage count for cookies'
    )
    
    scheduler.start()
    logging.info("Scheduler started")
    
    return scheduler 