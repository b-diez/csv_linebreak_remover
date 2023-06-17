import sys
import os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/..')

from linebreak_remover import is_line_broken

def test_line_with_no_quotes():
    line_in = 'El perro de san roque no tiene rabo'
    expected_output = False
    assert is_line_broken(line_in) == expected_output

def test_line_with_1_quote():
    line_in = 'El perro de "san roque no tiene rabo'
    expected_output = True
    assert is_line_broken(line_in) == expected_output

def test_line_with_2_quotes():
    line_in = 'El perro de "san roque" no tiene rabo'
    expected_output = False
    assert is_line_broken(line_in) == expected_output