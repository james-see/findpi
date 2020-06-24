all: clean build deploy
.PHONY: all

build:
	@python3 setup.py sdist bdist_wheel
deploy:
	twine upload dist/*
clean:
	@rm -rf dist build findpi.egg-info
