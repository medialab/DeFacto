from minet import multithreaded_fetch
from minet.fetch import FetchResult
from tqdm.auto import tqdm
from ural import is_url, normalize_url

FETCHRESULTFIELDS = ["id", "domain", "fetched_url", "normalized_url", "resolved_url", "fetch_date", "status", "title", "text", "lang"]

class Result:
    def __init__(self, fetch_result:FetchResult, id_pos:int):
        self.id = fetch_result.item[id_pos]
        self.fetched_url = fetch_result.url

        if self.fetched_url:
            self.domain = fetch_result.domain
            self.normalized_url = normalize_url(fetch_result.url)
            self.resolved_url = fetch_result.resolved
            self.fetch_date = fetch_result.meta.get("datetime_utc")
            self.encoding = fetch_result.meta.get("encoding")
        else:
            self.domain = None
            self.normalized_url = None
            self.resolved_url = None
            self.fetch_date = None
            self.encoding = None

        self.response = self.Response(fetch_result.response)

    class Response():
        """Class for reformatting the response sent from Minet fetch."""
        def __init__(self, response) -> None:
            if response:
                self.status:int = response.status
                self.data:bytes = response.data
            else:
                self.status = None
                self.data = None


def fetch(iterator, key, total):
    return tqdm(
        multithreaded_fetch(iterator, key=key_filter(key)),
        total=total,
        desc="Multithreaded fetch"
    )


def key_filter(key):
    return lambda x: x[key] if is_url(x[key]) else None
