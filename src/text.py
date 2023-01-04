import trafilatura
from fetch import Result
from bs4 import BeautifulSoup


def webpage_html_parser(result:Result):
    if result.response and result.response.status == 200 \
        and result.response.data and result.minet_meta.get("encoding"):
            html = result.response.data.decode(result.minet_meta["encoding"])
            soup = BeautifulSoup(html, features="lxml")
            result.meta.title = soup.title.text
            result.meta.text = trafilatura.extract(html)
            result.meta.data.update({"lang":soup.html.get("lang")})
    return result


def tweet_text(result:Result):
    if result:
        tweet_payload = result.meta.data.get("normalized_tweet_payload")
        if tweet_payload:
            result.meta.data.update({"lang":tweet_payload.get("lang")})
            result.meta.text = tweet_payload.get("text")
        return result
