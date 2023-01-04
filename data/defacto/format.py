import json
import os

import urllib3
from ural import is_url

if not os.path.isdir("data"): os.mkdir("data")

database_response_filepath = os.path.join("data", "defacto.json")
config_filepath = os.path.join("config.json")

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

claim_with_url = [claim_url_pair for claim_url_pair in 
            [
                {"url":claim.get(\
                    "claim-review",{}).get(\
                        "itemReviewed",{}).get(\
                            "appearance",{}).get(\
                                "url"),
                "context":{"claim":claim}} 
                for claim in data.get("data")
            ] 
        if claim_url_pair["url"] and is_url(claim_url_pair["url"])]

with open(database_response_filepath, "w") as f:
    json.dump(claim_with_url, f, indent=4)
    print(f"Wrote database response to {database_response_filepath}.")
