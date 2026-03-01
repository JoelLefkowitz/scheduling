default: format lint test

format:
    ruff format

lint:
    ruff check --fix
    mypy src tests
    trufflehog3 -c .trufflehog3.yaml --no-history

test:
    pytest
