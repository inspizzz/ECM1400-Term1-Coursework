from skimage import io
import numpy as np


def find_red_pixels(*args,**kwargs):
    '''
    purpose:   
        - finds red pixels in a given image with a range of limits

    arguments:
        - filename: the name of the file contains the image
        - upper_threshold: rgb need to be higher than this value to accept the pixel
        - lower_threshold: rgb need to be lower than this value to accept the pixel

    returns:
        - a 2d array of the numpy form of a list of red pixels within the given image
    '''

    UpperThreshold = kwargs["upper_threshold"]
    LowerThreshold = kwargs["lower_threshold"]
    FileName = str(args[0])

    img = io.imread(FileName)

    arr = []

    for i in img:
        line = []
        for j in i:
            if j[0] > UpperThreshold and j[1] < LowerThreshold and j[2] < LowerThreshold:
                line.append(1)
            else:
                line.append(0)
        arr.append(line)
    io.imsave("./data/map-red-pixels.jpg", np.asarray(arr))
    return np.asarray(arr)
                

def find_cyan_pixels(*args,**kwargs):
    '''
    purpose:   
        - finds cyan pixels in a given image with a range of limits

    arguments:
        - filename: the name of the file contains the image
        - upper_threshold: rgb need to be higher than this value to accept the pixel
        - lower_threshold: rgb need to be lower than this value to accept the pixel

    returns:
        - a 2d array of the numpy form of a list of cyan pixels within the given image
    '''

    UpperThreshold = kwargs["upper_threshold"]
    LowerThreshold = kwargs["lower_threshold"]
    FileName = str(args[0])

    img = io.imread(FileName)

    arr = []

    for i in img:
        line = []
        for j in i:
            if j[0] < LowerThreshold and j[1] > UpperThreshold and j[2] > UpperThreshold:
                line.append(1)
            else:
                line.append(0)
        arr.append(line)
    io.imsave("./data/map-cyan-pixels.jpg", np.asarray(arr))
    return np.asarray(arr)


def detect_connected_components(*args):
    '''
    purpose:   
        - locates connected components in a 2d array, generates a 2d array of the same size with the connected components marked using different number

    improvements:
        - instead of marking each component with a 1, the component is marked with a number that represents its corresponding number
        - checks added for when a pixel is out of bounds, especially when the pixel is at the edge of the image

    arguments:
        - args: a 2d array of the image at index 0

    returns:
        - a 2d array of the same size as the input array with the connected components marked with different numbers
    '''

    arr = args[0]
    HEIGHT = len(arr)
    WIDTH = len(arr[0])

    MARK = np.zeros(shape=(HEIGHT, WIDTH), dtype=int)
    QUEUE = np.ndarray(shape=(0, 2), dtype=int)
    
    components_counter = []
    component_counter = 1
    pixel_counter = 0

    for i in range(HEIGHT):
        for j in range(WIDTH):
            print(f"{i} : {j}")
            if arr[i][j] == 1 and MARK[i][j] == 0:
                MARK[i][j] = component_counter   
                QUEUE = np.resize(QUEUE, (QUEUE.shape[0] + 1, QUEUE.shape[1])) # resize to array to fit one more element
                QUEUE[-1] = [i, j] 
                pixel_counter = 1

                while QUEUE.tolist() != []:
                    x, y = QUEUE[0] # grab the first element
                    QUEUE = np.ndarray(shape=(QUEUE.shape[0] -1, QUEUE.shape[1]), buffer=np.asarray([QUEUE[1:]]), dtype=int) # create a new QUEUE array exluding the first element
                    for k in range(-1, 2): # up and down 
                        for l in range(-1, 2): # left and right
                            if x+k >= 0 and x+k < len(arr) and y+l >= 0 and y+l < len(arr[0]): # check if the pixel around is in bounds
                                if arr[x+k][y+l] == 1 and MARK[x+k][y+l] == 0: # check if the pixel is a path pixel and also is not yet MARK
                                    MARK[x+k][y+l] = component_counter
                                    QUEUE = np.resize(QUEUE, (QUEUE.shape[0] + 1, QUEUE.shape[1])) # reshape the queue to make space for this new pixel
                                    QUEUE[-1] = [x+k,y+l] # add this new pixel to the queue to be iterated over a 2x2 area
                                    pixel_counter += 1 # one more additional pixel that is connected in this component, keep track of this
                components_counter.append(pixel_counter)
                with open("./data/output/cc-output-2a.txt", "a") as f: # open file in append mode  
                    print(f"connected component {component_counter}, number of pixels = {pixel_counter}")  
                    f.writelines([f"connected component {component_counter}, number of pixels = {pixel_counter}\n"])
                component_counter += 1

    with open("./data/output/cc-output-2a.txt", "a") as f: # open the file in append mode
        print(f"Total number of connected components = {len(components_counter)}\n") # output total number of components
        f.writelines([f"Total number of connected components = {len(components_counter)}\n"])

    return MARK


def detect_connected_components_sorted(*args):
    '''
    purpose:   
        - sorts a 2d array of connected components by size

    arguments:
        - args: a 2d array of connected components at index 0

    returns:
        - sorted_dict: a dictionary of the sorted connected components
    '''

    dict = {} # empty dictionary
    sorted_dict = {} # empty dictionary for sorted values and keys

    for i in args[0]:
        for j in i:
            if j != 0:
                if j in dict.keys():
                    dict[j] += 1
                else:
                    dict.setdefault(j, 1)
    
    # sort the dictionary 
    keys = list(dict.keys()) # seperate array for the dictionaries key
    values = list(dict.values()) # seperate array for the dictionaries values

    for i in range(len(values)): # for the length of values
        sorted = True # sorted is by default True
        for j in range(len(values) - i - 1): # go over the list but every time a switch is made then go one element smaller as this is unnecessary computation
            if values[j] < values[j+1]: # if the value below is smaller
                keys[j], keys[j+1] = keys[j+1], keys[j] # switch keys around
                values[j], values[j+1] = values[j+1], values[j] # switch values around
                sorted = False # if a change was made then stay False
        if sorted: # once sorted, stop looping
            break # stop the loop
        
    # add information to file
    with open("./data/output/cc-output-2b.txt", "a") as f:
        for key, value in zip(keys, values): # for every component, but this time sorted
            f.writelines([f"Connected Component {str(key)}, number of pixels = {str(value)}\n"]) # add the component and how many pixels it has into file
            sorted_dict.setdefault(key, value) # create a dictionary that is sorted
        f.writelines([f"Total number of connected components = {len(dict)}\n"]) # add total amount of components to file

    # add top two components into file
    with open("./data/output/cc-top-2.txt", "a") as f: # open file temporarily
        print(f"Connected Component {str(keys[0])}, number of pixels = {str(values[0])}")
        print(f"Connected Component {str(keys[1])}, number of pixels = {str(values[1])}")
        f.writelines([f"Connected Component {str(keys[0])}, number of pixels = {str(values[0])}\n"]) # add component with most pixels to file
        f.writelines([f"Connected Component {str(keys[1])}, number of pixels = {str(values[1])}\n"]) # add component with second most pixels to file

    return sorted_dict

if __name__ == "__main__":
    red = find_red_pixels("./data/map.png", upper_threshold=100, lower_threshold=50)
    mark = detect_connected_components(red)
    detect_connected_components_sorted(mark)

    cyan = find_cyan_pixels("./data/map.png", upper_threshold=100, lower_threshold=50)
    mark = detect_connected_components(cyan)
    detect_connected_components_sorted(mark)

