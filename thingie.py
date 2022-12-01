import tkinter as tk
import json
import requests
import datetime
import numpy as np
import matplotlib.pyplot as plt
import threading

class Display(tk.Tk):
	def __init__(self) -> None:
		super().__init__()
		self.WIDTH = 400
		self.HEIGHT = 400

		self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
		self.title("display")
		self.protocol("WM_DELETE_WINDOW", self.close)

		self.running = True
		self.axis = False
		self.map = False

		self.points = []
		self.lines = []
		self.xRange = [50, self.WIDTH-50]
		self.yRange = [self.HEIGHT-100, 50]

		self.bottomLeft = [-0.534210, 51.272226] # bottom left coordinates of the map
		self.bottomRight = [0.291138, 51.717670] # bottom right coordinates of the map


	## ----------------------------------------------------
	## ----------------------- AXIS -----------------------
	## ----------------------------------------------------
	def showAxis(self):
		self.axis = True

		self.axisFrame = tk.Frame(self, width=self.WIDTH, height=self.HEIGHT-100)
		self.axisFrame.pack(side="top", fill="both", expand=True)
		self.axisFrame.bind("<Configure>", self.configureAxis)

		self.menuFrame = tk.Frame(self, width=self.WIDTH, height=100)
		self.menuFrame.pack(side="bottom", fill="x")
		self.menuFrame.bind("<Configure>", self.configureMenu)

		self.axisCanvas = tk.Canvas(self.axisFrame, width=self.WIDTH, height=self.HEIGHT-100)
		self.axisCanvas.pack(side="top", fill="both", expand=True)

		self.menuCanvas = tk.Canvas(self.menuFrame, width=self.WIDTH, height=100)
		self.menuCanvas.pack(side="bottom", fill="both", expand=True)

		self.x_axis = self.axisCanvas.create_line(50, self.HEIGHT-50, self.WIDTH-50, self.HEIGHT-50, fill="black", width=2)
		self.y_axis = self.axisCanvas.create_line(50, self.HEIGHT-50, 50, 50, fill="black", width=2)

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

	def configureAxis(self, event):
		print(f"axis - {event}")
		if self.axis:
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


	def configureMenu(self, event):
		#print(f"menu - {event}")
		if self.axis:
			self.WIDTH = event.width + event.x
			self.HEIGHT = event.height + event.y
			
			#self.menuFrame.config(width=self.WIDTH, height=100)

	def addPoint(self, point:tuple, color:str="black"):
		if self.axis:
			x, y = point
			self.axisCanvas.update()
			thing = self.axisCanvas.create_line(self.points[-1][0], self.points[-1][1], 50 + x, self.axisCanvas.winfo_height() - 50 - y, fill=color, width=1) # create a line from the last point to the new one
			self.points.append((50 + x, self.axisCanvas.winfo_height() - 50 - y))
			self.lines.append(thing)

	def submit(self):
		speciesData = getSpecies()
		site = self.site.get(1.0, tk.END).rstrip()
		species = self.species.get(1.0, tk.END).rstrip()

		print(f"{site} : {species}")

		if site in list(speciesData.keys()):
			if species in speciesData[site]:
				# get the data for that specific site "KT4" "NO"
				data = get_live_data_from_api(site_code=site, species_code=species, start_date="2022-11-28", end_date="2022-11-29")
				for i in data["RawAQData"]["Data"]:
					if i["@Value"] != "":
						date = int(i["@MeasurementDateGMT"].split(" ")[1].split(":")[0])
						value = int(float(i["@Value"]))

						date = self.translate(date, 0, 24, 0, self.axisCanvas.winfo_width() - 100)
						value = self.translate(value, 0, 100, 0, self.axisCanvas.winfo_height() - 100)
						print(f"{date} : {value}")

						self.addPoint((date, value), color="black")

	def clear(self):
		self.points = [(50, self.axisCanvas.winfo_height() - 50)]
		for i in self.lines:
			self.axisCanvas.delete(i)
		self.lines = []

	def closeAxis(self):
		self.axisCanvas.pack_forget()
		self.axis = False

	## --------------------------------------------------
	## ----------------------- MAP -----------------------
	## ---------------------------------------------------
	def showMap(self):
		self.map = True

		self.image = tk.PhotoImage(file="london.gif") # -0.534210,51.272226,0.291138,51.717670
		self.WIDTH = self.image.width()
		self.HEIGHT = self.image.height()
		self.geometry(f"{self.image.width()}x{self.image.height()}")

		self.mapCanvas = tk.Canvas(self, width=self.WIDTH, height=self.HEIGHT)
		self.mapCanvas.pack(expand=True)
		self.mapCanvas.bind("<Configure>", self.mapConfigure)
		self.mapCanvas.create_image(0, 0, anchor=tk.NW, image=self.image)

	def coordToXY(self, lat:float, lon:float):
		latDif = abs(self.bottomLeft[0] - self.bottomRight[0])
		lonDif = abs(self.bottomLeft[1] - self.bottomRight[1])
		
		lat = lat - self.bottomLeft[0]
		lon = lon - self.bottomLeft[1]

		x = self.translate(lat, 0, latDif, 0, self.WIDTH)
		y = self.translate(lon, 0, lonDif, 0, self.HEIGHT)
		return x, y

	def addCircle(self, x:str, y:str, size:int=3, color:str="black") -> None:
		self.mapCanvas.create_oval(x, y, x+size, y+size, activeoutline=color)
	
	def mapConfigure(self, event):
		print(f"map - {event}")
		if self.map:
			self.WIDTH = event.width
			self.HEIGHT = event.height

			self.mapCanvas.config(width=self.WIDTH, height=self.HEIGHT)


	def closeMap(self):
		self.mapCanvas.pack_forget()
		self.map = False

	def translate(self, value, leftMin, leftMax, rightMin, rightMax):
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

	def close(self):
		self.running = False

	def Update(self):
		while self.running:
			self.update()
			self.update_idletasks()


