.PHONY: install lint test run docker-build docker-run smoke clean

install:
	pip install -r requirements-dev.txt

lint:
	flake8 app.py tests

test:
	pytest --cov=app --cov-report=term-missing

run:
	FLASK_DEBUG=1 python app.py

docker-build:
	docker build -t aceest-fitness:local .

docker-run:
	docker run --rm -p 5000:5000 aceest-fitness:local

smoke:
	sh scripts/smoke_test.sh http://localhost:5000

clean:
	rm -rf .pytest_cache .coverage coverage.xml htmlcov reports
