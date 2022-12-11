import tkinter as tk
import json
import requests
import datetime
import numpy as np
import matplotlib.pyplot as plt
import threading

class Display(tk.Tk): # done
	'''
	purpose:
		- tkinter class that provides functions
		- displays data on a map
		- displays data on a graph
	'''

	def __init__(self) -> None:
		'''
		purpose:
			- initialise the tkinter class
			- declare variables
			- create the tkinter window

		arguments:
			- None

		returns:
			- None
		'''

		# initialise the tkinter class
		super().__init__()

		# set variables
		self.WIDTH = 400
		self.HEIGHT = 400

		# create the tkinter window
		self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
		self.title("display")
		self.protocol("WM_DELETE_WINDOW", self.close)

		# set more variables
		self.running = True
		self.axis = False
		self.map = False

		self.points = []
		self.lines = []
		self.xRange = [50, self.WIDTH-50]
		self.yRange = [self.HEIGHT-100, 50]

		self.bottomLeft = [-0.534210, 51.272226] # bottom left coordinates of the map
		self.bottomRight = [0.291138, 51.717670] # bottom right coordinates of the map

		self.circles = []


	## ----------------------------------------------------
	## ----------------------- AXIS -----------------------
	## ----------------------------------------------------
	def showAxis(self) -> None:
		'''
		purpose:
			- configure the axis frame and show
			- create two frames, one for the menu and one for the graph
			- add a canvas to each frame
			- display the menu on one canvas and the graph on the other

		arguments:
			- self

		returns:
			- None
		'''

		self.axis = True

		# create the axis frame
		self.axisFrame = tk.Frame(self, width=self.WIDTH, height=self.HEIGHT-100)
		self.axisFrame.pack(side="top", fill="both", expand=True)
		self.axisFrame.bind("<Configure>", self.configureAxis)

		# create the menu frame
		self.menuFrame = tk.Frame(self, width=self.WIDTH, height=100)
		self.menuFrame.pack(side="bottom", fill="x")
		self.menuFrame.bind("<Configure>", self.configureMenu)

		# create the axis canvas
		self.axisCanvas = tk.Canvas(self.axisFrame, width=self.WIDTH, height=self.HEIGHT-100)
		self.axisCanvas.pack(side="top", fill="both", expand=True)

		# create the menu canvas
		self.menuCanvas = tk.Canvas(self.menuFrame, width=self.WIDTH, height=100)
		self.menuCanvas.pack(side="bottom", fill="both", expand=True)

		# create the axis
		self.x_axis = self.axisCanvas.create_line(50, self.HEIGHT-50, self.WIDTH-50, self.HEIGHT-50, fill="black", width=2)
		self.y_axis = self.axisCanvas.create_line(50, self.HEIGHT-50, 50, 50, fill="black", width=2)

		# create the menu
		self.site = tk.Text(self.menuCanvas, width=10, height=1)
		self.site.place(x=10, y=10)
		
		self.species = tk.Text(self.menuCanvas, width=10, height=1)
		self.species.place(x=110, y=10)
		
		self.submitButton = tk.Button(self.menuCanvas, width=3, height=1, relief=tk.SOLID, text="submit", command=self.submit)
		self.submitButton.place(x=210, y=10)

		self.clearButton = tk.Button(self.menuCanvas, width=3, height=1, relief=tk.SOLID, text="clear", command=self.clear)
		self.clearButton.place(x=310, y=10)

		self.axisCanvas.update()
		self.clear()

	def configureAxis(self, event) -> None:
		'''
		purpose:
			- when the axis frame is resized, update the axis
			- update the axis coordinates

		arguments:
			- self
			- event: a tkinter event that describes the window resize in terms of x and y variables

		returns:
			- None
		'''

		# if the axis is currently being dispayed
		if self.axis:

			# update variables and adjust the coordinates of axis
			self.WIDTH = event.width + event.x
			self.HEIGHT = event.height + event.y

			self.axisCanvas.coords(self.x_axis, 50, self.HEIGHT-50, self.WIDTH-50, self.HEIGHT-50)
			self.axisCanvas.coords(self.y_axis, 50, self.HEIGHT-50, 50, 50)

			prev_xRange = self.xRange
			prev_yRange = self.yRange
			
			self.xRange = [50, self.WIDTH-50]
			self.yRange = [self.HEIGHT-50, 50]


			# update the pixels
			for i in range(len(self.points)):
				x, y = self.points[i]
				newX = self.translate(x, prev_xRange[0], prev_xRange[1], self.xRange[0], self.xRange[1])
				newY = self.translate(y, prev_yRange[0], prev_yRange[1], self.yRange[0], self.yRange[1])
				self.points[i] = (newX, newY)

			# update the lines
			for i in range(len(self.lines)):
				self.axisCanvas.coords(self.lines[i], self.points[i][0], self.points[i][1], self.points[i+1][0], self.points[i+1][1])

	def configureMenu(self, event) -> None:
		'''
		purpose:
			- when the menu frame is resized, update the menu
			- update the menu coordinates
		
		arguments:
			- self
			- event: a tkinter event that describes the window resize in terms of x and y variables

		returns:
			- None
		'''

		# if axis is showing
		if self.axis:
			# update the width and height of the window
			self.WIDTH = event.width + event.x
			self.HEIGHT = event.height + event.y

	def addPoint(self, point:tuple, color:str="black") -> None:
		'''
		purpose:
			- add a point to the graph

		arguments:
			- self
			- point: a tuple of the form (x, y) that represents the point to be added
			- color: the color of the point

		returns:
			- None
		'''
		# if axis is showing
		if self.axis:
			
			# unpack point and add a line to the graph
			x, y = point
			self.axisCanvas.update()
			thing = self.axisCanvas.create_line(self.points[-1][0], self.points[-1][1], 50 + x, self.axisCanvas.winfo_height() - 50 - y, fill=color, width=1) # create a line from the last point to the new one
			self.points.append((50 + x, self.axisCanvas.winfo_height() - 50 - y))
			self.lines.append(thing)

	def submit(self) -> None:
		'''
		purpose:
			- get the data from the site and species text boxes
			- get the data from the api
			- add the data to the graph

		arguments:
			- self
		
		returns:
			- None
		'''

		# get species data
		speciesData = getSpecies()

		# grab the site and species from the text boxes
		site = self.site.get(1.0, tk.END).rstrip()
		species = self.species.get(1.0, tk.END).rstrip()

		# if site and species are valid
		if site in list(speciesData.keys()):
			if species in speciesData[site]:

				# get the data for that specific site and species
				data = get_live_data_from_api(site_code=site, species_code=species, start_date="2022-11-28", end_date="2022-11-29")

				# iterate for every data value
				for i in data["RawAQData"]["Data"]:

					# check if not empty
					if i["@Value"] != "":

						# unpack and add the point to the graph
						date = int(i["@MeasurementDateGMT"].split(" ")[1].split(":")[0])
						value = int(float(i["@Value"]))

						date = self.translate(date, 0, 24, 0, self.axisCanvas.winfo_width() - 100)
						value = self.translate(value, 0, 100, 0, self.axisCanvas.winfo_height() - 100)

						self.addPoint((date, value), color="black")

	def clear(self) -> None:
		'''
		purpose:
			- clear the graph
			- gets all the points in the points variable and deletes them
			- resets the line variable to an empty list
			
		arguments:
			- self

		returns:
			- None
		'''

		# reset the points to the origin of the graph
		self.points = [(50, self.axisCanvas.winfo_height() - 50)]

		# for every line delete it 
		for i in self.lines:
			self.axisCanvas.delete(i)
		
		# reset the lines variable
		self.lines = []

	def closeAxis(self) -> None:
		'''
		purpose:
			- close the axis
			- forget the axis canvas, hiding it from view from the user

		arguments:
			- self
		
		returns:
			- None
		'''

		# forget both canvases
		self.axisCanvas.pack_forget()
		self.menuCanvas.pack_forget()

		# set axis to false so that program knows that the axis is no longer being shown to the user
		self.axis = False


	## --------------------------------------------------
	## ----------------------- MAP -----------------------
	## ---------------------------------------------------
	def showMap(self) -> None:
		'''
		purpose:
			- show the map
			- create two frames with one canvas in each frame
			- one canvas for the menu and the other for the map
			- pack them showing the map and menu to the user
			
		arguments:
			- self
		
		returns:
			- None
		'''

		self.map = True

		# get the image 
		self.image = tk.PhotoImage(file="data/london.gif")
		
		# set the width and height based on the image 
		self.WIDTH = self.image.width()
		self.HEIGHT = self.image.height() + 100
		self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

		# create all widgets assosciated with the map
		self.mapFrame = tk.Frame(self, width=self.WIDTH, height=self.HEIGHT-100)
		self.mapFrame.pack(side="top", fill="both", expand=True)
		self.mapFrame.bind("<Configure>", self.configureMap)

		self.mapMenuFrame = tk.Frame(self, width=self.WIDTH, height=100	)
		self.mapMenuFrame.pack(side="bottom", fill="both", expand=True)

		self.mapCanvas = tk.Canvas(self.mapFrame, width=self.WIDTH, height=self.HEIGHT-100)
		self.imageId = self.mapCanvas.create_image(0, 0, anchor=tk.NW, image=self.image)
		self.mapCanvas.pack(side="top", fill="both", expand=True)

		self.mapSpecies = tk.Text(self.mapMenuFrame, width=10, height=1)
		self.mapSpecies.place(x=50, y=40)

		self.mapDays = tk.Text(self.mapMenuFrame, width=10, height=1)
		self.mapDays.place(x=150, y=40)

		self.mapSubmitButton = tk.Button(self.mapMenuFrame, width=5, height=1, relief=tk.SOLID, command=self.mapSubmit, text="Submit")
		self.mapSubmitButton.place(x=250, y=40)

		self.mapClearButton = tk.Button(self.mapMenuFrame, width=5, height=1, relief=tk.SOLID, command=self.mapClear, text="Clear")
		self.mapClearButton.place(x=350, y=40)

	def configureMap(self, event) -> None:
		'''
		purpose:
			- when the map is resized, this function is called
			- attempts to resize the map to the new window size
			- does not work as for some reason the reutuned image does not display after updating it

		arguments:
			- self
			- event: the event that triggered this function

		returns:
			- None
		'''
		
		# img = self.image.zoom(1, 1)
		# img = self.image.subsample(1, 1)

		# img = self.image.zoom(25) #with 250, I ended up running out of memory
		# img = img.subsample(32) #mechanically, here it is adjusted to 32 instead of 320
		

		# self.mapCanvas.itemconfig(self.imageId, image=img)
		pass

	def mapSubmit(self) -> None:
		'''
		purpose:
			- get the species and the days from the text boxes
			- checks if the species is valid
			- get all data and the coordinates as dictionaries
			- for every coordinate convert it to x and y coordinates
			- draw a circle at that location

		arguments:
			- self

		returns:
			- None
		'''

		try:
			# get the species and the days
			species = self.mapSpecies.get(1.0, tk.END).rstrip()
			days = int(self.mapDays.get(1.0, tk.END).rstrip())

			# check if species is valid
			if species not in self.species:
				return

			# get the data and coords
			data, locations = getCoordsAndData(species=species, days=days)

			# iterate over the data
			for key, value in zip(list(data.keys()), list(data.values())):
				# get the latitude and longitude
				lat, lon = locations[key]
				# convert to x and y coordinates
				x, y = self.coordToXY(float(lat), float(lon))
				# draw a circe at that location
				self.addCircle(x, y, color="black", size=value)
		except:
			print("error caught")
		
	def mapClear(self) -> None:
		'''
		purpose:
			- for every circle in the map, remove it from the map
			- reset the circles variable to an empty list

		arguments:
			- self
		
		returns:
			- None
		'''

		# remove all circles from map
		for i in self.circles:
			self.mapCanvas.delete(i)

		# reset circles to empty list
		self.circles = []
	
	def coordToXY(self, lat:float, lon:float) -> tuple:
		'''
		purpose:
			- convert the latitude and longitude to x and y coordinates

		arguments:
			- self
			- lat: the latitude
			- lon: the longitude

		returns:
			- x: the x coordinate
			- y: the y coordinate
		'''

		# calculate the difference between the bottom left and bottom right
		latDif = abs(self.bottomLeft[0] - self.bottomRight[0])
		lonDif = abs(self.bottomLeft[1] - self.bottomRight[1])
		
		lat = lat - self.bottomLeft[0]
		lon = lon - self.bottomLeft[1]

		# scale the coordinates to fit the map
		x = self.translate(lat, 0, latDif, 0, self.WIDTH)
		y = self.translate(lon, 0, lonDif, 0, self.HEIGHT)

		return x, y

	def addCircle(self, x:str, y:str, size:int=3, color:str="black") -> None:
		'''
		purpose:
			- add a circle to the map
			- add the circles id to the list for future use

		arguments:
			- self
			- x: the x coordinate
			- y: the y coordinate
			- size: the size of the circle
			- color: the color of the circle
		
		returns:
			- None
		'''

		# add circle to map and also remember the id
		a = self.mapCanvas.create_oval(x, y, x+size, y+size, fill=color)
		self.circles.append(a)

	def closeMap(self) -> None:
		'''
		purpose:
			- hide the map from the user
			- set the map variable to false, so program knows that the map is not being displayed
		
		arguments:
			- self

		returns:
			- None
		'''

		# forget the widgets
		self.mapFrame.pack_forget()
		self.mapMenuFrame.pack_forget()
		self.mapCanvas.pack_forget()
		self.mapCanvas.pack_forget()
		self.mapSpecies.place_forget()
		self.mapDays.place_forget()
		self.mapSubmitButton.place_forget()
		self.mapClearButton.place_forget()

		# set map to false so that the program knows that the map is not being displayed anymore
		self.map = False

	def translate(self, value, leftMin, leftMax, rightMin, rightMax) -> float:
		'''
		purpose:
			- convert a value from one range to another

		arguments:
			- self
			- value: the value to convert
			- leftMin: the minimum value of the left range
			- leftMax: the maximum value of the left range
			- rightMin: the minimum value of the right range
			- rightMax: the maximum value of the right range

		returns:
			- the value converted to the right range
		'''

		try:
			# Figure out how 'wide' each range is
			leftSpan = leftMax - leftMin
			rightSpan = rightMax - rightMin

			# Convert the left range into a 0-1 range (float)
			valueScaled = float(value - leftMin) / float(leftSpan)

			# Convert the 0-1 range into a value in the right range.
			return rightMin + (valueScaled * rightSpan)
		except:
			return 0

	def close(self) -> None:
		'''
		purpose:
			- upon closing the window the function is called
			- stop the while loop from executing by changing the running variable to false

		arguments:
			- self
		
		returns:
			- None
		'''

		# set running to false so that the while loop stops executing
		self.running = False

	def Update(self) -> None:
		'''
		purpose:
			- update the window

		arguments:
			- self
		
		returns:
			- None
		'''

		# while the window is not closed (running is true)
		while self.running:
			# update the window
			self.update()
			self.update_idletasks()


