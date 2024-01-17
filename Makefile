.PHONY: prerequisites install dev test purge-db purge

# This Makefile should provide you with a simple way to get your dev
# environment up and running. It will install all the dependencies
# needed to run the project, and then run the project.

prerequisites:
	# Make sure to have micromamba installed - a fast conda/mamba implementation with very low overhead.
	# This will allow you to create a new environment with all the dependencies needed for this project.
	# Conda environments also contain dedicated python interpreters that won't mess up your local python installation."

install:
	micromamba create -f environment.yml  # Create a new environment

dev:
	uvicorn parma_analytics.api:app --reload

test:
	PYTHONPATH=. pytest tests/
	coverage html && open htmlcov/index.html

purge-db:
	docker-compose down
	rm -rf .data

purge: purge-db
	rm -rf .mypy_cache .pytest_cache .coverage .eggs
