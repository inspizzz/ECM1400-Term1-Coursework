import pytest
import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import utils

def test_sumValues():
    '''
    purpose:
        - test the sumValues function

    arguments:
        - none

    returns:
        - none
    '''

    # test the function given some lists of values and check the output is correct
    assert utils.sumValues([1, 2, 3]) == 6
    assert utils.sumValues([1, 2, 3, 4, 5]) == 15
    assert utils.sumValues([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == 55

def test_maxValue():
    '''
    purpose:
        - test the maxValue function

    arguments:
        - none

    returns:
        - none
    '''

    # test the function given some lists of values and check the output is correct
    assert utils.maxValue([1, 2, 3]) == 3
    assert utils.maxValue([1, 2, 3, 4, 5]) == 5
    assert utils.maxValue([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == 10

def test_minValue():
    '''
    purpose:
        - test the minValue function

    arguments:
        - none

    returns:
        - none
    '''

    # test the function given some lists of values and check the output is correct
    assert utils.minValue([1, 2, 3]) == 1
    assert utils.minValue([-11, 2, 3, 4, 5]) == -11
    assert utils.minValue([1, 2, 3, 4, 0, 6, 7, 8, 9, 10]) == 0

def test_meanValue():
    '''
    purpose:
        - test the meanValue function

    arguments:
        - none

    returns:
        - none
    '''

    # test the function given some lists of values and check the output is correct
    assert utils.meanValue([1, 2, 3]) == 2
    assert utils.meanValue([1, 2, 3, 4, 5]) == 3
    assert utils.meanValue([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == 5.5

def test_countValue():
    '''
    purpose:
        - test the countValue function

    arguments:
        - none

    returns:
        - none
    '''

    # test the function given some lists of values and check the output is correct
    assert utils.countValue("wrwrwrrwr", "wr") == 4 
    assert utils.countValue("hello world", "o") == 2
    assert utils.countValue("this is a sentence", " ") == 3