import tkinter as tk
import json
import requests
import datetime

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
		self.mapCanvas = tk.Canvas(self, width=self.WIDTH, height=self.HEIGHT)
		self.mapCanvas.pack()

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

			# check for changes too

## ---------------------------- 
## ---------------------------- 
##

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

# def displayObjectives():
# 	table = []


# 	response = requests.get(url="https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSites/GroupName=London/Json")
# 	response = json.loads(response.content.decode("utf-8"))

# 	for i in response["Sites"]["Site"]:
# 		if i["@SiteCode"] in [i.keys() for i in table]:
# 			table[i["@SiteCode"]].setdefault(i["@DataOwner"], )
# 		response2 = requests.get(url=f"https://api.erg.ic.ac.uk/AirQuality/Annual/MonitoringObjective/SiteCode={str(i['@SiteCode'])}/Year=2021/Json")
# 		if "<!DOCTYPE html PUBLIC" not in response2.content.decode("utf-8"):
# 			response2 = json.loads(response2.content.decode("utf-8"))


			



# 		if current != i["@DataOwner"]:
# 				print("\n\ncode\t\tdata owner\t\t")
# 				print("----------------------------------------------------------------------------------------------------")

# 		print(f"{i['@SiteCode']}\t\t{i['@DataOwner']}", end="")
		

# 			print(f"\t\t{response2['SiteObjectives']['Site']['Objective'][0]['@SpeciesCode']}\t\t{response2['SiteObjectives']['Site']['Objective'][0]['@Achieved']}")
			
# 			for j in response2["SiteObjectives"]['Site']["Objective"]:
# 				print(f"\t\t\t\t\t{j['@SpeciesCode']}\t\t{j['@Achieved']}")
				
			
			
			
# 		else:
# 			print("\t\tno")
		
# 		current = i["@DataOwner"]



if __name__ == "__main__":
	print(getSpecies())
	disp = Display()
	disp.showAxis()
	disp.Update()