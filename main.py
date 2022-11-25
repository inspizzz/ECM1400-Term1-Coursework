# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification


def main_menu():
    """Your documentation goes here"""
    value = input("• R - Access the PR module\n• I - Access the MI module\n• M - Access the RM module\n• A - Print the About text\n• Q - Quit the application")
    print(value)

    match value:
        case "R":
            reporting_menu()
        case "I":
            intelligence_menu()
        case "M":
            monitoring_menu()
        case "A":
            about()
        case "Q":
            quit()
        case _:
            print("wrong input, try again")
            main_menu()


def reporting_menu():
    """Your documentation goes here"""
    # Your code goes here


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
    """Your documentation goes here"""
    # Your code goes here


if __name__ == '__main__':
    main_menu()