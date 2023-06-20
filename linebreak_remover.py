import sys
import argparse
import logging

verbose = {
    0: logging.CRITICAL,
    1: logging.ERROR,
    2: logging.WARNING,
    3: logging.INFO,
    4: logging.DEBUG
    }

DEFAULT_ENCODING = 'utf-8'

def parse_arguments():
    """Read arguments from a command line."""
    parser = argparse.ArgumentParser(description='Arguments get parsed via --commands')
    # Verbosity args
    parser.add_argument('-v', metavar='verbosity', type=int, default=2,
        help='Verbosity of logging: 0 -critical, 1- error, 2 -warning, 3 -info, 4 -debug')
    # Add extra args
    parser.add_argument("-f", metavar='input path', required=False,
        help='The path of the file to be cleaned')

    args = parser.parse_args()

    return args

def is_line_broken(line):
    """Function to determine if a string has an open quote that never gets closed.
    Returns True if a string has a quote opening that is not closed afterwards.
    The logic includes a XOR operator (^) to determine if the quotes are open.
    When a new character is scanned, we determine the quote situation using the following logic:
    -------------------------------
    is_quote | quotes_open | result
    -------------------------------
    False    | False       | False
    False    | True        | True
    True     | False       | True
    True     | True        | False
    -------------------------------
    This logic mimics a XOR operator:
    https://www.techtarget.com/whatis/definition/logic-gate-AND-OR-XOR-NOT-NAND-NOR-and-XNOR?vgnextfmt=print#xor
    """
    quotes_open = False
    for char in line:
        is_quote = char == '"'
        quotes_open = quotes_open ^ is_quote
    return quotes_open

def main(_args):
    """Main function.
    Receives a csv file path as input.
    Scans the file line by line and removes line breaks by detecting lines that have an open quote
    and combining them with subsequent lines until the quote is closed.

    Return values:
    - 0: All is good
    - 1: File closed without closing a quote
    - 2: Invalid input file format
    - 3: Missing input file
    - 4: Misc error
    """
    try:
        if _args.f:
            file_path_in = _args.f
            # File format validation
            if file_path_in[-4:] != '.csv':
                msg = "Input file must be a .csv file."
                logging.error(msg)
                return 2
            # Set file path out by appending '_out' to the filename
            file_path_out = f"{file_path_in.split('.')[-2]}_out.{file_path_in.split('.')[-1]}"

            with open(file_path_in, 'r', encoding = DEFAULT_ENCODING) as file_in:
                with open(file_path_out, 'w', encoding = DEFAULT_ENCODING) as file_out:
                    # Set initial conditions
                    is_line_closed = True
                    line_out = ''
                    for line in file_in:
                        # Append current line to out buffer
                        line_out = line_out + line.replace('\n',' ')
                        if is_line_closed:
                            # If the previous line was closed, a broken line keeps the output buffer
                            # and sets the status of open line
                            if is_line_broken(line):
                                is_line_closed = False
                            # Otherwise, writes the line, minus the last space from replacing the
                            # last line break and cleans the output buffer
                            else:
                                file_out.write(f'{line_out[:-1]}\n')
                                line_out = ''
                        else:
                            # If the previous line was open, a broken line means that the quote is
                            # closed in this line. Writes the line, cleans the output buffer and
                            # sets the status of closed line
                            if is_line_broken(line):
                                file_out.write(f'{line_out[:-1]}\n')
                                is_line_closed = True
                                line_out = ''
                            # Otherwise, the quote is still open, so it continues with the next line
                            else:
                                continue

            if is_line_closed:
                msg = f'Process completed. Out file in {file_path_out}'
                logging.info(msg)
                return 0
            else:
                msg = 'File closed without closing a quote. Review file'
                logging.warning(msg)
                return 1

        else:
            msg = """There needs to be an input file.\n
                Please, include the file path after the flag -f\n
                python linebreak_remover.py -f <path_to_file>"""
            logging.error(msg)
            return 3

    # Catch generic exceptions
    # TODO: Branch into more specific exceptions
    except Exception as ex:
        logging.error(ex)
        return 4

if __name__ == "__main__":
    argms = parse_arguments()
    logging.basicConfig(level=verbose[argms.v], stream=sys.stdout)
    main(argms)
