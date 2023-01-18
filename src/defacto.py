import csv
import os
import sys

import click
from fs import CSVParams, JSONParams

data_dir = os.path.join(".", "data")


@click.command
@click.option("-c", "--config", required=False, type=click.Path(exists=True), nargs=1)
def request(config):

    # Verify the parameters
    params = JSONParams(config)

    # Download JSON response from database
    data = params.request()

    # Parse URLs from the data and write to a temporary CSV file
    if not os.path.isdir(data_dir): os.mkdir(data_dir)
    temp_raw_file = os.path.join(data_dir, "df_urls.csv")
    with open(temp_raw_file, "w", encoding="utf-8") as opened_outfile:
        fieldnames = ["id_column", "url_column"]
        writer = csv.DictWriter(opened_outfile, fieldnames=fieldnames)
        writer.writeheader()
        for claim in data["data"]:
            id = claim.get("id")
            url = claim.get("claim-review",{}).get("itemReviewed",{}).get("appearance",{}).get("url")
            writer.writerow({"id_column":id, "url_column":url})


@click.command
@click.option("-f", "--file", required=False, type=click.Path(exists=True), nargs=1)
@click.option("-u", "--url-column", required=True, type=str, nargs=1)
@click.option("-k", "--id-column", required=True, type=str, nargs=1)
def output(file, url_column, id_column):

    # Verify the parameters
    params = CSVParams(file, id_col=id_column, url_col=url_column)


@click.group
def cli() -> None:
    pass


if __name__ == "__main__":
    sys.tracebacklimit=0
    cli.add_command(request)
    cli.add_command(output)
    cli()
