#other dove_numpy functions

#Adaboost- ones, full, unique, log, sign

def ones(shape): #shape is int or tuple of ints
    if isinstance(shape, int): #1D array
        m = Matrix(1, shape, None, "==") 
    else: #2D
        m = Matrix(shape[0], shape[1], None, "==")
    print("#1\nend ${}".format(opNum)) #file.write

def full(shape): #shape is int or tuple of ints
    if isinstance(shape, int): #1D array
        m = Matrix(1, shape, None, "==") 
    else: #2D
        m = Matrix(shape[0], shape[1], None, "==")
    print("#{}\nend ${}".format(fill_value, opNum)) #fill value??

def log(arr): #natural log, base e... add syntax for this
    m = Matrix.modifyMatrix("e", arr, "log") #modify slightly... see what log functionality the use
    return m

def unique(arr):
    #loop structure and if statement to go through arr
    #maybe add syntax
    global opNum
    print("unique {}".format(arr.iD))
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
    m.modifyMatrix(None, arr, "unique") #signifies to backend to be unique value of array and store it
    return m

def log2(arr): #base 2
    m = Matrix.modifyMatrix("2", arr, "log") #base 2
    return m

#Kmeans- random.seed, swrt, random.choice, empty, argmin, mean
#Knn- argsort
#Ida- linalg.inv, linalg.eig
#Linear regression- corrcoef
#load_data- float32, loadtxt, genfromtxt, asarray
#naivebytes- argmax
#Pca- cov
#perceptron- where, amin, amax 
#random forests- swapaxes