import csv
import os
import sys

import click

from utils import get_endpoint, manage_filepath, request_data

data_dir = os.path.join(".", "data")


@click.command
@click.option("-c", "config", required=False, type=click.Path(exists=True), nargs=1)
@click.option("-o", "outfile", required=True, type=click.Path(exists=False), nargs=1)
def request(config, outfile):

    # Verify the parameters
    endpoint = get_endpoint(config)

    # Download JSON response from database
    data = request_data(endpoint)

    # Parse URLs from the data and write to a temporary CSV file
    manage_filepath(outfile)

    with open(outfile, "w", encoding="utf-8") as opened_outfile:
        fieldnames = ["id_column", "url_column"]
        writer = csv.DictWriter(opened_outfile, fieldnames=fieldnames)
        writer.writeheader()
        for claim in data["data"]:
            id = claim.get("id")
            url = claim.get("claim-review",{}).get("itemReviewed",{}).get("appearance",{}).get("url")
            writer.writerow({"id_column":id, "url_column":url})


@click.command
@click.option("-f", "--file", required=True, type=click.Path(exists=True), nargs=1)
def send_to_database(file):
    pass


@click.group
def cli() -> None:
    pass


if __name__ == "__main__":
    sys.tracebacklimit=0
    cli.add_command(request)
    cli.add_command(send_to_database)
    cli()
