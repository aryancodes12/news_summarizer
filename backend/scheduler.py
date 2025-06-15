from apscheduler.schedulers.background import BackgroundScheduler
from backend.news_fetcher import fetch_and_store_news

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_store_news, 'interval', minutes=10)
    scheduler.start()