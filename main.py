import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import monitoring
import intelligence
import reporting
import utils

def main_menu():
    """Your documentation goes here"""
    value = input(" -> R - Access the PR module\n\
 -> I - Access the MI module\n\
 -> M - Access the RM module\n\
 -> A - Print the About text\n\
 -> Q - Quit the application\n\
 -> ")

    if value == "R":
        reporting_menu()
    elif value == "I":
        intelligence_menu()
    elif value == "M":
        monitoring_menu()
    elif value == "A":
        about()
    elif value == "Q":
        quit()
    else:
        print("wrong input, try again")
        main_menu()


def reporting_menu(): 
    '''
    purpose:
        - displays a menu to the user in which they can select one of the functions in the reporting menu
        
    arguments:
        - None
        
    returns:
        - None
    '''

    choice = input("choose a function to execute:\n\n\
 -> daily average - 1 {monitoring station} {pollutant}\n\
 -> daily median - 2 {monitoring station} {pollutant}\n\
 -> hourly average - 3 {monitoring station} {pollutant}\n\
 -> monthly average - 4 {monitoring station} {pollutant}\n\
 -> peak hour date - 5 {date} {monitoring station} {pollutant}\n\
 -> count missing data - 6 {monitoring station} {pollutant}\n\
 -> fill missing data - 7 {new value} {monitoring station} {pollutant}\n\
 -> show monitoring stations - 8\n\
 -> show pollutants - 9\n\
 -> quit - 10\n\
 -> ")

    if choice.split(" ")[0] == "1":

        # gather varibles
        data = reporting.read()
        monitoring_station = choice.split(" ")[1]
        pollutant = choice.split(" ")[2]

        if monitoring_station not in reporting.possible_stations:
            print("invalid monitoring station")
            reporting_menu()
            return

        if pollutant.lower() not in reporting.possible_species:
            print("invalid pollutant")
            reporting_menu()
            return

        # call function
        result = reporting.daily_average(data=data, monitoring_station=monitoring_station, pollutant=pollutant)
        print(f"\n\n{result}\n\n")
        reporting_menu()

    elif choice.split(" ")[0] == "2":

        # gather varibles
        data = reporting.read()
        monitoring_station = choice.split(" ")[1]
        pollutant = choice.split(" ")[2]

        if monitoring_station not in reporting.possible_stations:
            print("invalid monitoring station")
            reporting_menu()
            return

        if pollutant.lower() not in reporting.possible_species:
            print("invalid pollutant")
            reporting_menu()
            return

        # call function
        result = reporting.daily_median(data=data, monitoring_station=monitoring_station, pollutant=pollutant)
        print(f"\n\n{result}\n\n")
        reporting_menu()

    elif choice.split(" ")[0] == "3":

        # gather varibles
        data = reporting.read()
        monitoring_station = choice.split(" ")[1]
        pollutant = choice.split(" ")[2]

        if monitoring_station not in reporting.possible_stations:
            print("invalid monitoring station")
            reporting_menu()
            return

        if pollutant.lower() not in reporting.possible_species:
            print("invalid pollutant")
            reporting_menu()
            return

        # call function
        result = reporting.hourly_average(data=data, monitoring_station=monitoring_station, pollutant=pollutant)
        print(f"\n\n{result}\n\n")
        reporting_menu()

    elif choice.split(" ")[0] == "4":
            
        # gather varibles
        data = reporting.read()
        monitoring_station = choice.split(" ")[1]
        pollutant = choice.split(" ")[2]

        if monitoring_station not in reporting.possible_stations:
            print("invalid monitoring station")
            reporting_menu()
            return

        if pollutant.lower() not in reporting.possible_species:
            print("invalid pollutant")
            reporting_menu()
            return

        # call function
        result = reporting.monthly_average(data=data, monitoring_station=monitoring_station, pollutant=pollutant)
        print(f"\n\n{result}\n\n")
        reporting_menu()

    elif choice.split(" ")[0] == "5":
    
        # gather varibles
        data = reporting.read()
        date = choice.split(" ")[1]
        monitoring_station = choice.split(" ")[2]
        pollutant = choice.split(" ")[3]

        if monitoring_station not in reporting.possible_stations:
            print("invalid monitoring station")
            reporting_menu()
            return

        if pollutant.lower() not in reporting.possible_species:
            print("invalid pollutant")
            reporting_menu()
            return

        # call function
        result = reporting.peak_hour_date(data=data, date=date, monitoring_station=monitoring_station, pollutant=pollutant)
        print(f"\n\n{result}\n\n")
        reporting_menu()

    elif choice.split(" ")[0] == "6":
        
        # gather varibles
        data = reporting.read()
        monitoring_station = choice.split(" ")[1]
        pollutant = choice.split(" ")[2]

        if monitoring_station not in reporting.possible_stations:
            print("invalid monitoring station")
            reporting_menu()
            return

        if pollutant.lower() not in reporting.possible_species:
            print("invalid pollutant")
            reporting_menu()
            return

        # call function
        result = reporting.count_missing_data(data=data, monitoring_station=monitoring_station, pollutant=pollutant)
        print(f"\n\n{result}\n\n")
        reporting_menu()

    elif choice.split(" ")[0] == "7":
            
        # gather varibles
        data = reporting.read()
        new_value = choice.split(" ")[1]
        monitoring_station = choice.split(" ")[2]
        pollutant = choice.split(" ")[3]

        if monitoring_station not in reporting.possible_stations:
            print("invalid monitoring station")
            reporting_menu()
            return

        if pollutant.lower() not in reporting.possible_species:
            print("invalid pollutant")
            reporting_menu()
            return
            
        # call function
        result = reporting.fill_missing_data(data=data, new_value=new_value, monitoring_station=monitoring_station, pollutant=pollutant)
        print(f"\n\n{result}\n\n")
        reporting_menu()

    elif choice.split(" ")[0] == "8":
        print(f"\n\n{list(reporting.possible_stations)}\n\n")
        reporting_menu()

    elif choice.split(" ")[0] == "9":
        print(f"\n\n{list(reporting.possible_species)}\n\n")
        reporting_menu()

    elif choice.split(" ")[0] == 10:
        print("returning to main menu")
        main_menu()

    


def monitoring_menu():
    """Your documentation goes here"""
    # Your code goes here


def intelligence_menu():
    """Your documentation goes here"""
    # Your code goes here

def about():
    """Your documentation goes here"""
    # Your code goes here

def quit():
    '''
    purpose:
        - quit the application

    arguments:
        - None
    
    returns:
        -None
    '''
    exit()


if __name__ == '__main__':
    main_menu()