class Graph: # done
	'''
	purpose:
		- create a graph for the neural network progress to be displayed on
	'''

	def __init__(self) -> None:
		'''
		purpose:
			- initialize the graph in interactive mode
			- figures will be shown upon creation

		arguments:
			- self

		returns:
			- None
		'''

		# initialize graph in interactive mode
		plt.ion()

		# allow up to 1000 points to be displayed on the graph
		self.accuracy = 1000
		self.counter = 0
		self.points = [2]*self.accuracy

		# plots all unused points higher above to graph so they dont have to be shown to the user
		self.graph, = plt.plot(np.linspace(0, 1, self.accuracy))

	def add(self, y) -> None:
		'''
		
		purpose:
			- add a point to the graph

		arguments:
			- self
			- y: the y coordinate of the point

		returns:
			- None
		'''

		# set the y value and add it to the graph
		self.points[self.counter] = y
		self.graph.set_ydata(self.points)

		# draw and pause
		plt.draw()
		plt.pause(0.00001)

		# increase the counter ready for the next point
		self.counter += 1
		if self.counter >= self.accuracy:
			self.counter = 0


class NeuralNet2: # done
	'''
	wiktors neural network class
	coded completely from sratch using just elementary classes
	aimed to create a neural network that doesnt use the cheats of keras or tensorflow
	aimed to also understand how neural networks work
	completely adjustable neural network that can be used for most purposes
	it isnt optimized, only optimized are the matrix operations performed by numpy

	purpose:
		- create a neural network with the given architecture
		- train the neural network with the given data
		- test the neural network with the given data
		- save the neural network
		- load the neural network

	'''

	def __init__(self, arch:dict, training:list, labeled:list, weight_learning_rate:float=0.05, bias_learning_rate:float=0.05, display_update:int=1000,
				 epochs:int=1) -> None:
		'''
		purpose:
			- create weight and bias matrices, using random initialisation
			- create a drop layer with each layer having a percentage of inactive neurons, currently 10% are inactive
			- create local variables of the data and learning rates and more
			- initialise the graph

		arguments:
			- self
			- arch: the architecture of the neural network
			- training: the training data
			- labeled: the expected outcome data
			- weight_learning_rate: how much to adjust the weights each backward propagation
			- bias_learning_rate: the learning rate for the biases
			- display_update: how often the graph should update
			- epochs: how many times the neural network should train
		
		returns:
			- None
		'''

		# unpack the architecture
		self.layer_names = []
		self.layer_sizes = []

		for value, key in arch.items():
			self.layer_names.append(value)
			self.layer_sizes.append(key)

		# create a weights and biases matrice for each layer. they can be created together however for simplicity they are seperate
		self.weights = []
		self.biases = []
		for i in range(0, len(self.layer_sizes) - 1):
			self.weights.append(
				np.matrix(data=np.random.uniform(-1, 1, (self.layer_sizes[i + 1], self.layer_sizes[i])), dtype=float))
			self.biases.append(np.matrix(data=np.ones((self.layer_sizes[i + 1], 1))))

		# create a drop layer for each layer with a probability of 10% of a neuron being inactive
		self.drop_layer = []
		for i in self.weights:
			y, x = i.shape
			m = np.matrix(data=[[(1 if k >= 0.1 else 0) for k in np.random.random(x)] for j in np.random.random(y)], dtype=int)
			self.drop_layer.append(m)

		# set local variables
		self.image = training
		self.label = labeled

		self.cache = []
		self.activations = []

		self.alpha = weight_learning_rate
		self.beta = bias_learning_rate
		self.update = display_update
		self.epochs = epochs

		# initialise the graph
		self.graph = Graph()

	def __repr__(self) -> str:
		'''
		purpose:
			- small debug of the neural network
			- shows its architecture
			- shows its weights and biases shapes for debugging if shapes dont align for multiplication
			- shows the size of the training data
			- shows the last output of the neural network
		'''

		# create a debug string and reutnr it
		debug = ""
		debug += f"\nNeuralNetwork:\n"
		debug += f" - Architecture:"
		debug += f"  - {'-'.join(str(l) for l in self.layer_sizes)}\n"
		debug += f"  - {'-'.join(str(l) for l in self.layer_names)}\n"
		debug += f" - weights:\n"
		debug += f"  - {'-'.join(str(l.shape) for l in self.weights)}\n"
		debug += f" - biases:\n"
		debug += f"  - {'-'.join(str(l.shape) for l in self.biases)}\n"
		debug += f" - dataset:\n"
		debug += f"  - {self.image.shape}\n"
		debug += f"\nData\n"
		debug += f" - outputL\n"
		debug += f"  - {self.cache[-1]}"
		return debug
		
	def train(self) -> None:
		'''
		purpose:
			- train the neural network
			- forward propagate the data on the neural network
			- calculate the cost 
			- backward propagate and update the weights and biases accordingly
			- print the average cost for the epoch and update the graph

		arguments:
			- self
			
		returns:
			- None
		'''

		# create local variables
		count = 0
		average_epoch = []
		iter_cost = []
		all_costs = []

		# for every training item
		for i in range(self.epochs):
			for x, y in zip(self.image, self.label):

				# forward propagate
				self.forward_propagate(x.reshape((np.multiply(x.shape[0], 1), 1)))

				# calculate the cost
				cost = self.cost_function(self.cache[-1], y)

				# backward propagate and learn
				self.backward_propagate2(y)
				
				# append the cost for its analysis
				average_epoch.append(cost)
				all_costs.append(cost)
				iter_cost.append(cost)
				
				# display iter information
				if count % 1000 == 0:
					print(f"epoch {i} count {count} average cost is {np.average(iter_cost)}")
					# for x1, y1 in zip(self.cache[-1], y):
					print(f"got {self.cache[-1].tolist()}, expected {y.tolist()}\n")
					self.graph.add(np.average(iter_cost))
					iter_cost = []
				count += 1
			
			# display epoch information + save the network
			if i % self.update == 0:
				print(f"epoch {i} average cost of last {self.update} epochs is {np.average(average_epoch)} also saving...")
				# self.save()
				average_epoch = []
				print(self)

	def forward_propagate(self, activations) -> None:
		'''
		purpose:
			- forward propagate the data on the neural network
			- calculate the activations and cache for each layer
			- save the activations and cache for each layer

		arguments:
			- self
			- activations: the activations of the first layer

		returns:
			- None
		'''

		# set cache up and activations
		self.cache = [activations]
		self.activations = [activations]

		# go over every layer, calculating the next layers activation values
		for i in range(len(self.weights)):
			
			# matrix multiple to get the sum of each connection connecting up to all neurons in the next layer
			sum = np.dot(np.multiply(self.weights[i], self.drop_layer[i]), self.cache[-1]) + self.biases[i]

			# save this to both the activations and cache
			self.activations.append(sum)
			self.cache.append(self.Sigmoid(sum))

	def backward_propagate2(self, expected) -> None:
		'''
		purpose:
			- backward propagate the data on the neural network
			- calculate the deltas for each layer
			- update the weights and biases accordingly

		arguments:
			- self
			- expected: the expected output of the last layer
		
		returns:
			- None
		'''

		# calculate deltas for the last layer, this is different than each consecutive layer afterwards
		deltas = [np.multiply(self.cost_function_deriv(self.cache[-1], expected), self.Sigmoid_derivative(self.activations[-1]))]

		# go over every layer backwards, calculating the deltas for each layer
		for i in np.arange(len(self.weights) - 1, 0, -1):
			delta = np.dot(self.weights[i].T, deltas[-1])
			delta = np.multiply(delta, self.Sigmoid(self.activations[i]))
			deltas.append(delta)

		# reverse the deltas so that they are in the correct order
		deltas.reverse()

		# update the weights and biases
		for i in np.arange(0, len(deltas)):
			self.weights[i] += np.multiply(-self.alpha, np.dot(deltas[i], self.cache[i].T))
			self.biases[i] += np.multiply(-self.beta, deltas[i])

	def Sigmoid(self, x:float) -> np.ndarray:
		'''
		purpose:
			- normalise the data to be between 0 and 1

		arguments:
			- self
			- x: the data to be normalised

		returns:
			- the normalised data
		'''

		# calculate the sigmoid of x and return
		return np.divide(1.0, (1.0 + np.exp(-x)))

	def Sigmoid_derivative(self, x:float) -> np.ndarray:
		'''
		purpose:
			- calculate the derivative of the sigmoid function on x
		
		arguments:
			- self
			- x: the data to be calculated on

		returns:
			- the derivative of the sigmoid function on x
		'''

		# calculate the derivative of the sigmoid function on x and return
		return np.multiply(self.Sigmoid(x), (1.0 - self.Sigmoid(x)))

	def ReLu(self, x:any) -> np.ndarray:
		'''
		purpose:
			- calculate the ReLu function on x and return

		arguments:
			- self
			- x: the data to be calculated on
		
		returns:
			- the ReLu function on x
		'''

		# another activation function that may be used
		return np.maximum(0, x)

	def ReLu_deriv(self, x:any) -> np.ndarray:
		'''
		purpose:
			- calculate the derivative of the ReLu function on x and return

		arguments:
			- self
			- x: the data to be calculated on
		
		returns:
			- the derivative of the ReLu function on x
		'''

		# derivative of the relu function
		return np.array(np.array(x) > 0, dtype=int)

	def cost_function(self, predicted:np.ndarray, expected:np.ndarray) -> float:
		'''
		purpose:
			- calculate the cost function on the predicted and expected values
			- how wrong did the neural network predict the expected values
			- uses this to update the weights and biases of the neural network

		arguments:
			- self
			- predicted: the predicted values
			- expected: the expected values

		returns:
			- the cost function on the predicted and expected values
		'''

		# constant
		m = 10

		# calculate the cost and reuturn, this is known as the cross entropy cost function
		# rcross entropy is widely used in classification models, which is an axample of this implementation
		cost = -1 / m * np.sum(np.multiply(expected, np.log(predicted)) + np.multiply((1 - expected), np.log(1 - predicted)))
		cost = np.squeeze(cost)
		return cost

	def cost_function_deriv(self, predicted, expected) -> float:
		'''
		purpose:
			- calculate the derivative of the cost function on the predicted and expected values
			- how wrong did the neural network predict the expected values
			- uses this to update the weights and biases of the neural network

		arguments:
			- self
			- predicted: the predicted values
			- expected: the expected values

		returns:
			- the derivative of the cost function on the predicted and expected values
		'''

		# calculate the derivative of the cost function and return
		# cross entropy cost derivative
		return -1 * (np.divide(expected, predicted) - np.divide(1-expected, 1-predicted))

	def save(self) -> None:
		'''
		purpose:
			- save the weights, biases, layer sizes, layer names and drop layer to a file
			- this is so that the neural network can be loaded from a file
			- this is useful for when the neural network is training for a long time
			- this is also useful for when the neural network is training on a computer that is not yours
			- used when the training could be interrupted and then resumed at a later time

		arguments:
			- self

		returns:
			- None
		'''

		# save all of the data to the files
		np.save("save/weights", np.asarray(self.weights, dtype=object))
		np.save("save/biases", np.asarray(self.biases, dtype=object))
		np.save("save/layer_sizes", np.asarray(self.layer_sizes, dtype=object))
		np.save("save/layer_names", np.asarray(self.layer_names, dtype=object))
		np.save("save/drop_layer", np.asarray(self.drop_layer, dtype=object))

	def load(self) -> None:
		'''
		purpose:
			- load the weights, biases, layer sizes, layer names and drop layer from a file
			- used when the neural network needs to be resumed

		arguments:
			- self

		returns:
			- None

		'''

		# load all of the data from the files
		self.weights = np.load("save/weights.npy", allow_pickle=True)
		self.biases = np.load("save/biases.npy", allow_pickle=True)
		self.layer_sizes = np.load("save/layer_sizes.npy", allow_pickle=True)
		self.layer_names = np.load("save/layer_names.npy", allow_pickle=True)
		self.drop_layer = np.load("save/drop_layer.npy", allow_pickle=True)

	def predict(self, data) -> float:
		'''
		purpose:
			- predict the output of the neural network on the data

		arguments:
			- self
			- data: the data to be predicted on

		returns:
			- the predicted output of the neural network on the data
		'''

		
		# forward propagate the data
		self.forward_propagate(data)

		# get the last layer of the neural network which is the output of the network
		result = self.cache[-1]

		# find the largest percentage in the result and its index
		biggest = [-99999, -1]
		for i in range(0, len(result)):
			if result[i][0] > biggest[0]:
				biggest[0] = result[i][0]
				biggest[1] = i

		print(f"predicted {biggest[0]} at index {biggest[1]}")

		# return the value of the largest predicted percentage
		return biggest[1]
	


