#!/usr/bin/env bash

python3 -m venv env &&
source env/bin/activate && pip3 install wheel && pip3 install -r requirements.txt && pip3 install pyedflib==0.1.17