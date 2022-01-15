default:up

init:
	docker-compose build

up:
	docker-compose up

lint:
	docker-compose run --rm app pylint main.py ./notifiers ./message ./test

pytest:
	docker-compose run --rm app pytest

typehint:
	docker-compose run --rm app mypy .

pipinstall:
	docker-compose run --rm app pip install -r requirements.txt
