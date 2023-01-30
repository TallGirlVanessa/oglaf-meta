#!/usr/bin/env python3

import json
import re
import functools


class TomeOfKnowledge:
    """Easily manipulate and interact with comic strip data."""

    JSON_META = "meta.json"

    def __init__(self, meta_file=JSON_META):
        """Initialize"""
        self.titles = dict()
        self.urls = dict()
        self.tags = dict()
        self.arcs = dict()
        self.lctitles = dict()
        self.lctags = dict()
        self.lcarcs = dict()
        self.order = dict()

        self.files = dict()
        self.metafile = meta_file
        self.load_meta()

    # Import JSON from file and raise exception on error
    def get_meta(self, f):
        """Load JSON from file and return the object"""
        try:
            with open(f, "r") as infile:
                fd = infile.read()
        except FileNotFoundError:
            raise Exception(
                "Your specified JSON file is not found or readable: {}".format(f)
            )
        return json.loads(fd)

    def add_strip(
        self, title=None, urls=None, publishorder=None, tags=list(), arcs=list()
    ):
        """Add a strip to the TomeOfKnowledge"""
        if title is None or urls is None or publishorder is None:
            raise Exception(
                "add_strip() requires at least title, urls and publish order"
            )
        elif title in self.titles.keys():
            raise Exception("Title to add '{}' already exists!".format(title))
        elif not isinstance(urls, list):
            raise Exception("URLs to add must be a list")
        elif publishorder in self.order.keys():
            raise Exception("The publish order you're trying to add already exists")

        self.titles[title] = dict()
        self.titles[title]["arcs"] = arcs
        self.titles[title]["publishOrder"] = publishorder
        self.titles[title]["tags"] = tags
        self.titles[title]["urls"] = urls

        for u in urls:
            self.urls[u] = title
        for t in tags:
            if t not in self.tags:
                self.tags[t] = list()
            self.tags[t].append(title)
        for a in arcs:
            if a not in self.arcs:
                self.arcs[a] = list()
            self.arcs[a].append(title)
        self.order[publishorder] = title

        return True

    # Build a matrix of data structures like:
    #   self.titles['Cumsprite']['arcs'] = [ 'Cumsprite' ]
    #   self.titles['Cumsprite']['publishOrder'] = '1'
    #   self.titles['Cumsprite']['tags'] = [ 'Ivan', 'Mistress' ]
    #   self.titles['Cumsprite']['urls'] = [ 'https://blah', 'https://blah/2' ]
    #   self.urls['https://blah'] = 'Cumsprite'
    #   self.tags['Ivan'] = [ 'Cumsprite' ]
    #   self.tags['Mistress'] = [ 'Cumsprite' ]
    #   self.arcs['Cumsprite'] = [ 'Cumsprite' ]
    #   self.order['0'] = 'Cumsprite'
    #
    def load_meta(self):
        """Load an archive of comic strip data"""
        j = self.get_meta(self.metafile)
        for title in j.keys():
            # Init this title's entry
            self.titles[title] = j[title]
            self.order[j[title]["publishOrder"]] = title

            # Lowercase title and URLs
            self.lctitles[title.lower()] = title
            for url in j[title]["urls"]:
                self.urls[url] = title

            # Load tags
            for tag in j[title]["tags"]:
                self.lctags[tag.lower()] = tag
                if tag not in self.tags:
                    self.tags[tag] = list()
                self.tags[tag].append(title)

            # Load story arcs
            for arc in j[title]["arcs"]:
                self.lcarcs[arc.lower()] = arc
                if arc not in self.arcs:
                    self.arcs[arc] = list()
                self.arcs[arc].append(title)

    def save_meta(self):
        """Write metadata to file"""
        with open(self.metafile, "w") as outfile:
            json.dump(self.titles, outfile, indent=2)


@functools.cache
def get_tome():
    return TomeOfKnowledge()


if __name__ == "__main__":
    print("Don't wank me.  I'm telling!!")
