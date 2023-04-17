#dove.numpy
#in other file: import dove.numpy as np
#logistic regression
#zeros, dot, sum, exp, array

opNum = 1 #total number of operations
TRANSCRIPT = "transcript.txt"
file = open(TRANSCRIPT, "w")

class Matrix():
    def __init__(self, row, col, name = None, operation = None):
        global opNum
        self.name = name
        self.iD = opNum #need in addition to global variable
        self.row = row
        self.col = col
        self.operation = operation
        opNum += 1
        if self.name == None: #matrix will be modified as specified later on in the user's program
            print("def ${} [1:{}] [1:{}]\n\t{} ".format(opNum, self.row, self.col, self.operation), end = ' ')
        else: #case where external data is used... I think
             print("def ${} [1:{}] [1:{}]\n\tdataset {}\nend ${}".format(self.iD, self.row, self.col, self.name, self.iD))

    def modifyMatrix(self, operand, operation):
        tmp = Matrix(self.row, self.col, None, operation)
        print("${} ${}\nend ${}".format(self.iD, operand.iD, tmp.iD)) 
        return tmp

def zeros(shape): #shape is int or tuple of ints
    global opNum
    if isinstance(shape, int): #1D array
        m = Matrix(1, shape, None, None) #file.write("def ${} [1:1] [1:{}]".format(opNum, shape))
    else: #2D
        m = Matrix(shape[1], shape[2], None, None) #file.write("def ${} [1:{}] [1:{}]".format(opNum, shape[1], shape[2])) 
    print("\n\t== #0") #file.write
    print("\nend ${}".format(opNum))
    opNum += 1

def dot(item1, item2): #add cases for 1D vs 2D
    m = Matrix.modifyMatrix(item1, item2, "*")
    return m

def dot2(item1, item2):
    Matrix.modifyMatrix(item1, item2, "*")

def sum(arr): # elements to sum, takes in array???
    global opNum
    print("sum ${}".format(arr.iD))
    print("set ${}".format(opNum))
    opNum += 1

#def exp(values):
    #new = Matrix(values.rows, values.columns, none, none)
    #new.modifyMatrix(, self, "^") <--- how to represent e???
    #file.write("\t exp ${}".format(values.id))
    #opNum += 1

#def array(data):
    #new = Matrix()
    #file.write("\t dataset data ${}".format(values.id)) #??????????
    #file.write("end ${}".format(opNum))
    #opNum += 1

#test code
#test1 = Matrix(2, 2, "test1")
#test2 = Matrix(2, 2, "test2")

#dotproduct = dot(test1, test2)
#zeromatrix = zeros((2, 1))
#sum = sum([2, 1], [3, 4])
#dotproduct2 = dot2(test1, test2) 
    
    
    
    
    
