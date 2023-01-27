.ONESHELL:
.DEFAULT_GOAL:= run
PYTHON= ./venv/bin/python3
PIP= ./venv/bin/pip

venv/bin/activate: requirements.txt
	python -m venv venv
	chmod +x venv/bin/activate
	. ./venv/bin/activate
	$(PIP) install -r requirements.txt
	$(PYTHON) -m spacy download fr_core_news_md

venv: venv/bin/activate
	. ./venv/bin/activate

run: venv
	$(PYTHON) app/main.py

clean:
	rm -rf app/__pycache__
	rm -rf venv

.PHONY: run clean