#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file has been modified by the Webis Group 
# to fit the needs of the IR Anthology. 
# The original is part of the ACL Anthology. 

#
# Copyright of the original 2019 Marcel Bollmann <marcel@bollmann.me>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Usage: create_hugo_pages.py [--dir=DIR] [-c] [--debug]

Creates page stubs for the full anthology based on the YAML data files.

This script can only be run after create_hugo_yaml.py!

Options:
  --dir=DIR                Hugo project directory. [default: {scriptdir}/../build/]
  --debug                  Output debug-level log messages.
  -c, --clean              Delete existing files in target directory before generation.
  -h, --help               Display this helpful text.
"""

from glob import glob
from tqdm import tqdm
import os
import shutil
import json
import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    log.info("Can't load yaml C bindings, reverting to slow pure Python version")
    from yaml import Loader

def check_directory(cdir, clean=False):
    if not os.path.isdir(cdir) and not os.path.exists(cdir):
        os.mkdir(cdir)
        return True
    entries = os.listdir(cdir)
    if "_index.md" in entries:
        entries.remove("_index.md")
    if entries and not clean:
        raise Exception("Directory already exists and has content files: {}\nCall this script with the -c/--clean flag to automatically DELETE existing files".format(cdir))
    for entry in entries:
        entry = "{}/{}".format(cdir, entry)
        if os.path.isdir(entry):
            shutil.rmtree(entry)
        else:
            os.remove(entry)
    return True


def create_papers(srcdir, clean=False):
    """Creates page stubs for all papers in the Anthology."""
    print("Creating stubs for papers...")
    if not check_directory("{}/content/papers".format(srcdir), clean=clean):
        return

    # Go through all paper volumes
    for jsonfile in tqdm(glob("{}/data/papers/*.json".format(srcdir))):
        #print("Processing {}".format(jsonfile))
        with open(jsonfile, "r") as f:
            data = json.loads(f.read())
        # Create a paper stub for each entry in the volume
        for anthology_id, entry in data.items():
            paper_dir = "{}/content/papers/{}".format(srcdir, anthology_id.split("-")[0])
            if not os.path.exists(paper_dir):
                os.makedirs(paper_dir)
            with open("{}/{}.md".format(paper_dir, anthology_id), "w") as f:
                print("---", file=f)
                yaml.dump(
                    {"anthology_id": anthology_id, "title": entry["title"]},
                    default_flow_style=False,
                    stream=f,
                )
                print("---", file=f)


def create_volumes(srcdir, clean=False):
    """Creates page stubs for all proceedings volumes in the Anthology."""
    print("Creating stubs for volumes...")
    if not check_directory("{}/content/volumes".format(srcdir), clean=clean):
        return

    jsonfile = "{}/data/volumes.json".format(srcdir)
    #print("Processing {}".format(jsonfile))
    with open(jsonfile, "r") as f:
        data = json.loads(f.read())
    # Create a paper stub for each proceedings volume
    for anthology_id, entry in data.items():
        with open("{}/content/volumes/{}.md".format(srcdir, anthology_id), "w") as f:
            print("---", file=f)
            paper_dir = "/papers/{}/{}/".format(anthology_id.split("-")[0], anthology_id)
            yaml.dump(
                {
                    "anthology_id": anthology_id,
                    "title": entry["title"],
                    "aliases": [
                        paper_dir,
                    ],
                },
                default_flow_style=False,
                stream=f,
            )
            print("---", file=f)

    return data


def create_people(srcdir, clean=False):
    """Creates page stubs for all authors/editors in the Anthology."""
    print("Creating stubs for people...")
    if not check_directory("{}/content/people".format(srcdir), clean=clean):
        return

    for jsonfile in tqdm(glob("{}/data/people/*.json".format(srcdir))):
        #print("Processing {}".format(jsonfile))
        with open(jsonfile, "r") as f:
            data = json.loads(f.read())
        # Create a page stub for each person
        for name, entry in data.items():
            person_dir = "{}/content/people/{}".format(srcdir, name[0])
            if not os.path.exists(person_dir):
                os.makedirs(person_dir)
            yaml_data = {"name": name, "title": entry["full"], "lastname": entry["last"]}
            with open("{}/{}.md".format(person_dir, name), "w") as f:
                print("---", file=f)
                # "lastname" is dumped to allow sorting by it in Hugo
                yaml.dump(yaml_data, default_flow_style=False, stream=f)
                print("---", file=f)

    return data


def create_venues_and_events(srcdir, clean=False):
    """Creates page stubs for all venues and events in the Anthology."""
    jsonfile = "{}/data/venues.json".format(srcdir)
    #print("Processing {}".format(jsonfile))
    with open(jsonfile, "r") as f:
        data = json.loads(f.read())

    print("Creating stubs for venues...")
    if not check_directory("{}/content/venues".format(srcdir), clean=clean):
        return
    # Create a paper stub for each venue (e.g. ACL)
    for venue, venue_data in data.items():
        venue_str = venue_data["slug"]
        with open("{}/content/venues/{}.md".format(srcdir, venue_str), "w") as f:
            print("---", file=f)
            yaml_data = {"venue": venue, "title": venue_data["name"]}
            yaml.dump(yaml_data, default_flow_style=False, stream=f)
            print("---", file=f)

    print("Creating stubs for events...")
    if not check_directory("{}/content/events".format(srcdir), clean=clean):
        return
    # Create a paper stub for each event (= venue + year, e.g. ACL 2018)
    for venue, venue_data in data.items():
        venue_str = venue_data["slug"]
        for year in venue_data["volumes_by_year"]:
            with open(
                "{}/content/events/{}-{}.md".format(srcdir, venue_str, year), "w"
            ) as f:
                print("---", file=f)
                yaml_data = {
                    "venue": venue,
                    "year": year,
                    "title": "{} ({})".format(venue_data["name"], year),
                }
                yaml.dump(yaml_data, default_flow_style=False, stream=f)
                print("---", file=f)


def create_sigs(srcdir, clean=False):
    """Creates page stubs for all SIGs in the Anthology."""
    jsonfile = "{}/data/sigs.json".format(srcdir)
    #print("Processing {}".format(jsonfile))
    with open(jsonfile, "r") as f:
        data = json.loads(f.read())

    print("Creating stubs for SIGs...")
    if not check_directory("{}/content/sigs".format(srcdir), clean=clean):
        return
    # Create a paper stub for each SIGS (e.g. SIGMORPHON)
    for sig, sig_data in data.items():
        sig_str = sig_data["slug"]
        with open("{}/content/sigs/{}.md".format(srcdir, sig_str), "w") as f:
            print("---", file=f)
            yaml.dump(
                {
                    "acronym": sig,
                    "short_acronym": sig[3:] if sig.startswith("SIG") else sig,
                    "title": sig_data["name"],
                },
                default_flow_style=False,
                stream=f,
            )
            print("---", file=f)


dir_ = "/home/jan/Schreibtisch/ir-anthology/build"

create_papers(dir_, clean=True)
create_volumes(dir_, clean=True)
create_people(dir_, clean=True)
create_venues_and_events(dir_, clean=True)
create_sigs(dir_, clean=True)

