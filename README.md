# Readme

Line break remover is a python script that takes a csv file and removes line breaks inside quoted fields. It receives a csv file path as input, scans the file line by line, and removes line breaks by detecting lines that have an open quote and combining them with subsequent lines until the quote is closed.

## Usage

Clone the repo, open a terminal in the repo directory and invoke the script:

```shell
python linebreak_remover.py -f <path_to_input_file>
```

The output file will be created in the same directory as the original file with an appended '_out'.

You can select the logging level with the flag -v and a number, where:

- 0: logging.CRITICAL
- 1: logging.ERROR
- 2: logging.WARNING
- 3: logging.INFO
- 4: logging.DEBUG

## Known issues

- Unit tests are not working properly.
- Exception handling is generic.