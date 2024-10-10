PYPY = venv/bin/pypy3
PIP = venv/bin/pip3

.PHONY: run activate freeze install clean build pre-push

run: install
	$(PYPY) main.py

activate: venv/bin/activate

venv/bin/activate:
	pypy3 -m venv venv
	touch $@

install: activate requirements.txt
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

freeze: activate
	$(PIP) freeze > requirements.txt

clean:
	rm -rf __pycache__ **/__pycache__ venv dist build RequestiPy.exe

pre-push: clean freeze
