#!/bin/bash
set -e
chown -R build-user:build-user /home/build-user/ir-anthology/data
chown -R build-user:build-user /home/build-user/ir-anthology/build
exec runuser -u build-user -- make