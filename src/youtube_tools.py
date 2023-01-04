import json
import os

from minet.youtube import YouTubeAPIClient
from minet.youtube.constants import YOUTUBE_API_BASE_URL
from ural.youtube import (YoutubeChannel, YoutubeUser, YoutubeVideo,
                          parse_youtube_url)
from fetch import Result

youtube_cache_filepath = os.path.join("cache", "youtube.json")
temp_cache_filepath = os.path.join("cache", "temp_youtube.json")


class YouTubeWrapper:
    def __init__(self, filepath) -> None:
        with open(filepath, "r", encoding="utf-8") as opened_config:
            config = json.load(opened_config)["youtube"]
        self.config = config
        self.wrapper = YouTubeAPIClient(key=self.config["key"])


def youtube_batch_processor(wrapper:YouTubeAPIClient, results:list[Result]):
    results = [get_ids(result) for result in results]

    print("")
    [print(result.meta.data) for result in results]

    # call_client(wrapper, results)
    return results


def get_ids(result:Result):
    print("")
    print(f"BEFORE: {result.meta.data}")
    # 1st result -- {}
    # 2nd result -- {'type': 'YoutubeVideo', 'video_id': 'iBBtuSOEQC0'} <-- BAD

    parsed_youtube_url = parse_youtube_url(result.url)
    result.meta.data.update({"type":parsed_youtube_url.__class__.__name__})
    if isinstance(parsed_youtube_url, YoutubeVideo):
        result.meta.data.update({"video_id":parsed_youtube_url.id})
    elif isinstance(parsed_youtube_url, YoutubeUser):
        result.meta.data.update({"user_id":parsed_youtube_url.id, "user_name":parsed_youtube_url.name})
    elif isinstance(parsed_youtube_url, YoutubeChannel):
        result.meta.data.update({"channel_id":parsed_youtube_url.id, "channel_name":parsed_youtube_url.name})

    print(f"AFTER: {result.meta.data}")
    # 1st result -- {'type': 'YoutubeVideo', 'video_id': 'iBBtuSOEQC0'}
    # 2nd result -- {'type': 'YoutubeVideo', 'video_id': 'bj6PcWBgVN4'}
    return result


def call_client(wrapper:YouTubeAPIClient, results:list[Result]):
    ids = [result.meta.data.get("video_id") for result in results if result.meta.data["type"] == "YoutubeVideo"]
    video_index = {}
    [video_index.update({id:data}) for id,data in wrapper.videos(ids)]
    [update_datafields(result, video_index) for result in results if result.meta.data.get("video_id")]


def update_datafields(result:Result, video_index:dict):
    id = result.meta.data.get("video_id")
    payload:YoutubeVideo = video_index.get(id)
    #print("")
    #print(payload)



        