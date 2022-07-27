from tech_news.database import find_news

# Requisito 10


def top_5_news():

    return [
        (news["title"], news["url"])
        for news in sorted(
            find_news(), key=lambda x: x["comments_count"], reverse=True
        )[:5]
    ]


# Requisito 11
def top_5_categories():
    """Seu código deve vir aqui"""
