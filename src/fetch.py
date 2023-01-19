import trafilatura
from bs4 import BeautifulSoup
from minet.fetch import FetchResult as MinetFetchResult
from ural import is_url, normalize_url

from CONSTANTS import (FETCH_RESULTS_CSV_HEADERS, SOCIAL_MEDIA_PLATFORMS,
                       URAL_DOMAIN_FUNCTIONS)


def formatted_fetch_result(fetch_result:MinetFetchResult):
    index, row = fetch_result.item[0], fetch_result.item[1]
    data = {k:None for k in FETCH_RESULTS_CSV_HEADERS}
    if fetch_result.url and is_url(fetch_result.url):
        data.update({
            "fetched_url":fetch_result.url,
            "normalized_url":normalize_url(fetch_result.url),
            "resolved_url":fetch_result.resolved,
            "fetch_date":fetch_result.meta.get("datetime_utc"),
            "domain":fetch_result.domain,
        })
        if fetch_result.response:
            status = fetch_result.response.status
            encoded_html = fetch_result.response.data
            encoding = fetch_result.meta.get("encoding")
            if status == 200 and encoding and \
                not any(domain == fetch_result.domain for domain in SOCIAL_MEDIA_PLATFORMS) and \
                    not any(fn(fetch_result.url) for fn in URAL_DOMAIN_FUNCTIONS):
                html = encoded_html.decode(encoding)
                soup = BeautifulSoup(html, features="lxml")
                data.update({
                    "webpage_title":soup.title.text,
                    "webpage_text":trafilatura.extract(html),
                    "webpage_lang":soup.html.get("lang")
                })

    return index, row, list(data.values())
