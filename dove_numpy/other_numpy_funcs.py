#other dove_numpy functions

#Adaboost- ones, full, unique, log, sign$
def ones(shape): #shape is int or tuple of ints
    if isinstance(shape, int): #1D array
        m = Matrix(1, shape, None, "==") 
    else: #2D
        m = Matrix(shape[0], shape[1], None, "==") 
    print("#1\nend ${}".format(m.iD)) #file.write

def full(shape, fill): #Return a new array of given shape and type, filled with fill_value
    if isinstance(shape, int): #1D array
        m = Matrix.modify_matrix(1, shape, None, "==") 
        print("#{}\nend ${}".format(fill, opNum)) 
    else: #2D
        m = Matrix.modify_matrix(shape[0], shape[1], None, "==") #first create matrix
        print("#{}\nend ${}".format(fill, opNum)) 
        print("forloop [{}:{}:{}] \{}".format(0, shape[0], 1, opNum)) #might need separate counter for loops
        print("update ${} [\{}] [\{}] %{}".format(m.iD, opNum, opNum, fill)) 
        print("endloop \{}".format(opNum))
    return m

def log(arr): #natural log, base e... 
    if type(arr) != Matrix: #if argument is a normal array
        m = Matrix(1, len(other), "external for now", "none")
    else:
        m = arr
    tmp = Matrix.modify_matrix(m, None, "^")
    print("set ${}".format(tmp.iD)) 
    print("update exp {} ${}".format("e", arr.iD)) #modify exp to allow different bases
    return tmp

def unique(arr):
    global opNum
    print("unique {}".format(arr.iD)) #new syntax, needs to be added to the backend
    opNum += 1
    print("set %{}".format())

def sign(num): #fix bc a singular value is still represented by like a matrix
    #if statement checking if it
    print("ifelse ${} #0".format(num.iD)) #ifelse %95 $52@(\18,1) %96
    print("set {}".format(opNum))
    print("update {}".format(num.iD)) #see note!!

#Decision tree- bincount, log2, random.choice, wrgwhere

def bincount(arr): #count occurence of each value in array
    #could definitely use the "unique" syntax
    m = Matrix(1, 1, None, None)
    m.modify_matrix(None, arr, "unique") #signifies to backend to be unique value of array and store it
    for i in range(len(m)):
        print("")
        #add body
    return m

def log2(arr): #base 2
    m = Matrix.modify_matrix("2", arr, "log") #base 2
    return m

#def random_choice(inp): generates a random sample from a given 1-D array

#Kmeans- random.seed, sqrt, random.choice, empty, argmin, mean

def sqrt(arr):
    if type(item2) == type(None):
        m = Matrix(item1.shape[0], item1.shape[1], 'placeholder', None) #taking in numpy nd array
        m = Matrix(item1.shape[0], item1.shape[1], 'placeholder', None)
    #now actual dot operations
    mn = Matrix.modify_matrix(m, 0.5, "^")
    return mn

def empty(arr):
    if isinstance(shape, int): #1D array
        m = Matrix(1, shape, None, "empty") #file.write("def ${} [1:1] [1:{}]".format(opNum, shape))
    else: #2D
        m = Matrix(shape[0], shape[1], None, "empty") #file.write("def ${} [1:{}] [1:{}]".format(opNum, shape[1], shape[2])) 
    print("\nend ${}".format(m.iD)) #file.write

def argmin(arr): #Returns the indices of the minimum values along an axis.
    min = arr[i]
    for i in range(len(arr)):
        if arr[i] < min:
            min = arr[i]














#Knn- argsort
#Ida- linalg.inv, linalg.eig
#Linear regression- corrcoef
#load_data- float32, loadtxt, genfromtxt, asarray
#naivebytes- argmax
#Pca- cov
#perceptron- where, amin, amax 
#random forests- swapaxes