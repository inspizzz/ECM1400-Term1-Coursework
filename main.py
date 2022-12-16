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
    '''
    purpose:
        - displays a menu to the user in which they can select one of the modules
        - demonstrates the functionality of the modules

    arguments:
        - None

    returns:
        - None
    '''

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
        - demonstrates the functionality of the reporting module
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
 -> back - 10\n\
 -> ")

    
    if choice.split(" ")[0] == "1":
        if len(choice.split(" ")) >= 3:
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
            return
        else:
            print("too few arguments")
            reporting_menu()
            return

    elif choice.split(" ")[0] == "2":
        if len(choice.split(" ")) >= 3:
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
            return
        else:
            print("too few arguments")
            reporting_menu()
            return

    elif choice.split(" ")[0] == "3":
        if len(choice.split(" ")) >= 3:
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
            return
        else:
            print("too few arguments")
            reporting_menu()
            return

    elif choice.split(" ")[0] == "4":
        if len(choice.split(" ")) >= 3:
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
            return
        else:
            print("too few arguments")
            reporting_menu()
            return

    elif choice.split(" ")[0] == "5":
        if len(choice.split(" ")) >= 4:
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
            return
        else:
            print("too few arguments")
            reporting_menu()
            return

    elif choice.split(" ")[0] == "6":
        if len(choice.split(" ")) >= 3:
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
            return
        else:
            print("too few arguments")
            reporting_menu()
            return

    elif choice.split(" ")[0] == "7":
        if len(choice.split(" ")) >= 4:
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
            return
        else:
            print("too few arguments")
            reporting_menu()
            return

    elif choice.split(" ")[0] == "8":
        print(f"\n\n{list(reporting.possible_stations)}\n\n")
        reporting_menu()
        return

    elif choice.split(" ")[0] == "9":
        print(f"\n\n{list(reporting.possible_species)}\n\n")
        reporting_menu()
        return

    elif choice.split(" ")[0] == "10":
        print("returning to main menu")
        main_menu()
        return
    else:
        print("invalid choice")
        reporting_menu()
        return

def monitoring_menu():
    '''
    purpose:
        - display the monitoring menu
        - shows the functionality of the monitoring module

    arguments:
        - None

    returns:
        - None
    '''
    
    choice = input("choose a functionality to explore:\n\n\
 -> display graph in terminal - 1 {site} {species} \n\
 -> display axis - 2 \n\
 -> display map - 3 \n\
 -> neural network - 4 \n\
 -> back - 5 \n\n\
 -> ")

    
    disp = monitoring.Display()

    if choice.split(" ")[0] == "1":
        if len(choice.split(" ")) == 3:
            disp.createTerminalAxis()
            disp.plotDataTerminalAxis(site=choice.split(" ")[1], species=choice.split(" ")[2])
            monitoring_menu()
            return
        else:
            print("too few arguments")
            monitoring_menu()
            return
    # if user chose to see the axis then initialise the display and show, later call this function again
    if choice.split(" ")[0] == "2":
        disp.initDisplay()
        disp.showAxis()
        disp.Update()
        monitoring_menu()
        return

    # if user chooses to see the map, then show the map and then call this function again
    if choice.split(" ")[0] == "3":
        disp.initDisplay()
        disp.showMap()
        disp.Update()
        monitoring_menu()
        return

    # select the neural network option and then come back to this menu
    if choice.split(" ")[0] == "4":
        monitoring.neuralNetwork()
        monitoring_menu()
        return
        
    else:

        # the choice did not have any of the above options, call the same menu function again
        print("invalid choice")
        monitoring_menu()
        return

def intelligence_menu():
    '''
    purpose:
        - show the user options regarding the intelligence module
        - be able to find connected components
        - be able to sort connected components
    
    arguments:
        - None

    returns:
        - None
    '''

    choice = input("choose a functionality to explore from the intelligence module:\n\n\
 -> find red connected components - 1\n\
 -> find cyan connected components - 2\n\
 -> sort red connected components - 3\n\
 -> sort cyan connected components - 4\n\
 -> back - 5\n\
 -> ")

    # check the users choice and then call appropriate function of the intelligence module
    if choice == "1":

        # detect components in the cyan pixels image
        intelligence.detect_connected_components(intelligence.find_red_pixels(filename="./data/map.png", upperThreshold=100, lowerThreshold=50))
        print("check the file ./data/output/cc-output-2a.txt for updated values")
        intelligence_menu()

    elif choice == "2":

        # detect components in the cyan pixels image
        intelligence.detect_connected_components(intelligence.find_cyan_pixels(filename="./data/map.png", upperThreshold=100, lowerThreshold=50))
        print("check the file ./data/output/cc-output-2a.txt for updated values")
        intelligence_menu()

    elif choice == "3":

        # find sorted components in the red pixels image
        mark = intelligence.detect_connected_components(intelligence.find_red_pixels(filename="./data/map.png", upperThreshold=100, lowerThreshold=50))
        intelligence.detect_connected_components_sorted(mark)
        print("check the files ./data/output/cc-output-2b.txt and ./data/output/cc-top-2.jpg for the output of this function")
        intelligence_menu()

    elif choice == "4":

        # find sorted components in the cyan pixels image
        mark = intelligence.detect_connected_components(intelligence.find_cyan_pixels(filename="./data/map.png", upperThreshold=100, lowerThreshold=50))
        intelligence.detect_connected_components_sorted(mark)
        print("check the files ./data/output/cc-output-2b.txt and ./data/output/cc-top-2.jpg for the output of this function")
        intelligence_menu()

    elif choice == "5":
        main_menu()
        return
    
    else:

        # none of the options selected
        print("invalid choice, try again")
        intelligence_menu()

def about():
    '''
    purpose:
        - show the user the about page
        - show module code
        - show student number

    arguments:  
        - None

    returns:
        - None
    '''

    # print the module code and student number
    print("ECM1400")
    print("238249")
    main_menu()
    return

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




