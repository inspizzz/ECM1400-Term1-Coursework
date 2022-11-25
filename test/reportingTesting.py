import pandas as pd
import pytest as pt
import sys
import os



current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import reporting

possible_stations = ["Harlington", "Marylebone Road", "N Kensington"]
possible_pollutants = ["no", "pm10", "pm25"]


def dailyAverageTest():
    print("testing dailyAverage function", end=" ... ")
    for pollutant in possible_pollutants:
        for station in possible_stations:
            file = pd.read_csv(f"data/Pollution-London {station}.csv")
            assert len(reporting.daily_average(data=file, monitoring_station=station, pollutant=pollutant)) == 365
    print("dailyAverage Passed")


def dailyMedianTest():
    print("testing dailyMedian function", end=" ... ")
    for pollutant in possible_pollutants:
        for station in possible_stations:
            file = pd.read_csv(f"data/Pollution-London {station}.csv")
            assert len(reporting.daily_median(data=file, monitoring_station=station, pollutant=pollutant)) == 365
    print("dailyMedian Passed")


def hourlyAverageTest():
    print("testing hourlyAverage function", end=" ... ")
    for pollutant in possible_pollutants:
        for station in possible_stations:
            file = pd.read_csv(f"data/Pollution-London {station}.csv")
            assert len(reporting.hourly_average(data=file, monitoring_station=station, pollutant=pollutant)) == 24
    print("hourlyAverage Passed")

def monthlyAverageTest():
    print("testing monthlyAverage function", end=" ... ")
    for pollutant in possible_pollutants:
        for station in possible_stations:
            file = pd.read_csv(f"data/Pollution-London {station}.csv")
            assert len(reporting.monthly_average(data=file, monitoring_station=station, pollutant=pollutant)) == 12
    print("monthlyAverage Passed")


def peakHourDateTest():
    print("testing monthlyAverage function", end=" ... ")
    file = pd.read_csv(f"data/Pollution-London Harlington.csv")
    assert(reporting.peak_hour_date(data=file, date="2021-01-01", monitoring_station="Harlington", pollutant="no")) == ("20:00:00", 13.00595)
    print("monthlyAverage Passed")

def countMissingDataTest():
    print("testing countMissingData function", end=" ... ")
    test = {("Harlington", "no"):70, ("Harlington", "pm10"):57, ("Harlington", "pm25"):57,
            ("Marylebone Road", "no"):557, ("Marylebone Road", "pm10"):2120, ("Marylebone Road", "pm25"):1265,
            ("N Kensington", "no"):71, ("N Kensington", "pm10"):8, ("N Kensington", "pm25"):8}
    

    for x, y in zip(test.keys(), test.values()):
        file = pd.read_csv(f"data/Pollution-London {x[0]}.csv")
        assert(reporting.count_missing_data(data=file, monitoring_station=x[0], pollutant=x[1])) == y
    print("countMissingData Passed")

def fillMissingDataTest():
    print("testing fillMissingData function", end=" ... ")
    file = pd.read_csv(f"data/Pollution-London Harlington.csv")

    assert(len(reporting.fill_missing_data(data=file.to_numpy(), new_value="", monitoring_station="Harlington", pollutant="no"))) == 8760
    print("fillMissingData Passed")

if __name__ == "__main__":
    dailyAverageTest()
    dailyMedianTest()
    hourlyAverageTest()
    monthlyAverageTest()
    peakHourDateTest()
    countMissingDataTest()
    fillMissingDataTest()