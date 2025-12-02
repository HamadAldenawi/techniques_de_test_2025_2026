test:
	pytest -q

unit_test:
	pytest -q --disable-warnings --maxfail=1 -k "not performance"

perf_test:
	pytest -q -m performance

coverage:
	coverage run -m pytest
	coverage report

lint:
	ruff check

doc:
	pdoc3 --html TP -o docs
