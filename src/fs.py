import json

import casanova
import urllib3

yellow = "\033[1;33m"
green = "\033[0;32m"
reset = "\033[0m"


class JSONParams:
    def __init__(self, config) -> None:
        self.endpoint = None
        with open(config, "r", encoding="utf-8") as opened_config:
            try:
                data = json.load(opened_config)
                try: self.endpoint = data["endpoint"]
                except KeyError as error:
                    print(f"{yellow}The configuration JSON file is missing an endpoint key.{reset}")
                    raise error
            except json.decoder.JSONDecodeError as error:
                print(f"{yellow}Configuration file is not a properly formatted JSON file.{reset}")
                raise error

    def request(self):
        http = urllib3.PoolManager()
        print("Getting response from database...")
        response = http.request("GET", self.endpoint)
        if response.status == 200:
            data = json.loads(response.data)
        else:
            raise TimeoutError(f"{yellow}Server did not return a good response.{reset}\nResponse: {response.status}")
        return data


class CSVParams:
    def __init__(self, file, id_col, url_col) -> None:
        with open(file) as opened_df:
            reader = casanova.reader(opened_df)
            if not id_col in reader.fieldnames:
                print(f"{yellow}The ID column header '{id_col}' is not in the CSV file {file}.{reset}")
                raise KeyError
            if not url_col in reader.fieldnames:
                print(f"{yellow}The URL column header '{url_col}' is not in the CSV file {file}.{reset}")
                raise KeyError
