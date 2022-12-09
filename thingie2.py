# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification.
# 
# This module will access data from the LondonAir Application Programming Interface (API)
# The API provides access to data to monitoring stations. 
# 
# You can access the API documentation here http://api.erg.ic.ac.uk/AirQuality/help
#

import requests
import datetime
import tkinter as tk
import json
from PIL import Image
import threading


class Display(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.HEIGHT = 400
        self.WIDTH = 400

        self.running = True

        self.axis = False
        self.xRange = [50, self.WIDTH-50]
        self.yRange = [self.HEIGHT-100, 50]
        self.points = [(50, self.HEIGHT-100)]
        self.lines = []
        self.reference = (50, self.HEIGHT-100)

        self.change = [False, ()]

        self.title("frame")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.bind("<Configure>", self.configure)
    

    def HideAxis(self):
        self.canvas.pack_forget()

        self.axis = False

    def showAxis(self):
        self.axis = True
        self.canvas = tk.Canvas(self)
        self.canvas.pack()
        self.canvas.config(width=self.WIDTH, height=self.HEIGHT)
        
        self.x_axis = self.canvas.create_line(50, self.HEIGHT-100, self.WIDTH-50, self.HEIGHT-100, fill="black", width=2)
        self.y_axis = self.canvas.create_line(50, self.HEIGHT-100, 50, 50, fill="black", width=2)

        self.site = tk.Text(self.canvas, width=10, height=1)
        self.site.place(x=50, y=self.HEIGHT-50)

        self.species = tk.Text(self.canvas, width=10, height=1)
        self.species.place(x=150, y=self.HEIGHT-50)

        self.submit = tk.Button(self.canvas, width=3, height=1, relief=tk.SOLID, text="submit", command=self.submit)
        self.submit.place(x=270, y=self.HEIGHT-50)
        
    def submit(self):
        data = getSpecies()

        if self.site.get() in list(getSpecies().keys()):
            if self.species.get() in data[self.site.get()]:
                graphData(self, self.site.get(), self.species.get())
            else:
                print("No species")
        else:
            print("No site")

    def showPoint(self, point:tuple, color:str="black") -> None:
        x, y = point
        x += 50
        y = self.HEIGHT - 100 - y

        if self.axis:
            thing = self.canvas.create_line(self.points[-1][0], self.points[-1][1], x, y, fill=color, width=1) # create a line from the last point to the new one
            self.lines.append(thing)

        self.points.append((x, y))

        print(self.points)

    def showMap(self):
        print(f"[DISPLAY] - showing map")
        self.map = True
        img = tk.PhotoImage(file="london.gif")
        print(f"{img.width()}, {img.height()}")

        label = tk.Label(self, image=img)
        label.grid(column=0, row=0, sticky="nw")

    def hideMap(self):
        self.map = False

    def close(self):
        print("[DISPLAY] - closing")
        self.running = False

    def configure(self, event):
        self.WIDTH = event.width
        self.HEIGHT = event.height

        if self.axis:
            self.canvas.config(width=self.WIDTH, height=self.HEIGHT)
            self.canvas.coords(self.x_axis, 50, self.HEIGHT-100, self.WIDTH-50, self.HEIGHT-100)
            self.canvas.coords(self.y_axis, 50, self.HEIGHT-100, 50, 50)

            prev_xRange = self.xRange
            prev_yRange = self.yRange

            self.xRange = [50, self.WIDTH-50]
            self.yRange = [self.HEIGHT-100, 50]

            # update the points
            for i in range(len(self.points)):
                x, y = self.points[i]
                newX = self.translate(x, prev_xRange[0], prev_xRange[1], self.xRange[0], self.xRange[1])
                newY = self.translate(y, prev_yRange[0], prev_yRange[1], self.yRange[0], self.yRange[1])
                self.points[i] = (newX, newY)
            
            for i in range(len(self.lines)):
                # update the lines
                self.canvas.coords(self.lines[i], self.points[i][0], self.points[i][1], self.points[i+1][0], self.points[i+1][1])
            print(f"range in x {abs(self.xRange[0] - self.xRange[1])} range in y {abs(self.yRange[0] - self.yRange[1])}")

        elif self.map:
            pass

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
            print("errorW")

    def loop(self): 
        while self.running:
            self.update()
            self.update_idletasks()


## ----------------------------------------------------------------------------------------------
##
##
##
##
## ----------------------------------------------------------------------------------------------

# display the data live on an axis in tkinter, add functionality for more display, also show color of the line as red orange and blue depending on health

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




def mapData(*args,**kwargs):
    data = []

    response = requests.get(url='https://api.erg.ic.ac.uk/AirQuality/Hourly/MonitoringIndex/GroupName=London/Json')
    response = json.loads(response.content.decode('utf-8'))
    counter = 1
    for i in response['HourlyAirQualityIndex']['LocalAuthority']:
        print(f"site {counter}")
        counter += 1
        if 'Site' in list(i.keys()):
            
            if type(i["Site"]) == list: # then there is an array of sites
                for j in i["Site"]:
                    if type(j["Species"]) == list:
                        for k in j['Species']:
                            row = {}
                            row.setdefault("SiteCode", j['@SiteCode'])
                            row.setdefault("Latitude", j['@Latitude'])
                            row.setdefault("Longitude", j['@Longitude'])
                            row.setdefault("SpeciesCode", k["@SpeciesCode"])
                            row.setdefault("Quality", k["@AirQualityIndex"])
                            row.setdefault("Band", k["@AirQualityBand"])
                            data.append(row)
                            
                    else:
                        row = {}
                        row.setdefault("SiteCode", j['@SiteCode'])
                        row.setdefault("Latitude", j['@Latitude'])
                        row.setdefault("Longitude", j['@Longitude'])
                        row.setdefault("SpeciesCode", j['Species']["@SpeciesCode"])
                        row.setdefault("Quality", j['Species']["@AirQualityIndex"])
                        row.setdefault("Band", j['Species']["@AirQualityBand"])
                        data.append(row)

            else: # is an dictionary                    
                for j in i["Site"]["Species"]:
                    row = {}
                    row.setdefault("SiteCode", i['Site']['@SiteCode'])
                    row.setdefault("Latitude", i['Site']['@Latitude'])
                    row.setdefault("Longitude", i['Site']['@Longitude'])
                    row.setdefault("SpeciesCode", j["@SpeciesCode"])
                    row.setdefault("Quality", j["@AirQualityIndex"])
                    row.setdefault("Band", j["@AirQualityBand"])
                    data.append(row)

    for i in data:
        print(i)


    
    

def graphData(instance:Display, site:str, species:str):
    data = get_live_data_from_api(site_code=site, species_code=species)
    
    for j in data["RawAQData"]["Data"]:
        date = j["@MeasurementDateGMT"]
        value = j["@Value"]
        
        if value != "":
            # plot it
            x = 50 + instance.translate(int(date.split(" ")[1].split(":")[0]), 0, 24, instance.xRange[0], instance.xRange[1])
            y = instance.HEIGHT - 100 - instance.translate(int(value), 0, 100, instance.yRange[0], instance.yRange[1])
            instance.showPoint((x, y))

    

def getStations(*args,**kwargs) -> list:
    data = []

    response = requests.get(url="https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSites/GroupName=London/Json")
    response = json.loads(response.content.decode("utf-8"))

    for i in response["Sites"]["Site"]:
        data.append(i["@SiteCode"])

    return data

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
            

if __name__ == "__main__":
    disp = Display()
    
    disp.showAxis()
    disp.showPoint((100, 100))

    #mapData()
    #data = getSpecies()
    #graphData(disp)

    disp.loop()







