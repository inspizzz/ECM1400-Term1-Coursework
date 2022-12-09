import numpy as np

def daily_average(data:dict, monitoring_station:str, pollutant:str) -> list:
    '''
    purpose:
        - 

    arguments:
        - 

    returns:
        - 
    '''

    """
    data: list of all data from csv file
    monitoring_station: which monitoring station to take data from
    pollutant: which pollutant to look at specifically

    returns: a list of the daily averages of the pollutant in that specific area
    """
    
    print(f"\n\n\n{monitoring_station} : {pollutant}")
    result = []
    # check if the station exists although this is unnecessary because data is already supplied so why have it ?
    if monitoring_station in list(data.keys()): 
        # collect the pollutant data column
        index = data[monitoring_station][0].index(pollutant)
        data = [data[monitoring_station][i][index] for i in range(1, len(data[monitoring_station]))]

  
        for i in range(0, len(data), 24): # start at the beginning of the day each iteration
            collected = data[i:i+24] # collect the days data ie. 24 values
            filtered = list(filter(("No data").__ne__, collected)) # remove all occurrences of No data
            converted = list(map(float, filtered)) # convert strings to floats so they can be summed

            if len(converted) != 0: # some days may have no values collected
                result.append(sum(converted) / len(converted)) # add mean average to the list
            else:
                result.append(None) # if the day has no values just put None instead

        return result # return the averages in neat array format
    else:
        raise("not a valid monitoring station try (Harlington, Marylebone Road, N Kensington)")


def daily_median(data:dict, monitoring_station:str, pollutant:str) -> list:
    '''
    purpose:
        - calculates each days median for the years worth of data for a given 
          monitoring station and pollutant

    arguments:
        - data: dictionary of all data from csv file
        - monitoring_station: which monitoring station to take data from
        - pollutant: which pollutant to look at specifically

    returns:
        - a list of medians for each day within the years worth of data
    '''
    """
    

    returns: a list of the daily medians of the pollutant in that specific area
    """

    # declare return variable
    result = []

    # check if the monitoring station is valid
    if monitoring_station in list(data.keys()):  
        # 
        index = data[monitoring_station][0].index(pollutant)
        data = [data[monitoring_station][i][index] for i in range(1, len(data[monitoring_station]))]
        
        for i in range(0, len(data), 24): # start at the beginning of the day each iteration
            collected = data[i:i+24] # collect the days data ie. 24 values
            filtered = list(filter(("No data").__ne__, collected)) # remove all occurrences of No data
            converted = list(map(float, filtered)) # convert strings to floats so they can be summed

            if len(converted) != 0: # some days may have no values collected
                result.append(np.median(converted))
            else:
                result.append(None) # if the day has no values just put None instead

        return result # return the averages in neat array format
    else:
        raise("not a valid monitoring station try (Harlington, Marylebone Road, N Kensington)")
    

def hourly_average(data:list, monitoring_station:str, pollutant:str) -> list: # done
    '''
    purpose:
        - calculates hourly averages for the pollutant for a given monitoring station

    arguments:
        - data: dictionary of all data
        - monitoring_station: which monitoring station to take data from
        - pollutant: which pollutant to look at specifically


    returns:
        - a list of 24 values of the hourly averages for the pollutant and monitoring station
    '''

    # initiate return variable
    result = []

    # check if the monitoring station is valid
    if monitoring_station in list(data.keys()):  

        # initiate variables to collect hourly data
        collect = [0] * 24
        counter = [0] * 24

        # grab the indexes of the time and pollutant within the data
        timeIndex = data[monitoring_station][0].index("time")
        pollutantIndex = data[monitoring_station][0].index(pollutant)

        # grab the time and pollutant columns from the data
        timeData = [data[monitoring_station][i][timeIndex] for i in range(1, len(data[monitoring_station]))]
        pollutantData = [data[monitoring_station][i][pollutantIndex] for i in range(1, len(data[monitoring_station]))]

        # collect each hour and store it into the collect and counter variables, checking if value exists
        for time, value in zip(timeData, pollutantData):
            index = int(time.split(":")[0]) - 1
            if value != "No data":
                collect[index] += float(value)
                counter[index] += 1

        # calculate all of the averages for each hour
        for x, y in zip(collect, counter): 
            # maybe no values were collected, cannot divide by 0
            if y != 0:
                result.append(x / y)
            else:
                result.append(None)

        return result
    else:
        raise("not a valid monitoring station try (Harlington, Marylebone Road, N Kensington)")


def monthly_average(data:list, monitoring_station:str, pollutant:str) -> list: # done
    '''
    purpose:
        - calculates the average value each month for a given pollutant for a given monitoring station

    arguments:
        - data: dictionary of all data
        - monitoring_station: which monitoring station to take data from
        - pollutant: which pollutant to look at specifically

    returns:
        - a list of the monthly averages of the pollutant in that specific area
    '''

    # initiate a variable to return
    result = []

    # check if the monitoring station is valid and is in the data dictionary
    if monitoring_station in list(data.keys()):
        # initiate variables to store monthly data
        collect = [0] * 12
        counter = [0] * 12

        # inititae index variables for date and pollutant within the data
        dateIndex = data[monitoring_station][0].index("date")
        pollutantIndex = data[monitoring_station][0].index(pollutant)

        # grab the date and pollutant columns
        dateData = [data[monitoring_station][i][dateIndex] for i in range(1, len(data[monitoring_station]))]
        pollutantData = [data[monitoring_station][i][pollutantIndex] for i in range(1, len(data[monitoring_station]))]

        # append values for each month into the collect and counter variables ignoring no data values
        for date, value in zip(dateData, pollutantData):
            index = int(date.split("-")[1]) - 1
            if value != "No data":
                collect[index] += float(value)
                counter[index] += 1

        # calculate all of the averages for each month
        for x, y in zip(collect, counter): 
            # maybe no values were collected, cannot divide by 0
            if y != 0: 
                result.append(x / y)
            else:
                result.append(None)

        return result
    else:
        raise("not a valid monitoring station try (Harlington, Marylebone Road, N Kensington)")
    
    
