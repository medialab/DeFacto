import trafilatura
from fetch import FetchResult
from bs4 import BeautifulSoup


def update_appearance(item, update):
    item["claim-review"]["itemReviewed"]["appearance"].update(update)
    return item


def update_itemReviewed(item, update):
    item["claim-review"]["itemReviewed"].update(update)
    return item


def webpage_enrich(result:FetchResult):
    if result.response and result.response.status == 200:
        result.item = update_appearance(result.item, {"text":None})
        if result.response and result.response.data and result.meta.get("encoding"):
            html = result.response.data.decode(result.meta["encoding"])
            text = trafilatura.extract(html)
            soup = BeautifulSoup(html, features="lxml")
            title = soup.title
            lang = soup.html.get("lang")
            result.item = update_appearance(result.item, {"text":text, "domain-specific":{"title":title.text, "lang":lang}})
            result.item = update_itemReviewed(result.item, {"lang":lang})
    return result


def tweet_text(result:FetchResult):
    if result:
        result.item = update_appearance(result.item, {"text":None, "domain-specific":result.domain_data})
        if result.domain_data.get("normalized_tweet_payload"):
            result.item = update_itemReviewed(result.item, {"lang":result.domain_data["normalized_tweet_payload"].get("lang")})
            text = result.domain_data["normalized_tweet_payload"].get("text")
            result.item = update_appearance(result.item, {"text":text})
        return result
