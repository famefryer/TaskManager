setup:
	python3 -m venv ./venv
	pip3 install  -r requirements.txt
	alembic upgrade head
tear_down:
	alembic downgrade base
start:
	python ./src/main.py
