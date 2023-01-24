import json
import os
from pathlib import Path

import urllib3


def get_endpoint(config_filepath):
    with open(config_filepath, "r", encoding="utf-8") as opened_config:
        try:
            data = json.load(opened_config)
            try: endpoint = data["endpoint"] # Key in JSON config file
            except KeyError as error:
                print(f"The configuration JSON file is missing an endpoint key.")
                raise error
        except json.decoder.JSONDecodeError as error:
            print(f"Configuration file is not a properly formatted JSON file.")
            raise error
        return endpoint


def request_data(endpoint):
    http = urllib3.PoolManager()
    print("Getting response from database...")
    response = http.request("GET", endpoint)
    if response.status == 200:
        data = json.loads(response.data)
    else:
        raise TimeoutError(f"Server did not return a good response.\nResponse: {response.status}")
    return data


def manage_filepath(fp):
    dirs, _ = os.path.split(fp)
    Path(dirs).mkdir(parents=True, exist_ok=True)
