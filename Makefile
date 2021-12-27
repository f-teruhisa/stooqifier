default:up

init:
	docker-compose build

up:
	docker-compose up

lint:
	docker-compose run --rm app pylint main.py ./notifiers ./message/message.py ./test

pytest:
	docker-compose run --rm app pytest
