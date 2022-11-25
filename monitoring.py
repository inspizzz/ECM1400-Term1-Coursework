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

class PollutionApi():
    def __init__(self):
        self.dataPath = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={sitecode}/SpeciesCode={speciescode}/StartDate={startdate}/EndDate={enddate}/Json"
        self.monitoringSitesPath = "https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSites/GroupName=London/json"


    

    def get_live_data_from_api(site_code='MY1',species_code='NO',start_date=None,end_date=None):
        """
        Return data from the LondonAir API using its AirQuality API. 

        *** This function is provided as an example of how to retrieve data from the API. ***
        It requires the `requests` library which needs to be installed. 
        In order to use this function you first have to install the `requests` library.
        This code is provided as-is. 
        """

        start_date = datetime.date.today() if start_date is None else start_date
        end_date = start_date + datetime.timedelta(days=1) if end_date is None else end_date


        url = self..format(
            site_code = site_code,
            species_code = species_code,
            start_date = start_date,
            end_date = end_date
        )

        res = requests.get(url)
        return res.json()

    def getMonitoringSites(self) -> list:
        """
        Grab data about the code names for all the possible site codes 

        returns an array of all of the site codes 
        """






def rm_function_1(*args,**kwargs):
    """show on the map """
    # Your code goes here

def rm_function_2(*args,**kwargs):
    """Your documentation goes here"""
    # Your code goes here

def rm_function_3(*args,**kwargs):
    """Your documentation goes here"""
    # Your code goes here

def rm_function_4(*args,**kwargs):
    """Your documentation goes here"""
    # Your code goes here


if __name__ == "__main__":
    data = get_live_data_from_api(site_code='MY1',species_code='NO',start_date="10-10-2021",end_date="11-10-2021")
    for i in data["RawAQData"]["Data"]:
        print(i)




