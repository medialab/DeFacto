import concurrent.futures
import json
import os
import pickle

import click
from tqdm.auto import tqdm
from ural.facebook import is_facebook_url
from ural.telegram import is_telegram_url
from ural.twitter import is_twitter_url
from ural.youtube import is_youtube_url

from fetch import Result, fetch_results
from text import webpage_html_parser
from tweet_tools import WrapperConfig, tweet_batch_processor
from youtube_tools import YouTubeWrapper, youtube_batch_processor

# file paths
cache_dir = "cache"
output_dir = "output"
updated_data_json = os.path.join(output_dir, "data.json")
config_filepath = os.path.join("config.json")
pickled_results_filepath = os.path.join(cache_dir, "fetchResults.pickle")


if not os.path.isdir(cache_dir):
    os.mkdir(cache_dir)
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

@click.command()
@click.argument("datafile")
@click.option("--debug/--no-debug", default=False)
def main(datafile, debug):

    if not os.path.isfile(datafile):
        raise FileNotFoundError

    click.echo(f"Debug mode is {'on' if debug else 'off'}")

    # ------------------------------------------------------- #
    # Open formatted data file and fetch URLs
    with open(datafile, "r") as f:
        try:
            data = json.load(f)
        except:
            raise Exception("Currently, only JSON files are compatible.")

    if not debug or not os.path.isfile(pickled_results_filepath):

        results:list[Result] = fetch_results(data)
        results = [result for result in results if result.response and result.response.status == 200]

        if debug:
            # Pickle filtererd results
            with open(pickled_results_filepath, "wb") as f:
                pickle.dump(results, f, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        with open(pickled_results_filepath, "rb") as f:
            results:list[Result] = pickle.load(f)
    # ------------------------------------------------------- #

    # ------------------------------------------------------- #
    # Configure API clients and/or raise key errors in config file
    twitter_wrapper = WrapperConfig(config_filepath).wrapper
    youtube_wrapper = YouTubeWrapper(config_filepath).wrapper
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
        web_results = list(tqdm(executor.map(webpage_html_parser, web_results), total=len(web_results), desc="Multiprocess Webpage HTML"))
    # ------------------------------------------------------- #
    
    # ------------------------------------------------------- #
    # Batched text and metadata extraction from Twitter API
    BATCH_SIZE = 20
    tweet_batches = [twitter_results[x:x+BATCH_SIZE] for x in range(0, len(twitter_results), BATCH_SIZE)]

    batch_processed_twitter_results = []
    for batch in tqdm(tweet_batches, total=len(tweet_batches), desc="Batch Process Tweets"):
        batch_processed_twitter_results.extend(tweet_batch_processor(twitter_wrapper, batch))

    twitter_results = batch_processed_twitter_results
    # ------------------------------------------------------- #

    # ------------------------------------------------------- #
    #with concurrent.futures.ProcessPoolExecutor() as executor:
    #    youtube_results = list(tqdm(executor.map(youtube_parsing_manager, youtube_results), total=len(youtube_results), desc="Mulitprocess YouTube URL Parsing"))

    BATCH_SIZE = 20
    youtube_batches = [youtube_results[x:x+BATCH_SIZE] for x in range(0, len(youtube_results), BATCH_SIZE)]
    batch_processed_youtube_results = []
    for batch in tqdm(youtube_batches, total=len(youtube_batches), desc="Batched Multithreaded YouTube"):
        batch_processed_youtube_results.extend(youtube_batch_processor(youtube_wrapper, batch))

    youtube_results = batch_processed_youtube_results


    # Multithreaded parsing of Youtube URLs
    #with concurrent.futures.ThreadPoolExecutor() as executor:
    #    youtube_results = list(tqdm(executor.map(youtube_batch_processor, multithreading_args), total=len(youtube_results), desc="Multithreaded YouTube Scraping"))
    # ------------------------------------------------------- #













    """
    # ------------------------------------------------------- #
    # Combine results from different platforms and write to JSON
    results = web_results+twitter_results+youtube_results+facebook_results

    with open(updated_data_json, "w", encoding="utf-8") as open_json:

        indexed_results = {}
        [indexed_results.update({result.item["id"]:result.item}) for result in results]
        
        claims = [indexed_results[claim["id"]] for claim in data["data"] if claim["id"] in indexed_results.keys()]

        data.update({"data":claims})

        json.dump(data, open_json, indent=4, ensure_ascii=False)
    """

if __name__ == '__main__':
    main()
