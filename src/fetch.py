from minet import multithreaded_fetch
from minet.fetch import FetchResult as MinetFetchResult
from ural import normalize_url
from tqdm.auto import tqdm


class Response():
    def __init__(self, response) -> None:
        self.status = response.status
        self.data = response.data


class FetchResult():
    def __init__(self, MinetFetchResult:MinetFetchResult) -> None:
        self.item = MinetFetchResult.item["claim"]
        self.entered_url = MinetFetchResult.item["url"]
        self.domain = MinetFetchResult.domain
        self.url = normalize_url(MinetFetchResult.url)
        self.meta = MinetFetchResult.meta
        self.resolved = MinetFetchResult.resolved
        self.response = None
        self.domain_data = {}
        
        if MinetFetchResult.response:
            self.response = Response(MinetFetchResult.response)
        
        self.item["claim-review"]["itemReviewed"]["appearance"].update({"domain":self.domain})


def fetch_results(claim_url_pairs:list[dict]):
    """
    params:
        claim_url_pairs (list[dict]): a list of dictionaries with two keys, 
        one of which is "url"
    
    returns:
        List of FetchResult objects, which were created by fetching the URL 
        with minet. The FetchResult object has the attribute "item" to hold 
        whatever was in the incoming dictionary's second key, i.e. "claim"
    """
    claim_reader = tqdm(multithreaded_fetch(claim_url_pairs, key=lambda x: x["url"]), total=len(claim_url_pairs), desc="Multithreaded Fetch")
    return [FetchResult(result) for result in claim_reader]