class Graph:
	def __init__(self):
		plt.ion()
		self.accuracy = 1000
		self.counter = 0
		self.points = [2]*self.accuracy
		self.graph, = plt.plot(np.linspace(0, 1, self.accuracy))

	def add(self, y):
		self.points[self.counter] = y
		self.graph.set_ydata(self.points)
		plt.draw()
		plt.pause(0.00001)
		self.counter += 1
		if self.counter >= self.accuracy:
			self.counter = 0


class NeuralNet2:
	def __init__(self, arch, training, labeled, weight_learning_rate=0.05, bias_learning_rate=0.05, display_update=1000,
				 epochs=1):
		self.layer_names = []
		self.layer_sizes = []

		for value, key in arch.items():
			self.layer_names.append(value)
			self.layer_sizes.append(key)

		self.weights = []
		self.biases = []
		for i in range(0, len(self.layer_sizes) - 1):
			self.weights.append(
				np.matrix(data=np.random.uniform(-1, 1, (self.layer_sizes[i + 1], self.layer_sizes[i])), dtype=float))
			self.biases.append(np.matrix(data=np.ones((self.layer_sizes[i + 1], 1))))

		# self.drop_layer = []
		# for i in self.weights:
		# 	# create a mask for the weight matrix
		# 	y, x = i.shape
		# 	m = np.matrix(data=[[(1 if k >= 0.1 else 0) for k in np.random.random(x)] for j in np.random.random(y)], dtype=int)
		# 	self.drop_layer.append(m)

		self.image = training
		self.label = labeled

		self.cache = []
		self.activations = []

		self.alpha = weight_learning_rate
		self.beta = bias_learning_rate
		self.update = display_update
		self.epochs = epochs

		self.graph = Graph()

	def __repr__(self):
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
		
	def train(self):
		count = 0
		average_epoch = []
		iter_cost = []
		all_costs = []

		for i in range(self.epochs):
			for x, y in zip(self.image, self.label):
				self.forward_propagate(x.reshape((np.multiply(x.shape[0], 1), 1)))
				cost = self.cost_function(self.cache[-1], y)
				self.backward_propagate2(y)
				
				average_epoch.append(cost)
				all_costs.append(cost)
				iter_cost.append(cost)
				
				if count % 1000 == 0:
					print(f"epoch {i} count {count} average cost is {np.average(iter_cost)}")
					# for x1, y1 in zip(self.cache[-1], y):
					print(f"got {self.cache[-1]}, expected {y}\n")
					self.graph.add(np.average(iter_cost))
					iter_cost = []
				count += 1
				
			if i % self.update == 0:
				print(f"epoch {i} average cost of last {self.update} epochs is {np.average(average_epoch)} also saving...")
				# self.save()
				average_epoch = []
				print(self)

	def forward_propagate(self, activations):
		self.cache = [activations]
		self.activations = [activations]
		for i in range(len(self.weights)):
			sum = np.dot(self.weights[i], self.cache[-1]) + self.biases[i]
			# sum = np.dot(np.multiply(self.weights[i], self.drop_layer[i]), self.cache[-1]) + self.biases[i]
			self.activations.append(sum)
			self.cache.append(self.Sigmoid_derivative(sum))

	def backward_propagate2(self, expected):
		deltas = [np.multiply(self.cost_function_deriv(self.cache[-1], expected), self.Sigmoid_derivative(self.activations[-1]))]

		for i in np.arange(len(self.weights) - 1, 0, -1):
			delta = np.dot(self.weights[i].T, deltas[-1])
			delta = np.multiply(delta, self.Sigmoid_derivative(self.activations[i]))
			deltas.append(delta)
		deltas.reverse()
		for i in np.arange(0, len(deltas)):
			self.weights[i] += np.multiply(-self.alpha, np.dot(deltas[i], self.cache[i].T))
			self.biases[i] += np.multiply(-self.beta, deltas[i])

	def Sigmoid(self, x):
		return np.divide(1.0, (1.0 + np.exp(-x)))

	def Sigmoid_derivative(self, x):
		return np.multiply(self.Sigmoid(x), (1.0 - self.Sigmoid(x))) # <---

	def ReLu(self, x):
		return np.maximum(0, x)

	def ReLu_deriv(self, x):
		return np.array(np.array(x) > 0, dtype=int)

	def cost_function(self, predicted, expected):
		m = 10

		cost = -1 / m * np.sum(np.multiply(expected, np.log(predicted)) + np.multiply((1 - expected), np.log(1 - predicted)))
		cost = np.squeeze(cost)
		return cost

	def cost_function_deriv(self, predicted, expected):
		return -1 * (np.divide(expected, predicted) - np.divide(1-expected, 1-predicted))

	def save(self):
		# save the bias matrix
		# save the weight matrix
		# save the layer sizes
		# save the layer names

		np.save("save/weights", np.asarray(self.weights, dtype=object))
		np.save("save/biases", np.asarray(self.biases, dtype=object))
		np.save("save/layer_sizes", np.asarray(self.layer_sizes, dtype=object))
		np.save("save/layer_names", np.asarray(self.layer_names, dtype=object))
		np.save("save/drop_layer", np.asarray(self.drop_layer, dtype=object))

	def load(self):
		print("loading from file")
		# load the bias matrix
		# load the weight matrix
		# load the layer sizes
		# load the layer names

		self.weights = np.load("save/weights.npy", allow_pickle=True)
		self.biases = np.load("save/biases.npy", allow_pickle=True)
		self.layer_sizes = np.load("save/layer_sizes.npy", allow_pickle=True)
		self.layer_names = np.load("save/layer_names.npy", allow_pickle=True)
		self.drop_layer = np.load("save/drop_layer.npy", allow_pickle=True)


