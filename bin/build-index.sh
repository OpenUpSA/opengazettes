#!/bin/bash

set -e

curl http://code4sa-gazettes.s3.amazonaws.com/archive/index/gazette-index-latest.jsonlines -O
python bin/build-index.py
jekyll build
