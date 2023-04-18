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
            print("def ${} [1:{}] [1:{}]\n\t{} ".format(self.iD, self.row, self.col, self.operation), end = ' ')
        else: #case where external data is used... I think
             print("def ${} [1:{}] [1:{}]\n\tdataset {}\nend ${}".format(self.iD, self.row, self.col, self.name, self.iD))

    def modifyMatrix(self, operand, operation):
        tmp = Matrix(self.row, self.col, None, operation)
        print("${} ${}\nend ${}".format(self.iD, operand.iD, tmp.iD)) 
        return tmp

def zeros(shape): #shape is int or tuple of ints
    if isinstance(shape, int): #1D array
        m = Matrix(1, shape, None, "==") #file.write("def ${} [1:1] [1:{}]".format(opNum, shape))
    else: #2D
        m = Matrix(shape[0], shape[1], None, "==") #file.write("def ${} [1:{}] [1:{}]".format(opNum, shape[1], shape[2])) 
    print("#0\nend ${}".format(m.iD)) #file.write

def dot(item1, item2): #need to convert inputs into my matrices!!!!!!!!
    #logistic regression: 2D matrix then 'None'
    if item2 == 'None':
        m = Matrix(1, len(item1), None, "*") #taking in numpy nd array
    else:
        m = Matrix.modifyMatrix(item1, item2, "*")
    print("${} ${}\nend ${}".format(item1.iD, item2.iD, m.iD))
    return m

def sum(arr): #elements to sum, takes in array???
    global opNum
    opNum += 1
    print("sum ${}".format(arr.iD))
    print("set ${}".format(opNum))
    #print("update ${}".format(opNum)) don't think I need this

def exp(values): #math.exp function does this... can represent e
    #m = Matrix.modifyMatrix(, values, none, "^")
    global opNum
    opNum += 1
    print("set ${}".format(values.iD))
    print("update exp ${}".format(opNum))

#def array(data): #can accept like any object... add options later
    #if isinstance(data, int): #1D array
        #m = Matrix(1, shape, None, "==") #file.write("def ${} [1:1] [1:{}]".format(opNum, shape))
    #else: #2D
        #m = Matrix(data[0], data[1], None, "==") #file.write("def ${} [1:{}] [1:{}]".format(opNum, shape[1], shape[2])) 
    #print("#0\nend ${}".format(opNum)) #file.write


    
    
    
    
    
