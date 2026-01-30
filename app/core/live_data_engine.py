import feedparser

def fetch_news():
    feed_url = "https://news.google.com/rss"
    feed = feedparser.parse(feed_url)

    articles = []

    for entry in feed.entries[:10]:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "summary": entry.summary if "summary" in entry else "",
            "source": "google_news"
        })

    return articles
