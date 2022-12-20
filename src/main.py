import concurrent.futures
import json
import os
import pickle

import click
import urllib3
from tqdm.auto import tqdm
from ural import is_url

from fetch import FetchResult, fetch_results
from text import webpage_enrich
from tweet_tools import tweet_enrich
from youtube_tools import youtube_enrich
from ural.youtube import is_youtube_url
from ural.telegram import is_telegram_url
from ural.facebook import is_facebook_url
from ural.twitter import is_twitter_url

# file paths
cache_dir = "cache"
output_dir = "output"
database_response_filepath = os.path.join(cache_dir,"response.json")
updated_data_json = os.path.join(output_dir, "data.json")
config_filepath = os.path.join("config.json")
pickled_results_filepath = os.path.join(cache_dir, "fetchResults.pickle")


if not os.path.isdir(cache_dir):
    os.mkdir(cache_dir)
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

@click.command()
@click.option('--debug/--no-debug', default=False)
def main(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")

    # ------------------------------------------------------- #
    # Get JSON response from database
    if not debug or not os.path.isfile(database_response_filepath):

        # Call the database's API
        with open(config_filepath, "r", encoding="utf-8") as opened_config:
            endpoint = json.load(opened_config)["endpoint"]
        http = urllib3.PoolManager()
        print("Getting response from database...")
        response = http.request("GET", endpoint)

        if response.status == 200:
            data = json.loads(response.data)
            if not isinstance(data.get("data"), list):
                raise AssertionError("The server did not return the expected data.")
        else:
            raise TimeoutError("Server did not return good response.")

        # If debugging, save API's response
        if debug:
            with open(database_response_filepath, "w") as f:
                json.dump(data, f, indent=4)
                print(f"Wrote database response to {database_response_filepath}.")
    
    else:
        with open(database_response_filepath, "r") as f:
            data = json.load(f)
    # ------------------------------------------------------- #

    # ------------------------------------------------------- #
    # Fetch valid URLs in the API's JSON response
    if not debug or not os.path.isfile(pickled_results_filepath):

        dfclaim_with_url = [claim_url_pair for claim_url_pair in 
            [
                {"claim":claim, 
                "url":claim.get(\
                    "claim-review",{}).get(\
                        "itemReviewed",{}).get(\
                            "appearance",{}).get(\
                                "url")} 
                for claim in data.get("data")
            ] 
        if claim_url_pair["url"] and is_url(claim_url_pair["url"])]

        results:list[FetchResult] = fetch_results(dfclaim_with_url)
        results = [result for result in results if result.response and result.response.status == 200]

        if debug:
            # Pickle filtererd results
            with open(pickled_results_filepath, "wb") as f:
                pickle.dump(results, f)
    else:
        with open(pickled_results_filepath, "rb") as f:
            results:list[FetchResult] = pickle.load(f)
    # ------------------------------------------------------- #

    # ------------------------------------------------------- #
    # Filter results        
    web_results = []
    twitter_results = []
    youtube_results = []
    facebook_results = []

    platforms = ["facebook.com", "twitter.com", "fb.watch", "youtube.com", "tiktok.com"]
    for result in results:
        if is_twitter_url(result.url): twitter_results.append(result)
        elif is_youtube_url(result.url): youtube_results.append(result)
        elif is_facebook_url(result.url): facebook_results.append(result)
        elif not is_telegram_url(result.url) and not any(domain == result.domain for domain in platforms):
            web_results.append(result)
    # ------------------------------------------------------- #

    # ------------------------------------------------------- #
    # Multiprocessing text, title, language extraction from HTML
    with concurrent.futures.ProcessPoolExecutor() as executor:
        web_results = list(tqdm(executor.map(webpage_enrich, web_results), total=len(web_results), desc="Multiprocess Webpage Text"))
    # ------------------------------------------------------- #

    # ------------------------------------------------------- #
    # Batched text and metadata extraction from Twitter API
    batch_size = 20
    tweet_batches = [twitter_results[x:x+batch_size] for x in range(0, len(twitter_results), batch_size)]
    processed_twitter_results = []
    for batch in tqdm(tweet_batches, total=len(tweet_batches), desc="Tweet Batches"):
        processed_twitter_results.extend(tweet_enrich(batch))

    twitter_results = processed_twitter_results
    # ------------------------------------------------------- #

    # ------------------------------------------------------- #
    # Multithreaded parsing of Youtube URLs
    with concurrent.futures.ThreadPoolExecutor() as executor:
        youtube_results = list(tqdm(executor.map(youtube_enrich, youtube_results), total=len(youtube_results), desc="Multiprocess YouTube URLs"))
    # ------------------------------------------------------- #














    # ------------------------------------------------------- #
    # Combine results from different platforms and write to JSON
    results = web_results+twitter_results+youtube_results+facebook_results

    with open(updated_data_json, "w", encoding="utf-8") as open_json:

        indexed_results = {}
        [indexed_results.update({result.item["id"]:result.item}) for result in results]
        
        claims = [indexed_results[claim["id"]] for claim in data["data"] if claim["id"] in indexed_results.keys()]

        data.update({"data":claims})

        json.dump(data, open_json, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
