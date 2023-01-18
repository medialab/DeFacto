import trafilatura
from bs4 import BeautifulSoup
from fetch import Result
from ural.facebook import is_facebook_url
from ural.telegram import is_telegram_url
from ural.twitter import is_twitter_url
from ural.youtube import is_youtube_url


def multiprocessing_text(result:Result):

    title, text, lang = web_text(result)

    return {
        "id":result.id,
        "domain":result.domain,
        "fetched_url":result.fetched_url,
        "normalized_url":result.normalized_url,
        "resolved_url":result.resolved_url,
        "fetch_date":result.fetch_date,
        "status":result.response.status,
        "title":title,
        "text":text,
        "lang":lang,
    }


def web_text(result:Result):
    title, text, lang = None, None, None
    platforms = ["facebook.com", "twitter.com", "fb.watch", "youtube.com", "tiktok.com"]
    if result.response and result.response.status == 200 and result.encoding and \
        not any(domain == result.domain for domain in platforms) and \
            not is_twitter_url(result.fetched_url) and \
                not is_youtube_url(result.fetched_url) and \
                    not is_facebook_url(result.fetched_url) and \
                        not is_telegram_url(result.fetched_url):
                            html = result.response.data.decode(result.encoding)
                            soup = BeautifulSoup(html, features="lxml")
                            title = soup.title.text
                            text = trafilatura.extract(html)
                            lang = soup.html.get("lang")
    return title, text, lang
