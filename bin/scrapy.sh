#! /bin/sh
#
# scrapy.sh
# Copyright (C) 2022 wanghuacheng <wanghuacheng@wanghuacheng-PC>
#
# Distributed under terms of the MIT license.
#

BIN=$(dirname $0)
APP_DIR=$(cd $BIN/..;pwd)
export PYTHONPATH=$APP_DIR/python


scrapy crawl mxdlk -o $APP_DIR/tmp/url.jsonlines
scrapy crawl summary -a url_json=$APP_DIR/tmp/url.jsonlines -a data_dir=$APP_DIR/data
