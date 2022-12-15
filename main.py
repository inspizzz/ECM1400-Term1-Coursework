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
    value = input("• R - Access the PR module\n\n\
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
 -> return to main menu - 8\n\
 -> ")

    if choice == "1":
        monitoring_station = choice.split(" ")[1]
        pollutant = choice.split(" ")[2]
        reporting.daily_average(monitoring_station, pollutant)
    elif choice == "2":
        monitoring_station = choice.split(" ")[1]
        pollutant = choice.split(" ")[2]
        reporting.daily_median(monitoring_station, pollutant)

    elif choice == "3":
        monitoring_station = choice.split(" ")[1]
        pollutant = choice.split(" ")[2]
        reporting.hourly_average(monitoring_station, pollutant)


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