def get_live_data_from_api(site_code='MY1', species_code='NO', start_date=None, end_date=None) -> dict: # done
		'''
		purpose:
			- Return data from the LondonAir API using its AirQuality API. 

		arguments:
			- site_code:  the site code to inspect
			- species_code: which species data to acquire
			- start_date: the lower bound for the range to collect the data
			- end_date: the upper bound for the range to collect the data

		return:
			- a json object consisiting of each measurement of data for the given site code and species code
			  between the start datr and the end date
		'''

		# start and end date calculated if not provided
		start_date = datetime.date.today() if start_date is None else start_date
		end_date = start_date + datetime.timedelta(days=1) if end_date is None else end_date

		# url is created using the data provided
		url = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={0}/SpeciesCode={1}/StartDate={2}/EndDate={3}/Json".format(
			site_code,
			species_code,
			start_date,
			end_date
		)

		# get the response from the server using the get request and return the json object
		response = requests.get(url) 
		return response.json()

def getSpecies() -> dict: # done
	'''
	purpose:
		- acquires data about each site and what species it measures

	arguments:
		- none

	returns:
		- a dictionary that consists of the sitecode as a key and what that site measures in an array as the value
	'''

	data = {}

	# request species data in london from the server endpoint and decode it
	response = requests.get(url="https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSiteSpecies/GroupName=London/Json")
	response = json.loads(response.content.decode("utf-8"))

	# for all monitoring sites
	for i in response["Sites"]["Site"]:

		# add to the dictionary the sites code linking to an empty array
		data.setdefault(i["@SiteCode"], [])

		# some species types collected by the sites could be a list rather than a dictionary
		if type(i["Species"]) == list: 
			
			# if a list, iterate through each species and add it to the dictionary
			for j in i["Species"]:
				data[list(data.keys())[-1]].append(j["@SpeciesCode"])
		else:
			# species is in a dictionary, add it to the dictionary
			data[list(data.keys())[-1]].append(i["Species"]["@SpeciesCode"])

	# return the data
	return data 
	
