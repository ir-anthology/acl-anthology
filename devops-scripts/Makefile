SHELL := /bin/bash

cache_path := $$(pwd)/.cache
root_path := $$(pwd)/..
web_path := $(cache_path)/ir-anthology.github.io
data_symlink_path := $(root_path)/data
real_data_path := $(cache_path)/real-data
example_data_path := $$(pwd)/example-data

.PHONY: quick
quick: example-data anthology local-server

.PHONY: clean
clean:
	rm -rf $(cache_path) $(data_symlink_path)
	sudo docker image rm -f ir-anthology ir-anthology-webserver ir-anthology-data-collector

.PHONY: example-data
example-data:
	rm -f $(data_symlink_path)
	ln -s $(example_data_path) $(data_symlink_path)

.PHONY: real-data
real-data: .cache/real-data-from-dump
	rm -f $(data_symlink_path)
	ln -s $(real_data_path) $(data_symlink_path)

.cache/real-data-from-dump:
	mkdir -p $(cache_path) $(real_data_path)
        cd $(cache_path) && ([ -d ir-anthology-data-collector ] || git clone https://github.com/ir-anthology/ir-anthology-data-collector.git) && (cd ir-anthology-data-collector && git pull)
        cd $(cache_path)/ir-anthology-data-collector && sudo docker build -t ir-anthology-data-collector .
        sudo docker run -it --rm --mount type=bind,source=$(real_data_path),target=/home/build-user/data ir-anthology-data-collector
	touch .cache/real-data-from-dump

.PHONY: anthology
anthology:
	[ -L $(data_symlink_path) ] || (echo "$$(tput setaf 3)you have to specify either 'example-data' or 'real-data' as a target BEFORE the target 'anthology'$$(tput setaf 7)" && exit 1)
	cd .. && sudo docker build -t ir-anthology-builder .
	mkdir -p $(cache_path)
	cd $(cache_path) && ([ -d ir-anthology.github.io ] || git clone gitgithub.com:ir-anthology/ir-anthology.github.io.git) && (cd ir-anthology.github.io && git pull && rm -rf anthology assets resources static index.html)
	sudo docker run -it --rm --mount type=bind,source=$(data_symlink_path),target=/home/build-user/ir-anthology/data --mount type=bind,source=$(web_path),target=/home/build-user/ir-anthology/build ir-anthology-builder
	sudo docker run --rm -it --mount type=bind,source=$(web_path),target=/anthology-git ubuntu:20.04 /bin/bash -c "chown -R $$UID:$$UID /anthology-git/"
	rm -f $(data_symlink_path)

.PHONY: local-server
local-server:
	cd local-webserver && sudo docker build -t ir-anthology-local-webserver .
	sudo docker run --rm --mount type=bind,source=$$(pwd)/local-webserver/nginx.site.conf,target=/etc/nginx/sites-enabled/default --mount type=bind,source=$(web_path),target=/var/www/html -p 8000:8000 ir-anthology-local-webserver

.PHONY: deploy
deploy: clean real-data anthology
	cd $(web_path) && git add -A && git commit -m "refresh build" && git push
	
