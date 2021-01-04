default:up

init:
	docker-compose build

up:
	docker-compose up

lint:
	docker-compose run app pylint ./app
