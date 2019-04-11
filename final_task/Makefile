.DEFAULT_GOAL := run

PROGRAMM_NAME := pycalc
SRC_FOLDER := $(PROGRAMM_NAME)
INSTALLED_EXECUTABLE_PATH := ~/.local/bin

PIP_LOCAL := --user

run:
	$(INSTALLED_EXECUTABLE_PATH)/$(PROGRAMM_NAME)


# run from the source folder
run-source:
	python3 -m $(SRC_FOLDER)

# locally
install:
	@echo "Installing..."
	pip3 install $(PIP_LOCAL) .

install-dev:
	@echo "Installing in the development mode..."
	pip3 install $(PIP_LOCAL) --editable .

uninstall:
	@echo "Uninstalling..."
	pip3 uninstall $(PROGRAMM_NAME) -y

show:
	pip3 show $(PROGRAMM_NAME)
