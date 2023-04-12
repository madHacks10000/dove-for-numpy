#dove.numpy
#in other file: import dove.numpy as np
#logistic regression
#zeros, dot, sum, exp, array


opNum = 0 #total number of operations
TRANSCRIPT = "transcript.txt"
file = open(TRANSCRIPT, "w")

def zeros(shape): #shape is int or tuple of ints
    if isinstance(shape, int): #1D array
        file.write("def ${} [1:1] [1:{}]".format(opNum, shape))
    else: #2D
        file.write("def ${} [1:{}] [1:{}]".format(opNum, shape[1], shape[2])) 
    file.write("== #0")
    file.write("end ${}".format(opNum))
    opNum += 1


def dot(item1, item2): #add cases for 1D vs 2D
    file.write("def ${} [1:{}] [1:{}]".format(opNum, shape[1], shape[2]))
    file.write("\t== ${} * ${}".format(opNum))
    file.write("end ${}".format(opNum))
    opNum += 1


def sum(arr): # elements to sum, takes in array???
    file.write("sum ${} ${}".format(opNum))
    file.write("set ${}".format(opNum))
    opNum += 1

def exp(values):
    file.write("def ${} [1:{}] [1:{}]".format(opNum, values.rows, values.columns))
    file.write("\t exp ${}".format(values.id))
    file.write("end ${}".format(opNum))
    opNum += 1

def array(data):
    file.write("def ${} [1:{}] [1:{}]".format(opNum, data.rows, data.columns))
    file.write("\t dataset data ${}".format(values.id)) #??????????
    file.write("end ${}".format(opNum))
    opNum += 1



    
    
    