def getAllSites() -> list: # done
	'''
	purpose:
		- gets a list of all of the monitoring stations

	arguments:
		- none

	returns:
		- a list of all of the monitoring stations
	'''

	# create an empyt list
	sites = []

	# make request to server and jsonify response
	response = requests.get(url="https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSites/GroupName=London/Json") 
	response = response.json()																									

	# for every site append the site code to the list and return
	for i in response["Sites"]["Site"]:																							# 
		sites.append(i["@SiteCode"])
	return sites

def getAllData(species_code:str, days:int) -> dict: # done
	'''
	purpose:
		- gathers all data for every monitoring station for a given species code and days to look at into the past

	arguments:
		- species_code: the species code to get the data for
		- days: amount of days in the past to look at

	returns: 
		- all data in dictionary format with the keys being the sitecode and the values being the readings
	'''
	# create an empty list and get a list of all the sites
	data = []
	sites = getAllSites() 
	
	# calculate the time range for given days
	startDate = datetime.date.today() - datetime.timedelta(days)
	endDate = datetime.date.today()
	
	# with open("data.txt", "r") as f:
	# 	data = json.load(f) # load data from the file
	
	# for every site code get data and create a dictionary containing date data and the value data
	for i in sites:
		try:
			response = get_live_data_from_api(site_code=i, species_code=species_code, start_date=startDate, end_date=endDate)
			print(f"got response for -> {i}      {sites.index(i) + 1}/{len(sites)}")

			for j in response["RawAQData"]["Data"]:
				if j["@Value"] != "":
					data.append({i:[int(j["@MeasurementDateGMT"].split(" ")[0].split("-")[0]), # year
								int(j["@MeasurementDateGMT"].split(" ")[0].split("-")[1]), # month
								int(j["@MeasurementDateGMT"].split(" ")[0].split("-")[2]), # day
								int(j["@MeasurementDateGMT"].split(" ")[1].split(":")[0]), # hour
								int(float(j["@Value"]))]}) # value
		except:
			print(f"response invalid for {i}	{sites.index(i) + 1}/{len(sites)} skipping")

		
	
	# save data to file
	# with open("data.txt", "r+") as f:
	# 	f.truncate(0)
	# 	f.seek(0)
	# 	json.dump(data, f)
	# 	f.truncate()
	
	return data

