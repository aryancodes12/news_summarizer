from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.db import init_db, get_db_connection
from backend.scheduler import start_scheduler
from backend.news_fetcher import fetch_and_store_news

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()
    fetch_and_store_news()
    start_scheduler()

@app.get("/news")
def get_news():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT title, summary, url, thumbnail, timestamp, category 
    FROM news 
    ORDER BY timestamp DESC LIMIT 80
""")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "title": row[0],
            "summary": row[1],
            "url": row[2],
            "thumbnail": row[3],
            "timestamp": row[4],
            "category": row[5]
        }
        for row in rows 
    ]