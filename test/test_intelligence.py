import pandas as pd
import pytest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import intelligence

def test_find_red_pixels():
    '''
    test: 
        - tests for the length of the array returned by find_red_pixels
    '''

    print("testing find_red_pixels function", end=" ... ")
    assert len(intelligence.find_red_pixels("./data/map.png", upper_threshold=100, lower_threshold=50)) == 1140
    print("find_red_pixels Passed")

def test_find_cyan_pixels():
    '''
    test: 
        - tests for the length of the array returned by find_cyan_pixels
    '''

    print("testing find_red_pixels function", end=" ... ")
    assert len(intelligence.find_red_pixels("./data/map.png", upper_threshold=100, lower_threshold=50)) == 1140
    print("find_red_pixels Passed")

def test_detect_connected_components():
    '''
    test: 
        - tests for the length of the array returned by detect_connected_components
    '''

    print("testing detect_connected_components function", end=" ... ")
    red = intelligence.find_red_pixels("./data/map.png", upper_threshold=100, lower_threshold=50)
    assert len(intelligence.detect_connected_components(red)) == 1140
    print("detect_connected_components Passed")

def test_detect_connected_components_sorted():
    '''
    test: 
        - tests for some expected content within the dictionary with the red image
        - tests for other values expected withint the dictionary but with the cyan image
    '''

    print("testing detect_connected_components_sorted function", end=" ... ")
    red = intelligence.find_red_pixels("./data/map.png", upper_threshold=100, lower_threshold=50)
    mark = intelligence.detect_connected_components(red)
    sorted = intelligence.detect_connected_components_sorted(mark)

    assert (130, 12364) in list(intelligence.detect_connected_components_sorted(mark).items())
    assert (1, 892) in list(intelligence.detect_connected_components_sorted(mark).items())
    assert (32, 108) in list(intelligence.detect_connected_components_sorted(mark).items())
    assert (210, 4) in list(intelligence.detect_connected_components_sorted(mark).items())

    cyan = intelligence.find_cyan_pixels("./data/map.png", upper_threshold=100, lower_threshold=50)
    mark = intelligence.detect_connected_components(cyan)
    sorted = intelligence.detect_connected_components_sorted(mark)

    assert (1, 15140) in list(intelligence.detect_connected_components_sorted(mark).items())
    assert (102, 240) in list(intelligence.detect_connected_components_sorted(mark).items())
    assert (141, 32) in list(intelligence.detect_connected_components_sorted(mark).items())
    assert (210, 4) in list(intelligence.detect_connected_components_sorted(mark).items())

    print("detect_connected_components_sorted Passed")

if __name__ == "__main__":
    test_find_red_pixels()
    test_find_cyan_pixels()
    test_detect_connected_components()
    test_detect_connected_components_sorted()