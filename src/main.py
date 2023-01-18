import concurrent.futures
import csv
import os
import pickle

import casanova
import click
from fetch import FETCHRESULTFIELDS, fetch, Result
from text import multiprocessing_text
from fs import CSVParams
from tqdm.auto import tqdm
from minet.cli.utils import LoadingBar

@click.command()
@click.argument("datafile", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option("-u", "--url-col", nargs=1, type=str, required=True)
@click.option("-i", "--id-col", nargs=1, type=str, required=True)
@click.option("--debug/--no-debug", default=False)
def main(datafile, debug, url_col, id_col):

    # ------------------------------------------------------- #
    #                   Verify parameters
    # ------------------------------------------------------- #
    if not os.path.isfile(datafile):
        raise FileNotFoundError
    CSVParams(file=datafile, id_col=id_col, url_col=url_col)
    click.echo(f"Debug mode is {'on' if debug else 'off'}")
    # ------------------------------------------------------- #

    # ------------------------------------------------------- #
    #               Fetch URLs and parse HTML
    # ------------------------------------------------------- #
    # Create the necessary file paths
    cache_dir = "cache"
    if not os.path.isdir(cache_dir): os.mkdir(cache_dir)
    pickled_results = os.path.join(cache_dir, "fetch.pickle")
    results_csv = os.path.join(cache_dir, "fetch.csv")

    # Open the in- and out-files
    total = casanova.reader.count(datafile)
    with open(datafile) as f, open(results_csv, "w", encoding="utf-8") as of:
        reader = casanova.reader(f)
        writer = csv.DictWriter(of, fieldnames=FETCHRESULTFIELDS)
        writer.writeheader()

        url_pos = reader.headers[url_col]
        id_pos = reader.headers[id_col]

        # If debugging and the fetch results are aleady cached, load the data
        if debug and os.path.isfile(pickled_results):
            with open(pickled_results, "rb") as f:
                fetch_results = pickle.load(f)
        # Otherwise, use Minet's multithreaded fetch to generate a list of pickle-able Result objects
        else:
            fetch_results = [Result(fetch_result, id_pos) for fetch_result in fetch(iterator=reader, key=url_pos, total=total)]
            with open(pickled_results, "wb") as f:
                pickle.dump(fetch_results, f, protocol=pickle.HIGHEST_PROTOCOL)

        # Use Python's multiprocessing to decode webpages' fetched HTML and parse the main text
        loading_bar = LoadingBar(desc="Multiprocessing text", unit="page", total=len(fetch_results))
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for result in executor.map(multiprocessing_text, fetch_results):
                writer.writerow(result)
                loading_bar.update()
    # ------------------------------------------------------- #

    # ------------------------------------------------------- #
    #                   Collect metadata
    # ------------------------------------------------------- #
    # Create the necessary file paths
    config_file = os.path.join("config.json")
    output_dir = "output"
    outfile = os.path.join(outfile, "enriched_results.csv")
    if not output_dir: os.mkdir(output_dir)

    # open the in- and out-files
    with open(results_csv) as f, open(outfile, "w") as of:
        enricher = casanova.enricher(f, of)




    # ------------------------------------------------------- #


if __name__ == '__main__':
    main()
