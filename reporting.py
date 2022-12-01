import numpy as np
import pandas as pd

possible_stations = ["Harlington", "Marylebone Road", "N Kensington"]

def daily_average(data:list, monitoring_station:str, pollutant:str) -> list:
    """
    data: list of all data from csv file
    monitoring_station: which monitoring station to take data from
    pollutant: which pollutant to look at specifically

    returns: a list of the daily averages of the pollutant in that specific area
    """
    result = []

    if monitoring_station in possible_stations: # check if the station exists although this is unnecessary because data is already supplied so why have it ?
        data = list(data.__getitem__(pollutant)) # collect the pollutant data
        
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


def daily_median(data:list, monitoring_station:str, pollutant:str) -> list:
    """
    data: list of all data from csv file
    monitoring_station: which monitoring station to take data from
    pollutant: which pollutant to look at specifically

    returns: a list of the daily medians of the pollutant in that specific area
    """
    result = []

    if monitoring_station in possible_stations: # check if the station exists although this is unnecessary because data is already supplied so why have it ?
        data = list(data.__getitem__(pollutant)) # collect the pollutant data
        
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
    

def hourly_average(data:list, monitoring_station:str, pollutant:str) -> list:
    """
    data: list of all data
    monitoring_station: which monitoring station to take data from
    pollutant: which pollutant to look at specifically

    returns: a list of the hourly averages of the pollutant in that specific area
    """

    result = []

    if monitoring_station in possible_stations: # check if the station exists although this is unnecessary because data is already supplied so why have it ?
        collect = [0] * 24
        counter = [0] * 24

        for time, value in zip(data.time, data.__getitem__(pollutant)):
            index = int(time.split(":")[0]) - 1 # get the index from the time, so all of the middays get added together
            if value != "No data": # check if there are any values that dont have any data corresponding
                collect[index] += float(value) # add the value to the others in the same hour
                counter[index] += 1 # log how many times added values together

        for x, y in zip(collect, counter): # calculate all of the averages for each month
            if y != 0: # maybe no values were collected, cannot divide by 0
                result.append(x / y) # calculate the average
            else:
                result.append(None) # place in placeholder to represent no values collected
        return result # return the averages in neat array format
    else:
        raise("not a valid monitoring station try (Harlington, Marylebone Road, N Kensington)")

    # arr = [data[i::24] for i in range(24)]
    # print(arr)



def monthly_average(data:list, monitoring_station:str, pollutant:str) -> list:
    """
    data: list of all data
    monitoring_station: which monitoring station to take data from
    pollutant: which pollutant to look at specifically

    returns: a list of the monthly averages of the pollutant in that specific area
    """

    result = []

    if monitoring_station in possible_stations: # check if the station exists although this is unnecessary because data is already supplied so why have it ?
        collect = [0] * 12
        counter = [0] * 12

        for date, value in zip(data.date, data.__getitem__(pollutant)): # iterate over only the date and value columns
            index = int(date.split("-")[1]) - 1 # get indexes by checking the date in the month in the data
            if value != "No data": # check if there is a No data tag in the data
                collect[index] += float(value) # add items together in the same month
                counter[index] += 1 # log how many items have been added together

        for x, y in zip(collect, counter): # calculate all of the averages for each month
            if y != 0: # maybe no values were collected, cannot divide by 0
                result.append(x / y) # calculate the average
            else:
                result.append(None) # place in placeholder to represent no values collected

        return result # return the averages in neat array format
    else:
        raise("not a valid monitoring station try (Harlington, Marylebone Road, N Kensington)")
    
    
def peak_hour_date(data:list, date:str, monitoring_station:str, pollutant:str) -> str:
    """
    data: list of all data
    date: day which to inspect
    monitoring_station: which monitoring station to take data from
    pollutant: which pollutant to look at specifically

    returns: a list of the monthly averages of the pollutant in that specific area
    """

    if monitoring_station in possible_stations: # check if the station exists although this is unnecessary because data is already supplied so why have it ?
        total = {} # for collecting data

        for date2, time, value in zip(data.date, data.time, data.__getitem__(pollutant)): # iterate over the date, time and values
            if date2 == date: # if the desired date is the one currently being looked at then 
                if value != "No data": # check for redundant data
                    total.setdefault(time, float(value)) # add to the dictionary

        # look through the dictionary for the max value and at what index is it at then find that date in the keys at the same index, basically reversing a dictionary
        return (list(total.keys())[list(total.values()).index(max(list(total.values())))], total[list(total.keys())[list(total.values()).index(max(list(total.values())))]]) # horrendous,      note to self, dont try to understand this later, it works, leave it
    else:
        raise("not a valid monitoring station try (Harlington, Marylebone Road, N Kensington)")
    

def count_missing_data(data:list,  monitoring_station:str, pollutant:str) -> int:
    """
    data: list of all data
    monitoring_station: which monitoring station to take data from
    pollutant: which pollutant to look at specifically

    returns: number of No data entries for a given station and pollutant
    """

    if monitoring_station in possible_stations: # check if the station exists although this is unnecessary because data is already supplied so why have it ?
        result = 0

        for i in data.__getitem__(pollutant):
            if i == "No data":
                result += 1
        return result
    else:
        raise("not a valid monitoring station try (Harlington, Marylebone Road, N Kensington)")

def fill_missing_data(data:list, new_value:float,  monitoring_station:str, pollutant:str) -> list:
    """
    data: list of all data
    new_value: new value to be placed in place for all No data fields
    monitoring_station: which monitoring station to take data from
    pollutant: which pollutant to look at specifically
    
    returns: number of No data entries for a given station and pollutant
    """
    index = {"no":2, "pm10":3, "pm25":4}

    if monitoring_station in possible_stations: # check if the station exists although this is unnecessary because data is already supplied so why have it ?
        for i in range(0, len(data)): # for every element 
            if data[i][index[pollutant]] == "No data": # check if element contains data
                data[i][index[pollutant]] = new_value # replace the value with the new value
        return data # return it
    else:
        raise("not a valid monitoring station try (Harlington, Marylebone Road, N Kensington)")


if __name__ == "__main__":
    possible_stations = ["Harlington"]
    possible_pollutants = ["no"]

    for pollutant in possible_pollutants:
        for station in possible_stations:
            file = pd.read_csv(f"data/Pollution-London {station}.csv")
            a = count_missing_data(data=file, monitoring_station=station, pollutant=pollutant)
            print(a)
            
