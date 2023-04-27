#dove.numpy
#in other file: import dove.numpy as np
#logistic regression
#zeros, dot, sum, exp, array
#import numpy as np

opNum = 1 #total number of operations
loop_indx = 1 #renam
reg_num = 1
TRANSCRIPT = "transcript.txt"
file = open(TRANSCRIPT, "w")

class Register():
    def __init__(self, value):
        self.iD = reg_num
        self.value = value
    
    def modify_register(self, operation, operand):
        print("do something")  
        print("set %{}".format(self.iD))

    class ForIndex(Register):
        def __init__(self, value):
            self.iD = loop_indx
    
    #soon, overload add, sub, etc


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
            if type(operand) == type(None): 
                tmp = self
                return tmp 
            elif (type(operand) == int) or (type(operand) == float):
                tmp = Matrix(self.shape[0], self.shape[1], None, operation) #should be 455, 30
                print("${} #{}\nend ${}".format(self.iD, operand, tmp.iD))
            else:
                tmp = Matrix(self.shape[0], operand.shape[1], None, operation) #should be 455, 30
                print("${} ${}\nend ${}".format(self.iD, operand.iD, tmp.iD)) 
        else:
            if type(operand) == type(None): 
                tmp = self
                return tmp
            elif (type(operand) == int) or (type(operand) == float): #adding a constant
                tmp = Matrix(self.row, self.col, None, operation)
                print("${} #{}\nend ${}".format(self.iD, operand, tmp.iD))
            elif (type(self) == int) or (type(self) == float):
                tmp = Matrix(operand.row, operand.col, None, operation)
                print("#{} ${}\nend ${}".format(self, operand.iD, tmp.iD))
            else: #might need another case where both operands are integers
                tmp = Matrix(self.row, self.col, None, operation)
                print("${} ${}\nend ${}".format(self.iD, operand.iD, tmp.iD)) 
        return tmp
    
def __add__(self, other): #overload addition operator
    return Matrix.modifyMatrix(self, other, '+')

def __sub__(self, other): #overload addition operator
    if type(self) == type(None):
        self = 0
    elif type(other) == type(None):
        other = 0

    if type(other) != Matrix: #need to add more cases
            if type(other) == int:
                other = other
            else: #it is a ndarray that needs to be converted
                other = Matrix(1, len(other), "external for now", "none") #make ndarray into a Matrix, can't alwas hardcode 1
    return Matrix.modifyMatrix(self, other, '-')

def __rsub__(self, other):
    if type(self) == type(None):
        self = 0
        #return negated matrix
    elif type(other) == type(None):
        other = 0
        #return negated matrix

    if type(other) != Matrix: #need to add more cases
            if type(other) == int:
                other = other
            else: #ndarray that needs to be converted
                other = Matrix(1, len(other), "external for now", "none") #make ndarray into a Matrix, can't alwas hardcode 1
            
    return Matrix.modifyMatrix(self, other, '-')
    
def __radd__(self, other): #overload addition operator
    return Matrix.modifyMatrix(self, other, '+')

def __mul__(self, other): #overload multiplication operator
    return Matrix.modifyMatrix(self, other, '*')

def __rmul__(self, other): #overload multiplication operator
    return Matrix.modifyMatrix(self, other, '*')

def __div__(self, other): #overload multiplication operator
    return Matrix.modifyMatrix(self, other, '/')

def __rtruediv__(self, other): #overload multiplication operator
    return Matrix.modifyMatrix(self, other, '/')

def __rfloordiv__(self, other): #overload multiplication operator
    return Matrix.modifyMatrix(self, other, '/')

def __neg__(self):
    return Matrix.modifyMatrix(self, -1, '*')

#np.for_loop(0, len(y_predicted), 1, lambda i: (
#np.if_else(y_predicted[i] > 0.5, 1, 0, y_predicted[i])

def for_loop(start, obj, step, func): #see DOVE
    global opNum
    global loop_indx
    opNum += 1
    index_var = Register.ForIndex
    print("forloop [{}:{}:{}] \{}".format(start, obj, step, index_var.iD)) #creates new forindex variable
    func(index_var)
    print("endloop \{}".format(loop_indx))


def if_else(cond, path_one, path_two): #optional arg for value i in case this is in a for loop
    global opNum
    global reg_num #global counter for registers
    #line 37ish in if
    #wrap if true and if false
    #result = if.false
    print("condition in string form") #how to correctly output condition?
    #other condition?
    if type(path_two) == type(None):
        print("select %{} {} {}".format(reg_num, path_one, reg_num))
        #set as a register
        #technically the else condition is like x = x... need to be explicit here??
    else:
        print("select %{} {} {} {}".format(reg_num, path_one, reg_num, path_two))

    print("ifelse {} {} {}".format()) #condition, value
    #save result in like %2
    print("update y i %2")
    

def zeros(shape): #shape is int or tuple of ints
    if isinstance(shape, int): #1D array
        m = Matrix(1, shape, None, "==") #file.write("def ${} [1:1] [1:{}]".format(opNum, shape))
    else: #2D
        m = Matrix(shape[0], shape[1], None, "==") #file.write("def ${} [1:{}] [1:{}]".format(opNum, shape[1], shape[2])) 
    print("#0\nend ${}".format(m.iD)) #file.write

def dot(item1, item2): 
    if type(item2) == type(None):
        m = Matrix(item1.shape[0], item1.shape[1], 'placeholder', None) #taking in numpy nd array
        n = None
    else:
        m = Matrix(item1.shape[0], item1.shape[1], 'placeholder', None)
        n = Matrix(item2.shape[0], item2.shape[1], 'placeholder', None)
    #now actual dot operations
    mn = Matrix.modifyMatrix(m, n, "*")
    return mn

def sum(arr): #elements to sum, takes in array
    global opNum
    print("sum ${}".format(arr.iD))
    print("set %{}".format(opNum))
    return opNum
    #print("update ${}".format(opNum)) don't think I need this

def exp(values): #values is a Matrix
    tmp = Matrix.modifyMatrix(values, None, "^")
    print("set ${}".format(tmp.iD)) #<--def needs some fixing
    print("update exp ${}".format(values.iD))
    return tmp

#def array(data): #can accept like any object... add options later
    #if isinstance(data, int): #1D array
        #m = Matrix(1, shape, None, "==") #file.write("def ${} [1:1] [1:{}]".format(opNum, shape))
    #else: #2D
        #m = Matrix(data[0], data[1], None, "==") #file.write("def ${} [1:{}] [1:{}]".format(opNum, shape[1], shape[2])) 
    #print("#0\nend ${}".format(opNum)) #file.write

#deal with ifelse statements

    
    
    
    
    
