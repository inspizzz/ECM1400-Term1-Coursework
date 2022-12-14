# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification


def sumValues(values):
    '''
    purpose:
        - sum all the values in the list

    arguments:
        - values: a list of numbers

    returns:
        - the sum of all the values in the list
    ''' 

    # catches any type errors 
    try: 

        # sum all elements in the list together and return
        sum = 0
        for i in values:
            sum += i

        return sum

    except TypeError:
        print("Invalid input. Please enter a list/array of numbers.")
        return None


def maxValue(values):
    '''
    purpose:
        - find the maximum value in the list

    arguments:
        - values: a list of numbers

    returns:
        - the maximum value in the list
    ''' 

    # catches any type errors
    try:
        # find the maximum value in the list and return
        max = -99999
        for i in values:
            if i > max:
                max = i

        return max

    except TypeError:
        print("Invalid input. Please enter a list/array of numbers.")
        return None



def minValue(values):
    '''
    purpose:
        - find the minimum value in the list

    arguments:
        - values: a list of numbers

    returns:
        - the minimum value in the list
    ''' 

    # catches any type errors
    try:

        # find the minimum value in the list and return
        min = 999999
        for i in values:
            if i < min:
                min = i

        return min

    except:
        print("Invalid input. Please enter a list/array of numbers.")
        return None


def meanValue(values):
    '''
    purpose:
        - find the mean value in the list

    arguments:
        - values: a list of numbers

    returns:
        - the mean value in the list
    '''

    try:
        # find the mean value in the list and return
        sum = 0
        length = 0

        for i in values:
            sum += i
            length += 1

        return sum / length

    except TypeError:
        print("Invalid input. Please enter a list/array of numbers.")
        return None


def countValue(values,xw):
    '''
    purpose:
        - count the number of times xw appears in the list

    arguments:
        - values: a list of numbers

    returns:
        - the number of times xw appears in the list
    '''

    counter, index = 0, 0

    # count the number of times xw appears in the list and return
    length = 0
    for i in values:
        length += 1

    while True:
        if values != "":
            if index <= length:
                print(index)
                if xw in values[:index]:
                    counter += 1
                    values = values[index:]
                    index = 0
                else:
                    index += 1
            else:
                break
        else:
            break
            
    return counter
    
if __name__ == "__main__":
    a = countValue("wrwrwrrwr", "wr")
    print("a")
    b = countValue("hello world", "o")
    print("b")
    c = countValue("this is a sentence", " ")
    print("done")
    print(a)
    print(b)
    print(c)