def get_live_data_from_api(site_code='MY1', species_code='NO', start_date=None, end_date=None):
		"""
		Return data from the LondonAir API using its AirQuality API. 

		*** This function is provided as an example of how to retrieve data from the API. ***
		It requires the `requests` library which needs to be installed. 
		In order to use this function you first have to install the `requests` library.
		This code is provided as-is. 
		"""
		start_date = datetime.date.today() if start_date is None else start_date
		end_date = start_date + datetime.timedelta(days=1) if end_date is None else end_date

		url = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={0}/SpeciesCode={1}/StartDate={2}/EndDate={3}/Json".format(
			site_code,
			species_code,
			start_date,
			end_date
		)

		response = requests.get(url)
		return response.json()

def getSpecies(*args,**kwargs):
	data = {}

	response = requests.get(url="https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSiteSpecies/GroupName=London/Json")
	response = json.loads(response.content.decode("utf-8"))

	for i in response["Sites"]["Site"]:
		data.setdefault(i["@SiteCode"], [])

		if type(i["Species"]) == list:
			for j in i["Species"]:
				data[list(data.keys())[-1]].append(j["@SpeciesCode"])
		else:
			data[list(data.keys())[-1]].append(i["Species"]["@SpeciesCode"])

	return data

def displayObjectivesMet():
	table = []

	response = requests.get(url="https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSites/GroupName=London/Json")
	response = json.loads(response.content.decode("utf-8"))
	
	for i in response["Sites"]["Site"]:

		
		
		# if i["@SiteCode"] in [i.keys() for i in table]:
		# 	table[i["@SiteCode"]].setdefault(i["@DataOwner"], )
		# response2 = requests.get(url=f"https://api.erg.ic.ac.uk/AirQuality/Annual/MonitoringObjective/SiteCode={str(i['@SiteCode'])}/Year=2021/Json")
		# if "<!DOCTYPE html PUBLIC" not in response2.content.decode("utf-8"):
		# 	response2 = json.loads(response2.content.decode("utf-8"))

		# if current != i["@DataOwner"]:
		# 		print("\n\ncode\t\tdata owner\t\t")
		# 		print("----------------------------------------------------------------------------------------------------")

		# print(f"{i['@SiteCode']}\t\t{i['@DataOwner']}", end="")
		# print(f"\t\t{response2['SiteObjectives']['Site']['Objective'][0]['@SpeciesCode']}\t\t{response2['SiteObjectives']['Site']['Objective'][0]['@Achieved']}")
			
		# for j in response2["SiteObjectives"]['Site']["Objective"]:
		# 	print(f"\t\t\t\t\t{j['@SpeciesCode']}\t\t{j['@Achieved']}")
		
		current = i["@DataOwner"]

