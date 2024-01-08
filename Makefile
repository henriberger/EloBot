MAX_LINE_LENGTH = 120

black:
	@black . --line-length $(MAX_LINE_LENGTH)

isort:
	@isort . --line-length $(MAX_LINE_LENGTH)

flake8:
	@flake8 . --exclude venv/,testing/memory_profiling/ --max-line-length $(MAX_LINE_LENGTH) --ignore=E203,W503

format:
	@make black
	@make isort
	@make flake8

pip-req:
	@pip3 freeze > setup/requirements.txt

pip-install:
	@pip3 install -r setup/requirements.txt
