#!/bin/bash

set -e 
python download_rss.py
# python llm_parse.py
python main.py
