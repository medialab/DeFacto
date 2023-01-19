import os

import casanova
import click
from minet import multithreaded_fetch
from minet.cli.utils import LoadingBar

from CONSTANTS import CACHE_DIR, FETCH_RESULTS_CSV_HEADERS, RESULTS_CSV
from fetch import formatted_fetch_result


@click.command()
@click.argument("datafile", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option("-u", "--url-col", nargs=1, type=str, required=True)
@click.option("--debug/--no-debug", default=False)
def main(datafile, debug, url_col):

    # ------------------------------------------------------- #
    #                   Verify parameters
    # ------------------------------------------------------- #
    if not os.path.isfile(datafile):
        raise FileNotFoundError
    click.echo(f"Debug mode is {'on' if debug else 'off'}")
    # ------------------------------------------------------- #

    # ------------------------------------------------------- #
    #               Fetch URLs and parse HTML
    # ------------------------------------------------------- #
    # Create the necessary file paths
    if not debug or not os.path.isfile(RESULTS_CSV):
        if not os.path.isdir(CACHE_DIR): os.mkdir(CACHE_DIR)

        # Open the in- and out-files
        total = casanova.reader.count(datafile)
        with open(datafile) as f, open(RESULTS_CSV, "w", encoding="utf-8") as of:
            enricher = casanova.threadsafe_enricher(f, of, add=FETCH_RESULTS_CSV_HEADERS)

            # Find where in the row the URL is
            url_pos = enricher.headers[url_col]

            # Set up a loading bar to keep track of the multithread progress
            loading_bar = LoadingBar(desc="Multithreaded Fetch", unit="page", total=total)

            # Using Minet's mulithreaded fetch, format and decode key details for the CSV
            for fetch_result in multithreaded_fetch(iterator=enricher, key=lambda x: x[1][url_pos]):
                index, row, additional_columns = formatted_fetch_result(fetch_result)
                enricher.writerow(index=index, row=row, add=additional_columns)
                loading_bar.update()
    # ------------------------------------------------------- #


if __name__ == '__main__':
    main()
