# Makefile for Raspberry Pi Bitcoin Miner

.PHONY: help install install-dev test lint format type-check clean run

help:
	@echo "Raspberry Pi Bitcoin Miner - Available Commands:"
	@echo ""
	@echo "  make install       - Install production dependencies"
	@echo "  make install-dev   - Install development dependencies"
	@echo "  make test          - Run test suite"
	@echo "  make lint          - Run linters (flake8, pylint)"
	@echo "  make format        - Format code (black, isort)"
	@echo "  make type-check    - Run type checker (mypy)"
	@echo "  make clean         - Clean build artifacts"
	@echo "  make run           - Run the miner"
	@echo "  make coverage      - Run tests with coverage report"
	@echo ""

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

test:
	pytest

coverage:
	pytest --cov=controller --cov-report=html --cov-report=term

lint:
	flake8 controller/ tests/
	pylint controller/

format:
	black controller/ tests/
	isort controller/ tests/

type-check:
	mypy controller/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ htmlcov/ .coverage

run:
	python controller/main.py

all: format lint type-check test
