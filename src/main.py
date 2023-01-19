import os

import casanova
import click
from minet import multithreaded_fetch
from tqdm.auto import tqdm

from CONSTANTS import CACHE_DIR, FETCH_RESULTS_CSV_HEADERS, RESULTS_CSV
from fetch import formatted_fetch_result


@click.command()
@click.argument("datafile", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option("-u", "--url-col", nargs=1, type=str, required=True)
@click.option("-o", "--outfile", nargs=1, type=str, required=False)
def main(datafile, url_col, outfile):

    # ------------------------------------------------------- #
    #                   Verify parameters
    # ------------------------------------------------------- #
    if not os.path.isfile(datafile):
        raise FileNotFoundError
    if not outfile:
        if not os.path.isdir(CACHE_DIR): os.mkdir(CACHE_DIR)
        OUTFILE = RESULTS_CSV
    else:
        if not os.path.exists(outfile): os.makedirs(os.path.dirname(outfile), exist_ok=True)
        OUTFILE = outfile
    # ------------------------------------------------------- #

    # ------------------------------------------------------- #
    #               Fetch URLs and parse HTML
    # ------------------------------------------------------- #
    # Open the in- and out-files
    total = casanova.reader.count(datafile)
    with open(datafile) as f, open(OUTFILE, "w", encoding="utf-8") as of:
        enricher = casanova.threadsafe_enricher(f, of, add=FETCH_RESULTS_CSV_HEADERS)

        # Find where in the row the URL is
        url_pos = enricher.headers[url_col]

        # Using Minet's mulithreaded fetch, format and decode key details for the CSV
        for fetch_result in tqdm(multithreaded_fetch(enricher, key=lambda x: x[1][url_pos]), total=total, desc="Multithreaded fetch"):
            index, row, additional_columns = formatted_fetch_result(fetch_result)
            enricher.writerow(index=index, row=row, add=additional_columns)
    # ------------------------------------------------------- #


if __name__ == '__main__':
    main()
