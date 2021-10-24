# -*- coding: utf-8 -*-
#
# This file has been modified by the Webis Group 
# to fit the needs of the IR Anthology. 
# The original is part of the ACL Anthology. 
#
#
# Copyright of the original file 2019 Arne Köhn <arne@chark.eu>
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

# Instructions:
# - if you edit the a command running python, make sure to
#   run . $(VENV) && python3 -- this sets up the virtual environment.
# - all targets running python somewhere should have venv as a dependency.
#   this makes sure that all required packages are installed.

SHELL = /bin/bash
ANTHOLOGYHOST := "https://ir.webis.de"
ANTHOLOGYDIR := anthology
HUGO_ENV ?= production

sourcefiles=$(shell find data -type f '(' -name "*.yaml" -o -name "*.xml" ')')
xmlstaged=$(shell git diff --staged --name-only --diff-filter=d data/xml/*.xml)
pysources=$(shell git ls-files | egrep "\.pyi?$$")
pystaged=$(shell git diff --staged --name-only  --diff-filter=d | egrep "\.pyi?$$")

timestamp=$(shell date -u +"%d %B %Y at %H:%M %Z")
githash=$(shell git rev-parse HEAD)
githashshort=$(shell git rev-parse --short HEAD)

#######################################################
# check whether the correct python version is available
ifeq (, $(shell which python3 ))
  $(error "python3 not found in $(PATH)")
endif

PYTHON_VERSION_MIN=3.7
PYTHON_VERSION=$(shell python3 -c 'import sys; print("%d.%d"% sys.version_info[0:2])' )
PYTHON_VERSION_OK=$(shell python3 -c 'import sys; print(int(float("%d.%d"% sys.version_info[0:2]) >= $(PYTHON_VERSION_MIN)))' )

ifeq ($(PYTHON_VERSION_OK),0)
  $(error "Need python $(PYTHON_VERSION_MIN), but only found python $(PYTHON_VERSION)!")
endif
# end python check
#######################################################

# hugo version check
HUGO_VERSION_MIN=58
HUGO_VERSION=$(shell hugo version | sed 's/.*Generator v0.\(..\).*/\1/')
HUGO_VERSION_TOO_LOW:=$(shell [ $(HUGO_VERSION_MIN) -gt $(HUGO_VERSION) ] && echo true)
ifeq ($(HUGO_VERSION_TOO_LOW),true)
  $(error "incorrect hugo version installed! Need hugo 0.$(HUGO_VERSION_MIN), but only found hugo 0.$(HUGO_VERSION)!")
endif


VENV := "venv/bin/activate"

.PHONY: site
site: json hugo sitemap


# Split the file sitemap into Google-ingestible chunks.
# Also build the PDF sitemap, and split it.
.PHONY: sitemap
sitemap: build/.sitemap

build/.sitemap: venv/bin/activate build/.hugo
	if ((. $(VENV) && python3 bin/split_sitemap.py build/anthology/sitemap.xml) | grep -v "no need to split"); then \
		rm -f build/anthology/sitemap_*.xml.gz; \
		gzip -9n build/anthology/sitemap_*.xml; \
		bin/create_sitemapindex.sh `ls build/anthology/ | grep 'sitemap_.*xml.gz'` > build/anthology/sitemapindex.xml; \
		touch build/.sitemap; \
	fi

.PHONY: venv
venv: venv/bin/activate

# installs dependencies if requirements.txt have been updated.
# checks whether libyaml is enabled to ensure fast build times.
venv/bin/activate: bin/requirements.txt
	test -d venv || python3 -m venv venv
	. $(VENV) && pip3 install -Ur bin/requirements.txt
	@python3 -c "from yaml import CLoader" 2> /dev/null || ( \
	    echo "WARNING     No libyaml bindings enabled for pyyaml, your build will be several times slower than needed";\
	    echo "            see the README on GitHub for more information")
	touch venv/bin/activate

.PHONY: all
all: clean check site

.PHONY: basedirs
basedirs:
	build/.basedirs
.PHONY: build/.basedirs
build/.basedirs:
	@mkdir -p build/data-export
	@mkdir -p build/content/papers
	@touch build/.basedirs

# copies all files that are not automatically generated
# and creates empty directories as needed.
.PHONY: static
static: build/.static

build/.static: build/.basedirs $(shell find hugo -type f)
	@echo "INFO     Creating and populating build directory..."
	@cp -r hugo/* build
	@echo >> build/config.toml
	@echo "[params]" >> build/config.toml
	@echo "  githash = \"${githash}\"" >> build/config.toml
	@echo "  githashshort = \"${githashshort}\"" >> build/config.toml
	@echo "  timestamp = \"${timestamp}\"" >> build/config.toml
	@perl -pi -e "s/ANTHOLOGYDIR/$(ANTHOLOGYDIR)/g" build/index.html
	@touch build/.static

.PHONY: data 
data: data/ir-anthology.bib

data/ir-anthology.bib: 
	mkdir -p data
	rm -f data/ir-anthology.bib
	cd data && wget https://raw.githubusercontent.com/ir-anthology/ir-anthology-data/master/ir-anthology.bib

.PHONY: json
json: build/.json

build/.json: data/ir-anthology.bib build/.basedirs venv/bin/activate
	rm -rf data/temp data/final
	mkdir -p build/data
	@echo "INFO     Deserialize BIBTEX file..."
	@. $(VENV) && python3 bin/bibanthology.py && python3 bin/bibanthology_to_hugo_json.py
	@touch build/.json

.PHONY: hugo_pages
hugo_pages: build/.pages

build/.pages: build/.basedirs build/.json venv/bin/activate
	@echo "INFO     Creating page templates for Hugo..."
	. $(VENV) && python3 bin/create_hugo_pages.py
	@touch build/.pages


.PHONY: hugo
hugo: build/.hugo

build/.hugo: build/.static build/.pages
	@echo "INFO     Running Hugo... this may take a while."
	@cd build && \
	    hugo -b $(ANTHOLOGYHOST)/$(ANTHOLOGYDIR) \
	         -d $(ANTHOLOGYDIR) \
		 -e $(HUGO_ENV) \
	         --cleanDestinationDir \
	         --minify
	@touch build/.hugo
	@mv data/files build/$(ANTHOLOGYDIR)/

.PHONY: clean
clean:
	rm -rf build
	rm -rf data

.PHONY: serve
serve:
	 @echo "INFO     Starting a server at http://localhost:8000/"
	 @cd build && python3 -m http.server 8000

# this target does not use ANTHOLOGYDIR because the official website
# only works if ANTHOLOGYDIR == anthology.
.PHONY: upload
upload:
	@if [[ $(ANTHOLOGYDIR) != "anthology" ]]; then \
            echo "WARNING: Can't upload because ANTHOLOGYDIR was set to '$(ANTHOLOGYDIR)' instead of 'anthology'"; \
            exit 1; \
        fi
	@echo "INFO     Running rsync..."
  # main site
	@rsync -azve ssh --delete build/anthology/ aclwebor@50.87.169.12:anthology-static
  # aclanthology.org
#	@rsync -azve ssh --delete build/anthology/ anthologizer@aclanthology.org:/var/www/html