def getAllSites() -> list:
	# get a list of all of the sites
	sites = []

	response = requests.get(url="https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSites/GroupName=London/Json")
	response = response.json()
	# print(response)
	for i in response["Sites"]["Site"]:
		sites.append(i["@SiteCode"])
	return sites

def getAllData(species_code:str) -> dict:
	# get a list of all the stations data
	data = []
	sites = getAllSites()
	for i in sites:
		response = get_live_data_from_api(site_code=i, species_code=species_code, start_date="2022-11-30", end_date="2022-12-1")
		
		print(f"got response for -> {i}      {sites.index(i) + 1}/{len(sites)}")
		for j in response["RawAQData"]["Data"]:
			if j["@Value"] != "":
				data.append({i:[int(j["@MeasurementDateGMT"].split(" ")[0].split("-")[0]), 
							int(j["@MeasurementDateGMT"].split(" ")[0].split("-")[1]),
							int(j["@MeasurementDateGMT"].split(" ")[0].split("-")[2]),
							int(j["@MeasurementDateGMT"].split(" ")[1].split(":")[0]),
							int(float(j["@Value"]))]})

	return data

def getCoordsAndData(species:str):
	locationData = {}
	data = {}
	allData = []
	siteData = {}

	with open("data.txt", "r") as f:
		content = json.load(f)

	# get the sitedata
	for i in content:
		for key, value in zip(list(i.keys()), list(i.values())):
			if key not in list(data.keys()):
				data.setdefault(key, [value[4]])
			else:
				data[key].append(value[4])
			allData.append(value[4])
	
	smallest = min(allData)
	largest = max(allData)
	avg = sum(allData) // len(allData)

	print(f"min : {smallest}\tmax : {largest}\tavg : {avg}")

	# get the location data
	response = requests.get(url="https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSiteSpecies/GroupName=London/Json")
	response = response.json()

	for i in response["Sites"]["Site"]:
		locationData.setdefault(i["@SiteCode"], [i["@Longitude"], i["@Latitude"]])

	for key, value in zip(list(data.keys()), list(data.values())):
		dif = abs(avg - sum(value) // len(value))
		siteData.setdefault(key, dif)
	print(siteData)
	print("\n")
	print(locationData)
	return siteData, locationData
	


# def train():
# 	# get the data for the past few years	
# 	data = getAllData(species_code="NO2")

# self.bottomLeft = [-0.534210, 51.272226] # bottom left coordinates of the map
# self.bottomRight = [0.291138, 51.717670] # bottom right coordinates of the map

if __name__ == "__main__":
	# getCoordsAndData("NO2")
	disp = Display()
	# disp.showAxis()
	disp.showMap()
	data, locations = getCoordsAndData("NO2")
	for key, value in zip(list(data.keys()), list(data.values())):
		lat, lon = locations[key]
		x, y = disp.coordToXY(float(lat), float(lon))
		disp.addCircle(x, y, color="black", size=value)
	disp.Update()

	
	
	# displayObjectivesMet()
	
	# input layer : year, month, day, hour
	# hidden layers there are three 
	# output layer, a value of the predicted measurement based on previous data

	# data = getAllData("NO2")
	# with open("data.txt", "a") as f:
	# 	json.dump(data, f)

	# with open("data.txt", "r") as f:
	# 	data = json.load(f)

	# A = [[i for i in j].values()[0:4] for j in data]
	# B = [[i for i in j].values()[4] for j in data]
	
	# architecture = {"input": 4, "hidden1": 50, "hidden2": 50, "hidden3": 50, "hidden4":50, "output": 1}
	# net = NeuralNet2(arch=architecture, training=np.asarray(A, dtype=int), labeled=np.asarray(B, dtype=float), epochs=10)
	# net.train()
