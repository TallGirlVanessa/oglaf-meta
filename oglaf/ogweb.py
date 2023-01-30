#!/usr/bin/env python3

import json
import re
import requests
from bs4 import BeautifulSoup
from time import sleep
from . import knowledge


class OGWeb:
    """Helper class to interact with the Oglaf web pages"""

    PROTOHOST = "https://www.oglaf.com"
    ARCHIVE_URL = PROTOHOST + "/archive/"

    def __init__(self):
        self.session = requests.Session()
        self.strip = dict()

    def get_newest(self):
        """Get the newest strip URL from the archive"""
        self.newest_url = None
        archive = self.get_page(self.ARCHIVE_URL)
        soup = BeautifulSoup(archive, "html.parser")

        newest_img = soup.find("img", attrs={"width": "400", "height": "100"})
        if newest_img:
            myanchor = newest_img.find_parent("a")
            if myanchor:
                self.newest_url = self.PROTOHOST + myanchor.get("href")

    def get_page(self, url):
        """Get a URL and return the content text, or None on error"""
        r = self.session.get(url, cookies={"AGE_CONFIRMED": "yes"})
        if r.status_code == requests.codes.ok:
            return r.text
        elif r.status_code == 421:
            sleep(5)
            return get_page(url)
        else:
            print("Oops getting page {} ({})".format(url, r.status_code))
            return None

    # Populate:
    #   self.strip['title'] = 'This strip has a title'
    #   self.strip['urls'] = [ 'https://www.oglaf.com/blah/', 'https://www.oglaf.com/blah/2/' ]
    #   self.strip['prev'] = 'https://www.oglaf.com/blah/'
    #   self.strip['next'] = 'https://www.oglaf.com/blah/'
    def get_strip_urls(self, pagetext):
        """Given the page source for a strip, find downstream, sibling, and upstream URLs"""
        soup = BeautifulSoup(pagetext, "html.parser")

        # Get the canonical URL for the current page then delete it
        canonical_link = soup.find("link", attrs={"rel": "canonical"})
        cur_url = canonical_link.get("href")
        canonical_link.decompose()

        # Delete the "prev" link so we don't process it later
        prev_link = soup.find("a", attrs={"rel": "prev"})
        prev_url = None
        if prev_link is not None:
            prev_url = self.PROTOHOST + prev_link.get("href")
            prev_link.decompose()

        # Get the "next" link then delete it
        next_link = soup.find("a", attrs={"rel": "next"})
        next_url = None
        if next_link is not None:
            next_url = self.PROTOHOST + next_link.get("href")
            next_link.decompose()

        # Convert current URI for comparison: https://www.oglaf.com/glove/2/ -> /glove/
        base_path = re.sub(r"^" + self.PROTOHOST, "", cur_url, flags=re.IGNORECASE)
        base_path = re.sub(r"/\d+/$", "/", base_path)
        base_path = base_path.rstrip("/")

        if prev_url is not None and base_path not in prev_url:
            # We must be on the first page of a strip
            strip_title = re.sub(r" page 1", "", soup.title.string, flags=re.IGNORECASE)
            self.strip["title"] = strip_title
            self.strip["prev"] = prev_url
            self.strip["urls"] = []
        if next_url is None or base_path not in next_url:
            # We must be on the last page of a strip
            self.strip["next"] = next_url

        self.strip["urls"].append(cur_url)

        # Find occasional epilogue or other add-ons (like /roughtrade/vocab/)
        epi_page = None
        for url in soup.find_all("a"):
            href = url.get("href")
            if base_path in href and href != cur_url:
                epi_page = self.PROTOHOST + href

        next_page_text = None
        if epi_page is not None:
            next_page_text = self.get_page(epi_page)
        if next_url is not None and base_path in next_url:
            next_page_text = self.get_page(next_url)

        if next_page_text is not None:
            # RECURSION HERE
            # To grab URLs for any other URLs for this strip
            self.get_strip_urls(next_page_text)


if __name__ == "__main__":
    print("Don't wank me.  I'm telling!!")
