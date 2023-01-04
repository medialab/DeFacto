from minet import multithreaded_fetch
from minet.fetch import FetchResult as MinetFetchResult
from tqdm.auto import tqdm
from ural import normalize_url
from dataclasses import dataclass, field


class Result():
    """Class for hodling all data related to a fetched URL."""
    def __init__(self, MinetFetchResult:MinetFetchResult) -> None:
        # accompanying data from which the URL was extracted
        self.context:dict = MinetFetchResult.item["context"]
        # the extracted URL
        self.item:str = MinetFetchResult.item["url"]
        # domain name that Minet fetched
        self.domain:str = MinetFetchResult.domain
        # URL that Minet fetched
        self.url:str = MinetFetchResult.url
        # metadata about the fetched media item
        self.meta = self.Meta(domain=self.domain)
        # URAL's normalized version of the URL that Minet fetched
        self.normalized_url:str = normalize_url(self.url)
        # Minet's metadata about the URL
        self.minet_meta:dict = MinetFetchResult.meta
        # URL's resolved path
        self.resolved:str = MinetFetchResult.resolved
        # reformatted data from Minet fetch's urllib response
        self.response = None

        if MinetFetchResult.response:
            self.response = self.Response(MinetFetchResult.response)
    
    class Response():
        """Class for reformatting the response sent from Minet fetch."""
        def __init__(self, response) -> None:
            self.status:int = response.status
            self.data:bytes = response.data

    @dataclass(init=True, repr=True)
    class Meta:
        """Class for holding metadata about the media item."""
        title: str = None
        text: str = None
        data: dict = field(default_factory=dict)
        audience: dict = field(default_factory=dict)

        def __init__(
            self,
            domain,
            title:str = "",
            text:str = "",
            data:field(default_factory=dict) = {},
            audience:field(default_factory=dict) = {"likes":"", "comments":"", "views":""}
        ) -> None:
            self.domain = domain
            self.title = title
            self.text = text
            self.data = data
            self.audience = audience


def fetch_results(data:list[dict]):
    """
    params:
        data (list[dict]): a list of dictionaries with two keys, one of which is "url"
    
    returns:
        List of Result objects, which were created by fetching the URL 
        with Minet. The Result object has the attribute "context" to hold 
        whatever accompanying data was in the incoming dictionary's key 
        "context" (i.e. "claim", as in the case of De Facto's database)
    """
    generator = tqdm(
        multithreaded_fetch(data, key=lambda x: x["url"]),
        total=len(data),
        desc="Multithreaded Fetch"
    )
    return [Result(result) for result in generator]
