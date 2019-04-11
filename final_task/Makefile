.DEFAULT_GOAL := run

PROGRAMM_NAME := pycalc
SRC_FOLDER := $(PROGRAMM_NAME)
INSTALLED_EXECUTABLE_DIR := ~/.local/bin

PYTHON := python3

PIP := pip3
PIP_LOCAL := --user

run:
	$(INSTALLED_EXECUTABLE_DIR)/$(PROGRAMM_NAME)

run-source:
	$(PYTHON) -m $(SRC_FOLDER)

install:
	@echo "Installing..."
	$(PIP) install $(PIP_LOCAL) .

install-dev:
	@echo "Installing in the development mode..."
	$(PIP) install $(PIP_LOCAL) --editable .

uninstall:
	@echo "Uninstalling..."
	$(PIP) uninstall $(PROGRAMM_NAME) -y

show:
	$(PIP) show $(PROGRAMM_NAME)

pycodestyle:
	pycodestyle $(PROGRAMM_NAME)/*
