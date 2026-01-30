def summarize_news(articles: list):
    if not articles:
        return "No news available."

    # simple extractive summary (v1)
    titles = [a["title"] for a in articles[:5]]

    summary = "Here are the main updates today:\n"
    for i, t in enumerate(titles, 1):
        summary += f"{i}. {t}\n"

    return summary
