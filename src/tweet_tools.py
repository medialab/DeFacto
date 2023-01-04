import json

from twitwi import TwitterWrapper, normalize_tweets_payload_v2
from ural.twitter import TwitterTweet, TwitterUser, TwitterList, parse_twitter_url
from text import tweet_text

from fetch import Result

# params taken from: https://github.com/python-twitter-tools/twitter/tree/api_v2
v2params = {
        "tweet.fields": "attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld",
        "user.fields":  "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
        "media.fields": "duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics",
        "expansions": "author_id,referenced_tweets.id,referenced_tweets.id.author_id,entities.mentions.username,attachments.poll_ids,attachments.media_keys,in_reply_to_user_id,geo.place_id"
        }


class WrapperConfig:
    def __init__(self, filepath) -> None:
        with open(filepath, "r", encoding="utf-8") as opened_config:
            config = json.load(opened_config)["twitter"]
        self.config = config
        self.wrapper =  TwitterWrapper(
                        config["token"],
                        config["secret_token"],
                        config["key"],
                        config["secret_key"],
                        listener=None,
                        api_version="2"
                    )


def call_client(wrapper:TwitterWrapper, results:list[Result]):
    """
    Function to call the Twitter API with a batch of Tweet IDs, and update the Result object's data fields.

    params:
        wrapper (twitwi.TwitterWrapper): configured instance of Twitwi's TwitterWrapper
        results (list[fetch.Result]): batch of Result objects
    
    returns:
        batch of Result objects whose meta fields (data, text, audience) are enriched 
    """
    # Extract the IDs of this batch of tweets
    ids = [result.meta.data.get("tweet_id") for result in results if result.meta.data.get("tweet_id")]
    # Call the Twitter API with the IDs and parameters
    response = wrapper.call(["tweets"], ids=",".join(ids), params=v2params)
    # Normalize the API's response
    normalized_tweets = normalize_tweets_payload_v2(response, collection_source="api")

    # Pair new Twitter data with the original fetch result object
    tweet_index = { k:v for (k,v) in zip([tweet["id"] for tweet in normalized_tweets], normalized_tweets)}
    [update_datafields(result, tweet_index) for result in results if result.meta.data.get("tweet_id")]

    # Update the text field in the claim's appearance
    [tweet_text(result) for result in results]


def get_ids(result:Result):
    """Helper function to parse the relevant ID (i.e. tweet, user, list)."""
    parsed_twitter_url = parse_twitter_url(result.url)
    if isinstance(parsed_twitter_url, TwitterTweet):
        result.meta.data.update({"tweet_id":parsed_twitter_url.id, "user_screen_name":parsed_twitter_url.user_screen_name})
    elif isinstance(parsed_twitter_url, TwitterUser):
        result.meta.data.update({"user_screen_name":parsed_twitter_url.screen_name})
    elif isinstance(parsed_twitter_url, TwitterList):
        result.meta.data.update({"twitter_list_id":parsed_twitter_url.id})
    return result


def update_datafields(result:Result, tweet_index:dict):
    """Helper function to update a Result object's meta fields (data, audience)."""
    id = result.meta.data.get("tweet_id")
    payload:dict = tweet_index.get(id)

    result.meta.data.update({"normalized_tweet_payload":payload})
    if payload:
        result.meta.audience.update({
            "likes": payload.get("like_count"),
            "comments": payload.get("reply_count"),
            "tweet":{
                "retweets":payload.get("retweet_count"),
                "quote_tweets":payload.get("quote_count"),
                "user_followers":payload.get("user_followers"),
                "user_mutual_followers":payload.get("user_friends"),
            }
        })


def tweet_batch_processor(wrapper:TwitterWrapper, results:list[Result]):
    """Main function to enrich a batch of tweets with metadata."""

    # parse the relevant ID from the Twitter URL
    results = [get_ids(result) for result in results]

    # send a batch of parsed results to the Twitter API
    call_client(wrapper, results)

    return results
