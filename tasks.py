from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from extensions import db
from models import Cookie
import logging

def reset_daily_usage():
    """重置所有Cookie的每日使用计数"""
    try:
        Cookie.query.update({Cookie.daily_used: 0})
        db.session.commit()
        logging.info("Successfully reset daily usage count for all cookies")
    except Exception as e:
        logging.error(f"Error resetting daily usage count: {str(e)}")
        db.session.rollback()

def init_scheduler():
    """初始化定时任务调度器"""
    scheduler = BackgroundScheduler()
    
    # 每天凌晨00:00重置使用计数
    scheduler.add_job(
        reset_daily_usage,
        trigger=CronTrigger(hour=0, minute=0),
        id='reset_daily_usage',
        name='Reset daily usage count for cookies',
        replace_existing=True
    )
    
    scheduler.start()
    logging.info("Scheduler started")
    
    return scheduler 