def peak_hour_date(data:list, date:str, monitoring_station:str, pollutant:str) -> str: # done
    '''
    purpose:
        - finds the hour of a day in which a specific pollutant was the highest

    arguments: 
        - data: dictionary of all data
        - date: day which to inspect
        - monitoring_station: which monitoring station to take data from
        - pollutant: which pollutant to look at specifically

    returns:
        - the peak hour within the given day
    '''

    # check if the monitoring station is valid
    if monitoring_station in list(data.keys()):
        # initiate variables and indexes of the date, time and pollutant
        total = {}
        dateIndex = data[monitoring_station][0].index("date")
        timeIndex = data[monitoring_station][0].index("time")
        pollutantIndex = data[monitoring_station][0].index(pollutant)

        # get the corresponding columns
        dateData = [data[monitoring_station][i][dateIndex] for i in range(1, len(data[monitoring_station]))]
        timeData = [data[monitoring_station][i][timeIndex] for i in range(1, len(data[monitoring_station]))]
        pollutantData = [data[monitoring_station][i][pollutantIndex] for i in range(1, len(data[monitoring_station]))]

        # find the target day and append all values that have data into the dictionary
        for date2, time, value in zip(dateData, timeData, pollutantData):
            if date2 == date:
                if value != "No data":
                    total.setdefault(time, float(value))

        # look through the dictionary for the max value and at what index is it at then find that date in the keys at the same index, basically reversing a dictionary
        # hahaha evil laugh
        return (list(total.keys())[list(total.values()).index(max(list(total.values())))], total[list(total.keys())[list(total.values()).index(max(list(total.values())))]]) # horrendous,      note to self, dont try to understand this later, it works, leave it
    else:
        raise("not a valid monitoring station try (Harlington, Marylebone Road, N Kensington)")
    

def count_missing_data(data:list,  monitoring_station:str, pollutant:str) -> int: # done
    '''
    purpose:   
        - counts the amount of elements in the dataset that has no data as the value

    arguments:
        - data:  dictionary of all data
        - monitoring_station: which monitoring station to look at
        - pollutant: which pollutant to inspect the no data fields

    returns:
        - number of no data entries for a given station and pollutant
    '''
    # check if the monitoring station is valid
    if monitoring_station in list(data.keys()):
        # set variables and get the column of required data to inspect
        result = 0
        index = data[monitoring_station][0].index(pollutant)
        data = [data[monitoring_station][i][index] for i in range(1, len(data[monitoring_station]))]
        
        # check every element in the column and append the counter
        for i in data:
            if i == "No data":
                result += 1
        return result
    else:
        raise("not a valid monitoring station try (Harlington, Marylebone Road, N Kensington)")


def fill_missing_data(data:list, new_value:float,  monitoring_station:str, pollutant:str) -> dict: # done
    '''
    purpose:
        - replaces all no-data fields with a value

    arguments:
        - data: dictionary of all data
        - new_value: new value to be placed in place for all No data fields
        - monitoring_station: which monitoring station to take data from
        - pollutant: which pollutant to look at specifically

    returns:
        - the same dictionary data that was passed as an argument, but with replaced data
    '''

    index = {"no":2, "pm10":3, "pm25":4}

    # check if the monitoring station exists
    if monitoring_station in list(data.keys()):
        # for every row, check it and replace no data elements with new_value
        for i in range(0, len(data[monitoring_station])):
            if data[monitoring_station][i][index[pollutant]] == "No data":
                data[monitoring_station][i][index[pollutant]] = new_value

        return data
    else:
        raise("not a valid monitoring station try (Harlington, Marylebone Road, N Kensington)")


def read() -> dict: # done
    '''
    purpose:
        - reads all data from the file, once

    arguments:
        - none

    returns:
        - all the data in dictionary form
    '''
    # create variables
    data = {"Harlington":[], "Marylebone Road":[], "N Kensington":[]}
    possible_stations = ["Harlington", "Marylebone Road", "N Kensington"]

    # for every station open the file and read the data appending to corresponding array in dictionary
    for station in possible_stations:
        with open(f"data/Pollution-London {station}.csv", "r") as f:
            for line in f.readlines():
                line = line.rstrip()
                data[station].append([line.split(",")[0], line.split(",")[1], line.split(",")[2], line.split(",")[3], line.split(",")[4]])
    return data

    
if __name__ == "__main__":
    possible_stations = ["Harlington", "Marylebone Road", "N Kensington"]
    possible_species = ["no", "pm10", "pm25"]
    data = read()

    for station in possible_stations:
        for species in possible_species:
            # result = daily_average(data=data, monitoring_station=station, pollutant=species)
            # result = daily_median(data=data, monitoring_station=station, pollutant=species)
            # result = hourly_average(data=data, monitoring_station=station, pollutant=species)
            # result = monthly_average(data=data, monitoring_station=station, pollutant=species)
            # result = peak_hour_date(data=data, date="2021-01-11", monitoring_station=station, pollutant=species)
            # result = count_missing_data(data=data, monitoring_station=station, pollutant=species)
            # result = fill_missing_data(data=data, new_value=3.0, monitoring_station=station, pollutant=species)
            pass

