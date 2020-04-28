#!/usr/bin/env bash

python3 -m venv venv
source venv/bin/activate && pip install wheel && pip install -r requirements.txt && pip install pyedflib==0.1.17