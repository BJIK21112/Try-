# X-Bot Development Makefile
# Professional development workflow commands

.PHONY: help install install-dev test test-cov lint format type-check security clean build deploy all

# Default target
help:
	@echo "X-Bot Development Commands"
	@echo "=========================="
	@echo ""
	@echo "Installation:"
	@echo "  install       Install production dependencies"
	@echo "  install-dev   Install development dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  test          Run all tests"
	@echo "  test-cov      Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint          Run flake8 linting"
	@echo "  format        Format code with black and isort"
	@echo "  type-check    Run mypy type checking"
	@echo "  security      Run security checks"
	@echo ""
	@echo "Development:"
	@echo "  clean         Clean up cache files"
	@echo "  build         Build Docker image"
	@echo "  deploy        Deploy to Cloud Run"
	@echo ""
	@echo "Combined:"
	@echo "  all           Run full quality check (format, lint, type-check, test)"

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt -r requirements-dev.txt

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=src --cov-report=html --cov-report=term-missing

# Code Quality
lint:
	flake8 src/ tests/

format:
	black src/ tests/
	isort src/ tests/

type-check:
	mypy src/

security:
	bandit -r src/
	safety check

# Development
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -delete
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

build:
	docker build -t gcr.io/sublime-lodge-472322-m2/x-bot:latest .

deploy:
	docker push gcr.io/sublime-lodge-472322-m2/x-bot:latest
	gcloud run deploy x-bot --image gcr.io/sublime-lodge-472322-m2/x-bot:latest --platform managed --region us-central1 --allow-unauthenticated

# Combined quality check
all: format lint type-check test

# Setup development environment
setup: install-dev
	pre-commit install
	@echo "Development environment setup complete!"
	@echo "Run 'make all' to verify everything works"

# CI/CD simulation
ci: clean all security build