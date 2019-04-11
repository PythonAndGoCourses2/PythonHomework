.DEFAULT_GOAL := run

PROGRAMM_NAME := pycalc
SRC_FOLDER := $(PROGRAMM_NAME)


install-dev:
	@echo "Installing in the development mode..."
	pip3 install --editable .

uninstall-dev:
	@echo "Uninstalling calc..."
	pip3 uninstall $(PROGRAMM_NAME) -y

run:
	python3 -m $(SRC_FOLDER)