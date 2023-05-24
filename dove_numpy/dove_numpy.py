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
    def __init__(self):
        global reg_num
        self.iD = reg_num
        reg_num += 1
    
    def modify_register(self):
        print("do something")  
        print("set %{}".format(self.iD))

    def __str__(self):
        print("{}{}d".format(0, 0)) #filler value for now
    
class Pointer():
    def __init__(self, name, row, col):
        self.name = name
        self.row = row
        self.col = col

    def __str__(self):
        print("${}@({},{})".format(self.iD, self.row, self.col))
    

class ForIndex():
    def __init__(self):
        global loop_indx
        self.iD = loop_indx
        loop_indx += 1

    def new_index(self):
        return ForIndex(self)

    def __repr__(self):
        return self.iD
    
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

    def __str__(self):
        return "${}".format(self.iD)

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
    
    def __add__(self, other): #this is the correct indentation
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

    def __getitem__(self, *args): #idx can be a tuple I think, this is for accessing a matrix
        print("getitem function")
        first = args[0]
        if type(first) == type(str):
            print("placeholder")
        #if type(idx) == type(int):
            #return "${}@(1,{})".format(self.iD, idx) 
        #else:  
            #return "${}@({},{})".format(self.iD, idx, idx)
        return ForIndex.new_index(self, self.name, 2, 2) #self.row #self.col

    def __setitem__(self, idx, value): #no return
        global opNum
        ForIndex.new_index(self, self.name, self.row, self.col)
        if type(idx) == type(int):
            print("update ${} [1] [{}] %{}".format(self.iD, idx, opNum))
        else:
            print("update ${} [{}] [{}] %{}".format(self.iD, idx, idx, opNum))
         

def for_loop(start, obj, step, func): #see DOVE
    global opNum
    global loop_indx
    opNum += 1
    index_var = ForIndex.new_index(obj, obj.iD, 1, j) #for right
    print("forloop [{}:{}:{}] \{}".format(start, obj.col, step, index_var.iD)) #creates new forindex variable
    func(index_var)
    print("endloop \{}".format(index_var.iD))


def if_else(cond, path_one, path_two): #optional arg for value i in case this is in a for loop
    global opNum
    global reg_num #global counter for registers
    #figure out what type cond, path_one and path_two are: matrix, value, register
    print("ifelse %{} %{} %{}".format(str(cond), str(path_one), str(path_two)))
    #check if class of path_two is a matirx, if so, return result (path_two)
    #else print a set statement and create new register
    result = path_two
    if type(path_two) == Matrix:
        return result
    else:
        Register.modify_register() #set the result, store in register
    #for ifelse statement just use tostring...

def __gt__(self, other): 
        return "> {} {}".format(self, other)
    
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

    
    
    
    
    
