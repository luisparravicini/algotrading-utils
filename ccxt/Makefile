install-deps:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

docker-build:
	docker build -t algotrading-utils/updater .

docker-run:
	if [ ! -d data ]; then mkdir data; fi
	docker run -ti -v`pwd`/data:/app/data algotrading-utils/updater
