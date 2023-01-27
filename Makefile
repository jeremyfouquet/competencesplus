.ONESHELL:
.DEFAULT_GOAL:= run
P3 = python3
PYTHON= ./venv/bin/python3
PIP= ./venv/bin/pip

venv/bin/activate: requirements.txt
	$(P3) -m venv venv
	chmod +x venv/bin/activate
	. ./venv/bin/activate
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PYTHON) -m spacy download fr_core_news_md

venv: venv/bin/activate
	. ./venv/bin/activate

run: venv
	$(PYTHON) app/main.py

clean:
	rm -rf app/__pycache__
	rm -rf venv

linux_packages:
	sudo apt-get install python3-tk
	sudo apt-get install python3-venv

.PHONY: run clean