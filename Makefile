.PHONY: prerequisites install dev lint build test start clean purge

# This Makefile should provide you with a simple way to get your dev
# environment up and running. It will install all the dependencies
# needed to run the project, and then run the project.

prerequisites:
	# Make sure to have micromamba installed - a fast conda/mamba implementation with very low overhead.
	# This will allow you to create a new environment with all the dependencies needed for this project.
	# Conda environments also contain dedicated python interpreters that won't mess up your local python installation."

install:
	pre-commit install
	micromamba create -f environment.yml  # Create a new environment
	micromamba activate parma-analytics  # Activate the new environment
	pip install -e . # Install the project in editable mode

dev:


lint:
	pre-commit run --all-files

build:

test: lint

start:

clean:
	rm -rf .mypycache

purge: clean
