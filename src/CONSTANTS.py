import os

from ural.facebook import is_facebook_url
from ural.telegram import is_telegram_url
from ural.twitter import is_twitter_url
from ural.youtube import is_youtube_url

CACHE_DIR = "cache"

SOCIAL_MEDIA_PLATFORMS = ["facebook.com", "twitter.com", "fb.watch", "youtube.com", "tiktok.com"]

URAL_DOMAIN_FUNCTIONS = [is_facebook_url, is_telegram_url, is_twitter_url, is_youtube_url]

FETCH_RESULTS_CSV_HEADERS = ["domain", "fetched_url", "normalized_url", "resolved_url", "fetch_date", "status", "webpage_title", "webpage_text", "webpage_lang"]