def getCoordsAndData(species:str, days:int) -> tuple: # done
	'''
	purpose:
		- gathers two dictionaries whos keys are the site codes and one dictionaries values are that dictionaries
		  location data in latitude and longitude format and the other contains the readings data made from the 
		  monitoring stations for a given species

	arguments:
		- species: the species code
		- days: days in the past to look at the reading data

	returns:
		- coordinates two dictionaries, one which contains the sitecodes as keys and their corresponding readings in
		  the past n days as an array, and another dictionary that contains sitecodes as keys and their corresponding
		  coordinates in latitude and longitude format
	'''

	# initiate local variables
	locationData = {}
	data = {}
	allData = []
	siteData = {}

	# get all the data for the given species in the past n days
	content = getAllData(species_code=species, days=days)

	# for every site in all of the data create a dictionary with the sitecode as the key and the value being an array
	for i in content:
		for key, value in zip(list(i.keys()), list(i.values())):
			if key not in list(data.keys()):
				data.setdefault(key, [value[4]])
			else:
				data[key].append(value[4])
			allData.append(value[4])
	
	# calculate the average of all of the data
	avg = sum(allData) // len(allData)

	# get the location data
	response = requests.get(url="https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSiteSpecies/GroupName=London/Json")
	response = response.json()

	# create a dictionary with the sitecode as the key and the value being an array containing the latitude and longitude
	for i in response["Sites"]["Site"]:
		locationData.setdefault(i["@SiteCode"], [i["@Longitude"], i["@Latitude"]])

	# create a dictionary with the sitecode as the key and the value being the difference between the average and the distance of the value from the average
	# produces a value that which represents the severty of the pollution
	for key, value in zip(list(data.keys()), list(data.values())):
		dif = abs(avg - sum(value) // len(value))
		siteData.setdefault(key, dif)

	return siteData, locationData

def neuralNetwork() -> None: # done
	'''
	purpose:
		- creates a neural network for the given data and trains it to predict the pollution levels for each hour of the day in the future

	arguments:
		- none

	returns:
		- none
	'''

	# get all data for the past week
	data = getAllData(species_code="NO2", days=7)

	# generate an array for the activations and the expected outputs
	activation = np.zeros(shape=(len(data), 24, 1), dtype=float)
	output = np.zeros(shape=(len(data), 20, 1), dtype=float)

	# set the activations and outputs to their corresponding values from the data
	for i in range(0, len(data)):
		activation[i][list(data[i].values())[0][3]] = 1.0

	for i in range(0, len(data)):
		output[i][list(data[i].values())[0][4] // 10] = 1.0

	# create the network for a given architecture and other variables vital for its training
	architecture = {"input": 24, "hidden1": 10, "hidden2": 10, "output": 20}
	net = NeuralNet2(arch=architecture, training=activation, labeled=output, epochs=20, weight_learning_rate=0.1, bias_learning_rate=0.1)

	# train the network on the data provided
	net.train()
	
	# test the network on user input, the user enters the time of day and the network predicts the pollution level, catch errors
	try:
		test = np.zeros(shape=(24, 1), dtype=float)
		time = int(input("enter the time to predict what the pollution is at"))
		test[time] = 1.0
		print(test)

		result = net.predict(test)
		print(f"Predicted level of pollutant {result * 10}")
	except:
		print("invalid input")

if __name__ == "__main__":
	disp = Display()
	disp.showAxis() # functionality 1, show the data on some axis in tkinter
	# disp.showMap() # functionarilty 2, show the data on a map in tkinter
	disp.Update()

	# data = getAllData("NO2", days=2)
	# with open("data.txt", "a") as f:
	# 	json.dump(data, f)

	# neuralNetwork() # functionality 3, use a neural network to predict the pollution levels in the future for a given hour of the day

	# functionality 4, any of the functions above
	
	

