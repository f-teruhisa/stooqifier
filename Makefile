default:up

init:
	docker-compose build

up:
	docker-compose up

lint:
	docker-compose run --rm app pylint main.py env.py ./notifiers
