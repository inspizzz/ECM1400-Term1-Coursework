
import pytest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import monitoring

# instances of classes in case the function tested is using more than one function inside of the class

net = monitoring.NeuralNet2(arch={}, training=[], labeled=[])
disp = monitoring.Display()


def test_translate():
	'''
	purpose:
		- test the translate function

	arguments:
		- None

	returns:
		- None
	'''

	# test the function
	assert disp.translate(10, 0, 100, 0, 1000) == 100


def test_Sigmoid():
	'''
	purpose:
		- test the Sigmoid function

	arguments:
		- None

	returns:
		- None
	'''

	# test the function
	assert net.Sigmoid(0) == 0.5


def test_Sigmoid_derivative():
	'''
	purpose:
		- test the Sigmoid_derivative function

	arguments:
		- None

	returns:
		- None
	'''

	# test the function
	assert net.Sigmoid_derivative(x=0) == 0.25


def test_ReLu():
	'''
	purpose:
		- test the ReLu function

	arguments:
		- None

	returns:
		- None
	'''

	# test the function
	assert net.ReLu(0) == 0

def test_ReLu_deriv():
	'''
	purpose:
		- test the ReLu_deriv function

	arguments:
		- None

	returns:
		- None
	'''
	assert net.ReLu_deriv(0) == 0

def test_cost_function():
	'''
	purpose:
		- test the cost_function function

	arguments:

	returns:
		- None
	'''

	# test the function
	assert net.cost_function([0], [0]) == 0

def test_cost_function_deriv():
	'''
	purpose:
		- test the cost_function_deriv function

	arguments:
		- None

	returns:
		- None
	'''

	# test the function
	assert net.cost_function_deriv([0], [0]) == 0

def test_predict():
	pass # cannot test without training network

def test_get_live_data_from_api():
	'''
	purpose:
		- test the get_live_data_from_api function

	arguments:
		- None

	returns:
		-None
	'''

	# test the function
	assert type(monitoring.get_live_data_from_api()) == dict

def test_getSpecies():
	'''
	purpose:
		- test the getSpecies function

	arguments:
		- None

	returns:
		-None
	'''

	# test the function
	assert type(monitoring.getSpecies()) == dict

def test_getAllSites():
	'''
	purpose:
		- test the getAllSites function

	arguments:
		- None

	returns:
		-None
	'''

	# test the function
	assert type(monitoring.getAllSites()) == list

def test_getAllData():
	'''
	purpose:
		- test the getAllData function

	arguments:
		- None

	returns:
		-None
	'''

	# test the function
	assert type(monitoring.getAllData(species_code="NO2", days=1)) == list

def test_getCoordsAndData():
	'''
	purpose:
		- test the getCoordsAndData function

	arguments:
		- None

	returns:
		-None
	'''

	# test the function
	assert type(monitoring.getCoordsAndData(species="NO2", days=1)) == tuple

