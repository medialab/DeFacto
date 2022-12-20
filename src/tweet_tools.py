import json

from twitwi import TwitterWrapper, normalize_tweets_payload_v2
from ural import normalize_url
from ural.twitter import TwitterTweet, TwitterUser, TwitterList, parse_twitter_url
from text import tweet_text

from fetch import FetchResult

# params taken from: https://github.com/python-twitter-tools/twitter/tree/api_v2
v2params = {
        "tweet.fields": "attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld",
        "user.fields":  "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
        "media.fields": "duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics",
        "expansions": "author_id,referenced_tweets.id,referenced_tweets.id.author_id,entities.mentions.username,attachments.poll_ids,attachments.media_keys,in_reply_to_user_id,geo.place_id"
        }


def call_client(wrapper:TwitterWrapper, results:list[FetchResult]):
    # Extract the IDs of this batch of tweets
    ids = [result.domain_data.get("tweet_id") for result in results if result.domain_data.get("tweet_id")]
    # Call the Twitter API with the IDs and parameters
    response = wrapper.call(["tweets"], ids=",".join(ids), params=v2params)
    # Normalize the API's response
    normalized_tweets = normalize_tweets_payload_v2(response, collection_source="api")

    # Pair new Twitter data with the original fetch result object
    tweet_index = { k:v for (k,v) in zip([tweet["id"] for tweet in normalized_tweets], normalized_tweets)}
    [result.domain_data.update({"normalized_tweet_payload":tweet_index.get(result.domain_data.get("tweet_id"))}) for result in results if result.domain_data.get("tweet_id")]

    # Update the text field in the claim's appearance
    [tweet_text(result) for result in results]


def tweet_enrich(results:list[FetchResult]):
    with open("config.json", "r", encoding="utf-8") as opened_config:
        config = json.load(opened_config)["twitter"]

    wrapper = TwitterWrapper(
        config["token"],
        config["secret_token"],
        config["key"],
        config["secret_key"],
        listener=None,
        api_version="2"
    )

    # Update the result's domain data with the Tweet ID
    for result in results:
        parsed_twitter_url = parse_twitter_url(result.url)
        if isinstance(parsed_twitter_url, TwitterTweet):
            result.domain_data.update({"tweet_id":parsed_twitter_url.id, "user_screen_name":parsed_twitter_url.user_screen_name})
        elif isinstance(parsed_twitter_url, TwitterUser):
            result.domain_data.update({"user_screen_name":parsed_twitter_url.screen_name})
        elif isinstance(parsed_twitter_url, TwitterList):
            result.domain_data.update({"twitter_list_id":parsed_twitter_url.id})

    call_client(wrapper, results)

    return results
