#!/bin/bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
export PATH=/usr/local/bin:$PATH\
# brew install python\
apt-get install python
# export PATH=/usr/local/share/python:$PATH\
# easy_install pip
apt-get install python-pip
pip install -r requirements.txt

