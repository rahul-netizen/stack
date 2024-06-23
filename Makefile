help:
	@echo "Available command"
	@echo "- pytest.      : Run tests "
# @echo "- format       : Format python scripts using black & isort"
# @echo "- type	      : Perform type check using mypy"
# @echo "- lint         : Lint the code using flake8"
# @echo "- secure       : Perform security vulnerabilities in files"
	@echo "- deps	      : Install required dependencies for the project"
	@echo "- ci	      	  : Perform CI steps using deps, format, type, line & secure"
	@echo "- perms        : Set rwx permission dev for all files in the project"
	@echo "- docker-spin        : Start the airlfow containers"
	@echo "- up       : Utility to  run perms and docker-spin together"
	@echo "- down       : Bring down the airflow containers"
	@echo "- restart       : Restart the airlfow containers"
	@echo "- ex       : Execute in the airflow webserver container"
	@echo "- precommit       : Execute in the airflow webserver container"


.PHONY:  ci
####################################################################################################################
# Setup containers to run Airflow

docker-spin:
				docker compose up airflow-init && docker compose up --build -d

perms:
		sudo mkdir airflow && cd airflow &&	sudo mkdir -p plugins temp dags tests migrations data visualization && sudo chmod -R u=rwx,g=rwx,o=rwx logs plugins temp dags tests migrations data visualization

up: perms docker-spin

down:
		docker compose down --volumes --rmi all

restart:
			down up

ex:
		docker exec -u root -it webserver bash

pytest:
			python3 -m pytest --log-cli-level info -p no:warnings -v ./tests



####################################################################################################################
# Testing, dependencies, auto formatting, type checks, & Lint checks

# format:
# 		python3 -m isort .
# 		python3 -m black -S .

# type:
# 		python3 -m mypy .

# lint:
# 		python3 -m flake8 .

# secure:
# 		python3 -m bandit -r .

# ci : format lint secure

deps:
		pip3 install -r ./containers/airflow/requirements.txt

precommit:
			docker exec -u root webserver git init . && pre-commit run --all-files && ls

ci	: precommit
