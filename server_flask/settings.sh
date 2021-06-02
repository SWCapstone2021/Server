#!/bin/bash
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export PATH=/opt/conda/bin:$PATH
pip install -U flask-cors
# export FLASK_APP=server/app
python app.py
exit 0W
