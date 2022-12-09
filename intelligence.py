from skimage import io
import numpy as np


filename = "data/map.png"


def find_red_pixels(*args,**kwargs):
    """
    filename: the name of the file is stored within the args variable
    upper_threshold: rgb need to be higher than this value to accept the pixel
    lower_threshold: rgb need to be lower than this value to accept the pixel

    returns: a 2d array of the numpy form of a list of red pixels within the given image
    
    """
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
    """
    filename: the name of the file is stored within the args variable
    upper_threshold: rgb need to be higher than this value to accept the pixel
    lower_threshold: rgb need to be lower than this value to accept the pixel

    returns: a 2d array of the numpy form of a list of cyan pixels within the given image
    
    """
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


def detect_connected_components2(*args, **kwargs):
    arr = args[0]
    HEIGHT = len(arr)
    WIDTH = len(arr[0])

    visited = np.zeros(shape=(HEIGHT, WIDTH), dtype=int)
    tovisit = np.ndarray(shape=(0, 2), dtype=int)
    components_counter = []
    component_counter = 1
    pixel_counter = 0

    for i in range(HEIGHT):
        for j in range(WIDTH):
            print(f"{i} : {j}")
            if arr[i][j] == 1 and visited[i][j] == 0:
                visited[i][j] = component_counter   
                tovisit = np.resize(tovisit, (tovisit.shape[0] + 1, tovisit.shape[1])) # resize to array to fit one more element
                tovisit[-1] = [i, j] 
                pixel_counter = 1

                while tovisit.tolist() != []:
                    x, y = tovisit[0] # grab the first element
                    tovisit = np.ndarray(shape=(tovisit.shape[0] -1, tovisit.shape[1]), buffer=np.asarray([tovisit[1:]]), dtype=int) # create a new tovisit array exluding the first element
                    for k in range(-1, 2): # up and down 
                        for l in range(-1, 2): # left and right
                            if x+k >= 0 and x+k < len(arr) and y+l >= 0 and y+l < len(arr[0]): # check if the pixel around is in bounds
                                if arr[x+k][y+l] == 1 and visited[x+k][y+l] == 0: # check if the pixel is a path pixel and also is not yet visited
                                    visited[x+k][y+l] = component_counter
                                    tovisit = np.resize(tovisit, (tovisit.shape[0] + 1, tovisit.shape[1])) # reshape the queue to make space for this new pixel
                                    tovisit[-1] = [x+k,y+l] # add this new pixel to the queue to be iterated over a 2x2 area
                                    pixel_counter += 1 # one more additional pixel that is connected in this component, keep track of this
                components_counter.append(pixel_counter)
                with open("./data/output/cc-output-2a.txt", "a") as f: # open file in append mode  
                    print(f"connected component {component_counter}, number of pixels = {pixel_counter}")  
                    f.writelines([f"connected component {component_counter}, number of pixels = {pixel_counter}\n"])
                component_counter += 1

    with open("./data/output/cc-output-2a.txt", "a") as f: # open the file in append mode
        print(f"Total number of connected components = {len(components_counter)}\n") # output total number of components
        f.writelines([f"Total number of connected components = {len(components_counter)}\n"])

    return visited



