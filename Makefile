PY = venv/bin/pypy3
PIP = venv/bin/pip
VENV_DIR = venv

.PHONY: run activate freeze install clean build pre-push test

run: install
	$(PY) main.py

activate: $(VENV_DIR)/bin/activate

$(VENV_DIR)/bin/activate:
	pypy3 -m ensurepip
	pypy3 -m venv $(VENV_DIR)
	touch $@

install: activate requirements.txt
	$(PIP) install -r requirements.txt --no-cache-dir
	cd http_client && ../$(PY) setup.py build && ../$(PY) setup.py install

freeze: activate
	$(PIP) freeze > requirements.txt

clean:
	$(PY) http_client/setup.py clean
	$(PIP) uninstall -y -r requirements.txt
	rm -rf __pycache__ **/__pycache__ $(VENV_DIR) dist build **/*.pyc **/*.so

re: clean run

pre-push: clean freeze
