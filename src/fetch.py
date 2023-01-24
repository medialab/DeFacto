import os

import casanova
import click
import trafilatura
from bs4 import BeautifulSoup
from minet import multithreaded_fetch
from minet.fetch import FetchResult as MinetFetchResult
from tqdm.auto import tqdm
from ural import is_url, normalize_url

from CONSTANTS import (FETCH_RESULTS_CSV_HEADERS, SOCIAL_MEDIA_PLATFORMS,
                       URAL_DOMAIN_FUNCTIONS)
from utils import manage_filepath


@click.command()
@click.argument("datafile", type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.option("-u", "--url-col", nargs=1, type=str, required=True)
@click.option("-o", "--outfile", nargs=1, type=click.Path(exists=False), required=True)
def main(datafile, url_col, outfile):

    # ------------------------------------------------------- #
    #                   Verify parameters
    # ------------------------------------------------------- #
    if not os.path.isfile(datafile):
        raise FileNotFoundError
    if not os.path.exists(outfile): manage_filepath(outfile)
    # ------------------------------------------------------- #

    # ------------------------------------------------------- #
    #               Fetch URLs and parse HTML
    # ------------------------------------------------------- #
    # Open the in- and out-files
    total = casanova.reader.count(datafile)
    with open(datafile) as f, open(outfile, "w", encoding="utf-8") as of:
        enricher = casanova.threadsafe_enricher(f, of, add=FETCH_RESULTS_CSV_HEADERS)

        # Find where in the row the URL is
        url_pos = enricher.headers[url_col]

        # Using Minet's mulithreaded fetch, format and decode key details for the CSV
        for fetch_result in tqdm(multithreaded_fetch(enricher, key=lambda x: x[1][url_pos]), total=total, desc="Multithreaded fetch"):
            index, row, additional_columns = formatted_fetch_result(fetch_result)
            enricher.writerow(index=index, row=row, add=additional_columns)
    # ------------------------------------------------------- #


def formatted_fetch_result(fetch_result:MinetFetchResult):
    index, row = fetch_result.item[0], fetch_result.item[1]
    data = {k:None for k in FETCH_RESULTS_CSV_HEADERS}
    if fetch_result.url and is_url(fetch_result.url):
        data.update({
            "fetched_url":fetch_result.url,
            "normalized_url":normalize_url(fetch_result.url),
            "resolved_url":fetch_result.resolved,
            "fetch_date":fetch_result.meta.get("datetime_utc"),
            "domain":fetch_result.domain,
        })
        if fetch_result.response:
            status = fetch_result.response.status
            data.update({"status":status})
            encoded_html = fetch_result.response.data
            encoding = fetch_result.meta.get("encoding")
            if status == 200 and encoding and \
                not any(domain == fetch_result.domain for domain in SOCIAL_MEDIA_PLATFORMS) and \
                    not any(fn(fetch_result.url) for fn in URAL_DOMAIN_FUNCTIONS):
                    try: html = encoded_html.decode(encoding)
                    except: html = encoded_html.decode(encoding, errors="ignore").encode("utf-8").decode("utf-8")
                    soup = BeautifulSoup(html, features="lxml")
                    if soup.title: data.update({"webpage_title":soup.title.text})
                    try: data.update({"webpage_lang":soup.html.get("lang")})
                    except: pass
                    try:
                        text = trafilatura.extract(html)
                        data.update({"webpage_text":text})
                    except: pass

    return index, row, list(data.values())


if __name__ == '__main__':
    main()
