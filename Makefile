black:
	black .

black_check:
	black --check .

flake8:
	# stop the build if there are Python syntax errors or undefined names
	flake8 . --count --show-source --statistics --exclude=.venv,venv