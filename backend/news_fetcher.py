import requests
from backend.db import get_db_connection
from backend.summarizer import summarize_text

API_KEY = "pub_1ebf1665807446c9b4f8d75efaa9ea0d"


def infer_category(text):
    text = text.lower()
    if any(word in text for word in ["election", "government", "president", "policy"]):
        return "Politics"
    elif any(word in text for word in ["tech", "ai", "startup", "software", "app", "hardware"]):
        return "Technology"
    elif any(word in text for word in ["stock", "crypto", "market", "invest"]):
        return "Finance"
    elif any(word in text for word in ["match", "goal", "team", "tournament"]):
        return "Sports"
    elif any(word in text for word in ["health", "covid", "cancer", "vaccine"]):
        return "Health"
    else:
        return "General"
    

def fetch_and_store_news():
    url = f"https://newsdata.io/api/1/news?apikey=pub_1ebf1665807446c9b4f8d75efaa9ea0d&country=in&language=en"
    try:
        res = requests.get(url)
        data = res.json()
        articles = data.get("results", [])
        if not articles:
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM news")

        for item in articles:
            if not item.get("title") or not item.get("description") or not item.get("pubDate"):
                continue

            title = item["title"]
            description = item["description"]
            summary = summarize_text(description)
            url = item.get("link", "")
            thumbnail = item.get("image_url", "")
            timestamp = item["pubDate"]
            category = infer_category(description)

            cursor.execute("""
                INSERT INTO news (title, description, summary, url, thumbnail, timestamp, category)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (title, description, summary, url, thumbnail, timestamp, category))

        conn.commit()
        conn.close()
    except Exception as e:
        print("Error fetching/storing news:", e)