# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification


def sumValues(values):
    """Your documentation goes here"""    
    sum = 0
    for i in values:
        sum += i

    return sum


def maxValue(values):
    """Your documentation goes here"""    
    max = -99999
    for i in values:
        if i > max:
            max = i
    return max


def minValue(values):
    """Your documentation goes here"""    
    min = 999999
    for i in values:
        if i < min:
            min = i
    return min


def meanValue(values):
    """Your documentation goes here"""    
    return sum(values) / len(values)


def countValue(values,xw):
    """Your documentation goes here"""  
    counter, index = 0, 0

    while True:
        print(f"counter:{counter} index:{index}")
        print(values[index:])
        if xw in values[index:]:
            counter += 1
            index = values.index(xw, index) + 1
        else:
            break
    return counter
