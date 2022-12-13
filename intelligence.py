from skimage import io
import numpy as np


def find_red_pixels(upperThreshold:int, lowerThreshold:int, filename:str) -> np.ndarray: # done
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

    # read pixels from the image
    img = io.imread(filename)
    arr = []

    # find all the pixels that qualify as being red and add them to the new image variable called arr
    for i in img:
        line = []
        for j in i:
            if j[0] > upperThreshold and j[1] < lowerThreshold and j[2] < lowerThreshold:
                line.append(1)
            else:
                line.append(0)
        arr.append(line)

    # save the new image and return it
    io.imsave("./data/map-red-pixels.jpg", np.asarray(arr))
    return np.asarray(arr)
                

def find_cyan_pixels(upperThreshold:int, lowerThreshold:int, filename:str) -> np.ndarray: # done
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

    # read pixels from the image
    img = io.imread(filename)
    arr = []

    # find all the pixels that qualify as being cyan and add them to the new image variable called arr
    for i in img:
        line = []
        for j in i:
            if j[0] < lowerThreshold and j[1] > upperThreshold and j[2] > upperThreshold:
                line.append(1)
            else:
                line.append(0)
        arr.append(line)

    # save the new image and return it
    io.imsave("./data/map-cyan-pixels.jpg", np.asarray(arr))
    return np.asarray(arr)


def detect_connected_components(arr:list) -> list: # done
    '''
    purpose:   
        - locates connected components in a 2d array, generates a 2d array of the same size with the connected components marked using different number

    improvements:
        - instead of marking each component with a 1, thes component is marked with a number that represents its corresponding number
        - checks added for when a pixel is out of bounds, especially when the pixel is at the edge of the image

    arguments:
        - args: a 2d array of the image at index 0

    returns:
        - a 2d array of the same size as the input array with the connected components marked with different numbers
    '''
    
    # define the height and width of the image
    HEIGHT = len(arr)
    WIDTH = len(arr[0])

    # define mark and queue arrays as per the example code
    MARK = np.zeros(shape=(HEIGHT, WIDTH), dtype=int)
    QUEUE = np.ndarray(shape=(0, 2), dtype=int)
    
    # initiate couting variables
    components_counter = []
    component_counter = 1
    pixel_counter = 0

    # for every pixel if it is a path pixel find the whole path that it is connected to, logging these paths as they go by
    for i in range(HEIGHT):
        for j in range(WIDTH):

            # check if pixel is a path pixel and hasnt been seen by the algorithm yet
            if arr[i][j] == 1 and MARK[i][j] == 0:

                # mark it as a path pixel and add it to the queue to be processed to find more path pixels
                MARK[i][j] = component_counter   
                QUEUE = np.resize(QUEUE, (QUEUE.shape[0] + 1, QUEUE.shape[1]))
                QUEUE[-1] = [i, j] 
                pixel_counter = 1

                # while there are more path pixels adjacent to the current path pixel, keep iterating over them
                while QUEUE.tolist() != []:
                    x, y = QUEUE[0]
                    QUEUE = np.ndarray(shape=(QUEUE.shape[0] -1, QUEUE.shape[1]), buffer=np.asarray([QUEUE[1:]]), dtype=int) 
                    for k in range(-1, 2):
                        for l in range(-1, 2):

                            # check if the pixel is in bounds
                            if x+k >= 0 and x+k < len(arr) and y+l >= 0 and y+l < len(arr[0]):

                                # cehck if the pixel is a path pixel and hasnt been seen by the algorithm yet
                                if arr[x+k][y+l] == 1 and MARK[x+k][y+l] == 0:

                                    # mark it as a path pixel and add it to the queue to be processed to find more path pixels
                                    MARK[x+k][y+l] = component_counter
                                    QUEUE = np.resize(QUEUE, (QUEUE.shape[0] + 1, QUEUE.shape[1])) 
                                    QUEUE[-1] = [x+k,y+l]
                                    pixel_counter += 1

                # after the program is done with the current component, add the number of pixels for that component into the components_counter list
                components_counter.append(pixel_counter)

                # save to file as required by the specification
                with open("./data/output/cc-output-2a.txt", "a") as f:  
                    f.seek(0)
                    f.truncate()
                    print(f"connected component {component_counter}, number of pixels = {pixel_counter}")  
                    f.writelines([f"connected component {component_counter}, number of pixels = {pixel_counter}\n"])
                
                # increment the component counter
                component_counter += 1

    # save to file the total number of components as required by the specification
    with open("./data/output/cc-output-2a.txt", "a") as f:
        print(f"Total number of connected components = {len(components_counter)}\n")
        f.writelines([f"Total number of connected components = {len(components_counter)}\n"])

    return MARK


def detect_connected_components_sorted(mark:list) -> dict: # done
    '''
    purpose:   
        - sorts a 2d array of connected components by size

    arguments:
        - args: a 2d array of connected components at index 0

    returns:
        - sorted_dict: a dictionary of the sorted connected components
    '''

    # create variables 
    dict = {}
    sorted_dict = {}

    # structure the data into the dictionary
    for i in mark:
        for j in i:
            if j != 0:
                if j in dict.keys():
                    dict[j] += 1
                else:
                    dict.setdefault(j, 1)
    
    # seperate out the keys and the values of the dictionary
    keys = list(dict.keys())
    values = list(dict.values())

    # sort the keys of the dictionary moving the values as well
    for i in range(len(values)):
        sorted = True
        for j in range(len(values) - i - 1):
            if values[j] < values[j+1]:
                keys[j], keys[j+1] = keys[j+1], keys[j]
                values[j], values[j+1] = values[j+1], values[j]
                sorted = False
        if sorted:
            break
        
    # add information to file as required by the specification
    with open("./data/output/cc-output-2b.txt", "a") as f:
        for key, value in zip(keys, values):
            f.writelines([f"Connected Component {str(key)}, number of pixels = {str(value)}\n"])
            sorted_dict.setdefault(key, value)
        f.writelines([f"Total number of connected components = {len(dict)}\n"])

    # add top two components into file as required by the specification
    with open("./data/output/cc-top-2.txt", "a") as f:
        print(f"Connected Component {str(keys[0])}, number of pixels = {str(values[0])}")
        print(f"Connected Component {str(keys[1])}, number of pixels = {str(values[1])}")
        f.writelines([f"Connected Component {str(keys[0])}, number of pixels = {str(values[0])}\n"])
        f.writelines([f"Connected Component {str(keys[1])}, number of pixels = {str(values[1])}\n"])

    return sorted_dict

if __name__ == "__main__":
    red = find_red_pixels(filename="./data/map.png", upperThreshold=100, lowerThreshold=50)
    mark = detect_connected_components(red)
    detect_connected_components_sorted(mark)

    cyan = find_cyan_pixels(filename="./data/map.png", upperThreshold=100, lowerThreshold=50)
    mark = detect_connected_components(cyan)
    detect_connected_components_sorted(mark)

