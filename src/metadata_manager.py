import casanova
from ural.facebook import is_facebook_url
from ural.twitter import is_twitter_url
from ural.youtube import is_youtube_url

def collect_metadata(row, fieldnames):
    row_as_dict = {f:c for f,c in list(zip(fieldnames, row))}
    url = row_as_dict.get("fetched_url")
    if is_twitter_url(url=url):
        pass
        # return = twitter_collection(row_as_dict)
    elif is_youtube_url(url=url):
        pass
        # return = youtube_collection(row_as_dict)
    elif is_facebook_url(url=url):
        pass
        # return = facebook_collection(row_as_dict)
