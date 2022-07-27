import time
import requests
import parsel
from tech_news.database import create_news

# Requisito 1


def fetch(url):
    try:
        time.sleep(1)
        request = requests.get(url, timeout=3)
        if request.status_code == 200:
            return request.text
        else:
            return None
    except requests.Timeout:
        return None


# Requisito 2
def scrape_novidades(html_content):
    selector = parsel.Selector(text=html_content)

    return selector.css("a.cs-overlay-link::attr(href)").getall()


# Requisito 3
def scrape_next_page_link(html_content):
    selector = parsel.Selector(text=html_content)

    return selector.css("a.next::attr(href)").get()


# Requisito 4
def scrape_noticia(html_content):
    selector = parsel.Selector(text=html_content)

    return {
        "url": selector.css("link[rel=canonical]::attr(href)").get(),
        "title": selector.css("h1.entry-title::text").get().strip(),
        "timestamp": selector.css(".meta-date::text").get(),
        "writer": selector.css("span.author > a ::text").get(),
        "comments_count": len(selector.css(".comments-list li").getall()),
        "summary": "".join(
            selector.css(
                "div.entry-content > p:nth-of-type(1) *::text"
            ).getall()
        ).strip(),
        "tags": selector.css("section.post-tags ul li a::text").getall(),
        "category": selector.css("span.label::text").get(),
    }


# Requisito 5
def get_tech_news(amount):
    html_content = fetch("https://blog.betrybe.com/")
    results = []

    while True:
        urls = scrape_novidades(html_content)

        for url in urls:
            html = fetch(url)
            current_news = scrape_noticia(html)

            if len(results) == amount:
                create_news(results)
                return results

            results.append(current_news)

        base_url = scrape_next_page_link(html_content)
        html_content = fetch(base_url)
