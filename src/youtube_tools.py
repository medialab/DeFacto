from fetch import FetchResult

from ural.youtube import parse_youtube_url
from ural.youtube import YoutubeVideo, YoutubeUser, YoutubeChannel
from minet.youtube.scrapers import scrape_channel_id, YOUTUBE_SCRAPER_POOL
from text import update_appearance
from bs4 import BeautifulSoup
from minet.web import request
import json
import os

youtube_cache_filepath = os.path.join("cache", "youtube.json")
temp_cache_filepath = os.path.join("cache", "temp_youtube.json")

def youtube_enrich(result:FetchResult):

    parsed_youtube_url = parse_youtube_url(result.url)
    if isinstance(parsed_youtube_url, YoutubeUser):
        result.domain_data.update({"user_id":parsed_youtube_url.id, "user_name":parsed_youtube_url.name})

    elif isinstance(parsed_youtube_url, YoutubeVideo):

        video_id = parsed_youtube_url.id

        result.domain_data.update({"video_id":video_id})
        url = "https://"+result.url
        try:
            channel_id, channel_name, video_title, video_description, video_views, date_published = scrape_video_info(url)
            result.domain_data.update({
                "channel_id":channel_id,
                "channel_name":channel_name,
                "video_title":video_title,
                "video_description":video_description,
                "video_views":video_views,
                "video_published":date_published
                })
        except:
            result.domain_data.update({"channel_id":None})

    elif isinstance(parsed_youtube_url, YoutubeChannel):

        channel_id = parsed_youtube_url.id

        if not channel_id:
            url = "https://"+result.url
            channel_id = scrape_channel_id(url)
            result.domain_data.update({"channel_id":channel_id, "channel_name":parsed_youtube_url.name, "video_id":None})                

    result.item = update_appearance(result.item, {"domain-specific": result.domain_data})

    return result


def scrape_video_info(url):
    err, response = request(url, pool=YOUTUBE_SCRAPER_POOL)
    if err:
        raise err
    soup = BeautifulSoup(response.data.decode("utf-8"), "lxml")
    
    channel_id = xpath(soup, "meta", {"itemprop": "channelId"})
    
    channel_name = xpath(soup, "link", {"itemprop": "name"})

    video_title = xpath(soup, "meta", {"itemprop": "name"})

    video_description = xpath(soup, "meta", {"itemprop": "description"})

    views = xpath(soup, "meta", {"itemprop":"interactionCount"})

    date = xpath(soup, "meta", {"itemprop":"datePublished"})

    return channel_id, channel_name, video_title, video_description, views, date


def xpath(soup:BeautifulSoup, tag:str, attribute:dict):
    tag = soup.find(tag, attribute)
    if tag:
        return tag.get("content")