def detect_connected_components(*args, **kwargs):
    """
    args: an array of the image, using 1 as a path pixel and 0 as an empty pixel
    does: finds all the components within a 1 bit depth image and places all of the components into a file
          assumes that a path pixel is a 1 and an empty pixel is a 0
    returns: None
    """
    arr = args[0] # create local varibale of the image as an array
    HEIGHT = len(arr) # constant height variable
    WIDTH = len(arr[0]) # constant width variabel

    visited = [] # visited pixels, not to be visited again

    tovisit = np.ndarray(shape=(0, 2), dtype=int) # list of pixels to be inspected in all 8 directions

    components_counter = [] # list relevant to the pixel number in each component, the index references also the component number
    counter = 0 # counter of number of pixels in component
    
    #implement a flood fill noting down how many elements there are 

    for i in range(len(arr)): # iterate over each row in the pixel image
        for j in range(len(arr[i])): # iterate over each column in each row in the pixel image
            if arr[i][j] == 1 and [i, j] not in visited: # if the pixel is a path pixel and pixel is not visited yet then 
                visited.append([i, j]) # add pixel to visited pixels so it does not get visited again
                tovisit = np.resize(tovisit, (tovisit.shape[0] + 1, tovisit.shape[1])) # resize to array to fit one more element
                tovisit[-1] = [i, j] # set the element to the new created space generated in the line above
                counter = 1 # set counter to one for that one visited element

                while tovisit.tolist() != []: # go through all adjacent elements of that pixel iteratively until none are left
                    # pop the first element of the ndarray
                    x, y = tovisit[0] # grab the first element
                    tovisit = np.ndarray(shape=(tovisit.shape[0] -1, tovisit.shape[1]), buffer=np.asarray([tovisit[1:]]), dtype=int) # create a new tovisit array exluding the first element
                    
                    # check 3x3 square around the pixel
                    for k in range(-1, 2): # up and down 
                        for l in range(-1, 2): # left and right
                            if x+k >= 0 and x+k < len(arr) and y+l >= 0 and y+l < len(arr[0]): # check if the pixel around is in bounds
                                if arr[x+k][y+l] == 1 and [x+k, y+l] not in visited: # check if the pixel is a path pixel and also is not yet visited
                                    visited.append([x+k,y+l]) # add this pixel to visited pixels
                                    tovisit = np.resize(tovisit, (tovisit.shape[0] + 1, tovisit.shape[1])) # reshape the queue to make space for this new pixel
                                    tovisit[-1] = [x+k,y+l] # add this new pixel to the queue to be iterated over a 2x2 area
                                    counter += 1 # one more additional pixel that is connected in this component, keep track of this
                    
                components_counter.append(counter) # when the component is finished then add the amount of pixels in the componenet to an array
                with open("./data/output/cc-output-2a.txt", "a") as f: # open file in append mode    
                    f.writelines([f"connected component {len(components_counter)}, number of pixels = {components_counter[-1]}\n"]) # write the componenet number and how many pixels it contains to the file
                print(f"connected component {len(components_counter)}, number of pixels = {components_counter[-1]}") # print out the component number and its number of pixels
    with open("./data/output/cc-output-2a.txt", "a") as f: # open the file in append mode
        print(f"Total number of connected components = {len(components_counter)}\n") # output total number of components
        f.writelines([f"Total number of connected components = {len(components_counter)}\n"]) # write the final line counting how many components there are in total
    return np.asarray(components_counter)

def detect_connected_components_sorted(*args,**kwargs):
    """
    does: opens the cc-output-2a.txt file and grabs all of the components placing them into a dictionary, then sorts them by number of pixels and places back into another file 
          called cc-output-2b.txt
    """
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
    for key, value in zip(keys, values): # for every component, but this time sorted
        with open("./data/output/cc-output-2b.txt", "a") as f: # open file temporarily
            f.writelines([f"Connected Component {str(key)}, number of pixels = {str(value)}\n"]) # add the component and how many pixels it has into file
        sorted_dict.setdefault(key, value) # create a dictionary that is sorted

    # add total number of components to file
    with open("./data/output/cc-output-2b.txt", "a") as f: # open file temporarily
        f.writelines([f"Total number of connected components = {len(dict)}\n"]) # add total amount of components to file

    # add top two components into file
    with open("./data/output/cc-top-2.txt", "a") as f: # open file temporarily
        f.writelines([f"Connected Component {str(keys[0])}, number of pixels = {str(values[0])}\n"]) # add component with most pixels to file
        f.writelines([f"Connected Component {str(keys[1])}, number of pixels = {str(values[1])}\n"]) # add component with second most pixels to file




if __name__ == "__main__":
    red = find_red_pixels("./data/map.png", upper_threshold=100, lower_threshold=50)
    # cyan = find_cyan_pixels("./data/map.png", upper_threshold=100, lower_threshold=50)

    #mark = detect_connected_components2(red)
    # detect_connected_components_sorted(mark)

