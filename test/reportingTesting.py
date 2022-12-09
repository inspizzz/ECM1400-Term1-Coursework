import pandas as pd
import pytest
import sys
import os



current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import reporting

possible_stations = ["Harlington", "Marylebone Road", "N Kensington"]
possible_pollutants = ["no", "pm10", "pm25"]


def test_dailyAverage():
    print("testing dailyAverage function", end=" ... ")
    for pollutant in possible_pollutants:
        for station in possible_stations:
            data = reporting.read()
            assert len(reporting.daily_average(data=data, monitoring_station=station, pollutant=pollutant)) == 365
    print("dailyAverage Passed")


def test_dailyMedian():
    print("testing dailyMedian function", end=" ... ")
    for pollutant in possible_pollutants:
        for station in possible_stations:
            data = reporting.read()
            assert len(reporting.daily_median(data=data, monitoring_station=station, pollutant=pollutant)) == 365
    print("dailyMedian Passed")


def test_hourlyAverage():
    print("testing hourlyAverage function", end=" ... ")
    for pollutant in possible_pollutants:
        for station in possible_stations:
            data = reporting.read()
            assert len(reporting.hourly_average(data=data, monitoring_station=station, pollutant=pollutant)) == 24
    print("hourlyAverage Passed")

def test_monthlyAverage():
    print("testing monthlyAverage function", end=" ... ")
    for pollutant in possible_pollutants:
        for station in possible_stations:
            data = reporting.read()
            assert len(reporting.monthly_average(data=data, monitoring_station=station, pollutant=pollutant)) == 12
    print("monthlyAverage Passed")


def test_peakHourDate():
    print("testing monthlyAverage function", end=" ... ")
    data = reporting.read()
    assert(reporting.peak_hour_date(data=data, date="2021-01-01", monitoring_station="Harlington", pollutant="no")) == ("20:00:00", 13.00595)
    print("monthlyAverage Passed")

def test_countMissingData():
    print("testing countMissingData function", end=" ... ")
    test = {("Harlington", "no"):70, ("Harlington", "pm10"):57, ("Harlington", "pm25"):57,
            ("Marylebone Road", "no"):557, ("Marylebone Road", "pm10"):2120, ("Marylebone Road", "pm25"):1265,
            ("N Kensington", "no"):71, ("N Kensington", "pm10"):8, ("N Kensington", "pm25"):8}
    

    for x, y in zip(test.keys(), test.values()):
        data = reporting.read()
        assert(reporting.count_missing_data(data=data, monitoring_station=x[0], pollutant=x[1])) == y
    print("countMissingData Passed")

def test_fillMissingData():
    data = reporting.read()
    for station in possible_stations:
        for pollutant in possible_pollutants:
            print(f"testing fillMissingData function for {station}, {pollutant}", end=" ... ")

    
            assert(len(reporting.fill_missing_data(data=data, new_value="", monitoring_station=station, pollutant=pollutant))) == 8760
    print("fillMissingData Passed")

# if __name__ == "__main__":
#     dailyAverageTest()
#     dailyMedianTest()
#     hourlyAverageTest()
#     monthlyAverageTest()
#     peakHourDateTest()
#     countMissingDataTest()
#     fillMissingDataTest()