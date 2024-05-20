setup:
	python3 -m venv ./venv
	pip3 install  -r requirements.txt
	alembic upgrade head
start:
	python ./src/main.py
