#dove.numpy
#in other file: import dove.numpy as np
#logistic regression
#zeros, dot, sum, exp, array
import numpy as np

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
        self.shape = (row, col)
        self.operation = operation
        opNum += 1
        if self.name == None: #matrix will be modified as specified later on in the user's program
            print("def ${} [1:{}] [1:{}]\n\t{} ".format(self.iD, self.row, self.col, self.operation), end = ' ')
        else: #case where external data is used... I think
             print("def ${} [1:{}] [1:{}]\n\tdataset {}\nend ${}".format(self.iD, self.row, self.col, self.name, self.iD))

    def modifyMatrix(self, operand, operation):
        global opNum
        if operation == "*": #dot product
            if type(operand) == type(None): #how to deal with this???
                #n = 'None'
                #opNum += 1
                #tmp = Matrix(self.shape[0], self.shape[1], None, operation)
                #print("${} \nend ${}".format(self.iD, opNum))
                tmp = self
                return tmp #dot product of a matrix with nothing is just the matrix
            elif type(operand) == int:
                tmp = Matrix(self.shape[0], self.shape[1], None, operation) #should be 455, 30
                print("${} #{}\nend ${}".format(self.iD, operand, tmp.iD))
            else:
                tmp = Matrix(self.shape[0], operand.shape[1], None, operation) #should be 455, 30
                print("${} ${}\nend ${}".format(self.iD, operand.iD, tmp.iD)) 
        else:
            if type(operand) == type(None): #how to deal with this???
                #n = 'None'
                #opNum += 1
                #tmp = Matrix(self.shape[0], self.shape[1], None, operation)
                #print("${} \nend ${}".format(self.iD, opNum))
                tmp = self
                return tmp
            elif type(operand) == int: #adding a constant
                tmp = Matrix(self.row, self.col, None, operation)
                print("${} #{}\nend ${}".format(self.iD, operand, tmp.iD))
            elif type(self) == int:
                tmp = Matrix(operand.row, operand.col, None, operation)
                print("#{} ${}\nend ${}".format(self, operand.iD, tmp.iD))
            else: #might need another case where both operands are integers
                tmp = Matrix(self.row, self.col, None, operation)
                print("${} ${}\nend ${}".format(self.iD, operand.iD, tmp.iD)) 
        return tmp
    
    def __add__(self, other): #overload addition operator
        return Matrix.modifyMatrix(self, other, '+')
    
    def __radd__(self, other): #overload addition operator
        return Matrix.modifyMatrix(self, other, '+')
    
    def __mul__(self, other): #overload multiplication operator
        return Matrix.modifyMatrix(self, other, '*')

    def __div__(self, other): #overload multiplication operator
        return Matrix.modifyMatrix(self, other, '/')

    #def __rdiv__(self, other): #overload addition operator <---outdated
        #return Matrix.modifyMatrix(self, other, '/')

    def __rtruediv__(self, other): #overload multiplication operator
        return Matrix.modifyMatrix(self, other, '/')
    
    def __rfloordiv__(self, other): #overload multiplication operator
        return Matrix.modifyMatrix(self, other, '/')

    def __neg__(self):
        return Matrix.modifyMatrix(self, -1, '*')

def zeros(shape): #shape is int or tuple of ints
    if isinstance(shape, int): #1D array
        m = Matrix(1, shape, None, "==") #file.write("def ${} [1:1] [1:{}]".format(opNum, shape))
    else: #2D
        m = Matrix(shape[0], shape[1], None, "==") #file.write("def ${} [1:{}] [1:{}]".format(opNum, shape[1], shape[2])) 
    print("#0\nend ${}".format(m.iD)) #file.write

def dot(item1, item2): #need to convert inputs into my matrices!!!!!!!!
    #logistic regression: 2D matrix then 'None'
    #print("item 1: {}".format(item1))
    #print("item 2: {}".format(item2))
    if type(item2) == type(None):
        m = Matrix(item1.shape[0], item1.shape[1], 'placeholder', None) #taking in numpy nd array
        n = None
    else:
        #m = Matrix.modifyMatrix(item1, item2, "*")
        m = Matrix(item1.shape[0], item1.shape[1], 'placeholder', None)
        n = Matrix(item2.shape[0], item2.shape[1], 'placeholder', None)
    #now actual dot operations
    mn = Matrix.modifyMatrix(m, n, "*")
    return mn


def sum(arr): #elements to sum, takes in array???
    global opNum
    opNum += 1
    print("sum ${}".format(arr.iD))
    print("set ${}".format(opNum))
    #print("update ${}".format(opNum)) don't think I need this

def exp(values): #values is a Matrix
    tmp = Matrix.modifyMatrix(values, None, "^")
    print("set ${}".format(tmp.iD))
    print("update exp ${}".format(values.iD))
    return tmp

#def array(data): #can accept like any object... add options later
    #if isinstance(data, int): #1D array
        #m = Matrix(1, shape, None, "==") #file.write("def ${} [1:1] [1:{}]".format(opNum, shape))
    #else: #2D
        #m = Matrix(data[0], data[1], None, "==") #file.write("def ${} [1:{}] [1:{}]".format(opNum, shape[1], shape[2])) 
    #print("#0\nend ${}".format(opNum)) #file.write


    
    
    
    
    
