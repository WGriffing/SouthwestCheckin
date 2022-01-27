import json
import logging
import os
import sys
from time import sleep

import requests

BASE_URL = "https://mobile.southwest.com/api/"
CHECKIN_INTERVAL_SECONDS = 0.25
MAX_ATTEMPTS = 40

logging.getLogger().setLevel(logging.DEBUG)


class Reservation:
    def __init__(self, number, first, last, verbose=False):
        self.number = number
        self.first = first
        self.last = last
        self.verbose = verbose

    @staticmethod
    def generate_headers():
        this_dir = os.path.dirname(__file__)
        header_file = open(
            os.path.join(this_dir, "../../southwest-headers/southwest_headers.json")
        )
        # the header file is expected to exist by following the directions in https://github.com/byalextran/southwest-headers/tree/develop
        tricky_headers = json.load(header_file)

        return {
            "Host": "mobile.southwest.com",
            "Content-Type": "application/json",
            "Accept": "*/*",
            "X-Channel-ID": "MWEB",
            **tricky_headers,
        }

    # You might ask yourself, "Why the hell does this exist?"
    # Basically, there sometimes appears a "hiccup" in Southwest where things
    # aren't exactly available 24-hours before, so we try a few times
    def safe_request(self, url, body=None):
        try:
            attempts = 0
            headers = Reservation.generate_headers()
            while True:
                if body is not None:
                    r = requests.post(url, headers=headers, json=body)
                else:
                    r = requests.get(url, headers=headers)
                data = r.json()
                if self.verbose:
                    print("----- request headers begin -----")
                    print(json.dumps(headers, indent=2))
                    print("----- request headers end -----")
                if "httpStatusCode" in data and data["httpStatusCode"] in [
                    "NOT_FOUND",
                    "BAD_REQUEST",
                    "FORBIDDEN",
                ]:
                    attempts += 1
                    if not self.verbose:
                        print(data["message"])
                    else:
                        print("----- response headers begin -----")
                        print(r.headers)
                        print("----- response headers end -----")
                        print("----- response data begin -----")
                        print(json.dumps(data, indent=2))
                        print("----- response data end -----")
                    if attempts > MAX_ATTEMPTS:
                        sys.exit("Unable to get data, killing self")
                    sleep(CHECKIN_INTERVAL_SECONDS)
                    continue
                if self.verbose:
                    print("----- response headers begin -----")
                    print(r.headers)
                    print("----- response headers end -----")
                    print("----- response data begin -----")
                    print(json.dumps(data, indent=2))
                    print("----- response data end -----")
                return data
        except ValueError:
            # Ignore responses with no json data in body
            pass

    def load_json_page(self, url, body=None):
        data = self.safe_request(url, body)
        if not data:
            return
        for k, v in list(data.items()):
            if k.endswith("Page"):
                return v

    def with_suffix(self, uri):
        return "{}{}{}?first-name={}&last-name={}".format(
            BASE_URL, uri, self.number, self.first, self.last
        )

    def lookup_existing_reservation(self):
        # Find our existing record
        return self.load_json_page(
            self.with_suffix(
                "mobile-air-booking/v1/mobile-air-booking/page/view-reservation/"
            )
        )

    def get_checkin_data(self):
        return self.load_json_page(
            self.with_suffix(
                "mobile-air-operations/v1/mobile-air-operations/page/check-in/"
            )
        )

    def checkin(self):
        data = self.get_checkin_data()
        info_needed = data["_links"]["checkIn"]
        url = "{}mobile-air-operations{}".format(BASE_URL, info_needed["href"])
        print("Attempting check-in...")
        confirmation = self.load_json_page(url, info_needed["body"])
        return confirmation
