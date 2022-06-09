# define the name of the virtual environment directory
VENV := venv

# default target, when make executed without arguments
all: venv

# venv python 3.8
venv: 
	python3.8 -m venv $(VENV)

run: venv
	./$(VENV)/bin/python3 main.py $(token_file_path) $(grammar_file_path) $(code_file_path) $(output_path)

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

.PHONY: all venv run clean
