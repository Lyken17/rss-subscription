#!/bin/bash

set -e 
python download_rss.py
python llm_parse.py || true
python main.py
