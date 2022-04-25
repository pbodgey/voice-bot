SRC = voice_bot
PY = python
VENV = pipenv

.PHONY: run setup-venv shell

run:
	$(VENV) run $(PY) $(SRC)/bot.py

setup-venv:
	$(PIP) install $(VENV)
	$(VENV) install

shell:
	$(VENV) shell
