compose:
	docker-compose up --build

compose-daemon:
	docker-compose up --build -d

develop: compose-daemon
	docker-compose exec snacks-api /bin/bash

test: compose-daemon
	docker-compose exec snacks-api pytest --cov snacks/ tests/

clean:
	find . -name *.pyc -delete
	find . -name __pycache__ -type d -delete
	rm -rf snacks.egg-info
	rm -rf .pytest_cache
