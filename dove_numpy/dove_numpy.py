#dove.numpy
#in other file: import dove.numpy as np
#logistic regression
#zeros, dot, sum, exp, array
import numpy as np

matrix_num = 1 #total number of operations
loop_indx = 1 #renam
reg_num = 1
TRANSCRIPT = "transcript.txt"
file = open(TRANSCRIPT, "w")


class Register():
    def __init__(self):
        global reg_num
        self.iD = reg_num
        reg_num += 1
    
    def new_reg(self):
        print("set %{}".format(self.iD)) 

    def __str__(self):  
        return "%{}".format(self.iD)

    def __gt__(self, other): 
        print("> {} {}".format(self, other))
        r = Register()
        r.new_reg()
        return r

    def __lt__(self, other): 
        print("< {} {}".format(self, other))
        r = Register()
        r.new_reg()
        return r

class Pointer():
    def __init__(self, name, row, col):
        self.name = name
        self.row = row
        self.col = col

    def new_ptr(self):
        print("+ ${}@({},{})".format(self.name, self.row, str(self.col)))
        r = Register()
        r.new_reg()
        return r

    def __str__(self):
        return "${}@({},{})".format(self.name, self.row, str(self.col))
    
    def __gt__(self, other): 
        print("> {} {}".format(self, other))
        return Register()

class ForIndex():
    def __init__(self):
        global loop_indx
        self.iD = loop_indx
        loop_indx += 1

    def new_index(self):
        return ForIndex()

    def __repr__(self):
        return "\{}".format(self.iD)
    
    def __str__(self):
        return "\{}".format(self.iD)

    def __gt__(self, other): 
        print("> {} {}".format(self, other))
        return Register()

class Slice():
    def __init__(self, matrix, pos):
        global matrix_num
        self.iD = matrix_num
        self.obj = matrix.iD #what is being sliced
        self.pos = pos
        matrix_num += 1

    def new_slice(self): #matrix = thing to be sliced
        print(self.pos)
        print("slice const ${} [{}] [{}] ${}".format(self.obj, parse(self.pos[0]), parse(self.pos[1]), self.iD))

def parse(seq):
        if any(isinstance(x, ForIndex) for x in seq):
            result = str(seq)
        else:
            if np.isnan(np.diff(seq)[0]):
                result = str(seq[0])
            elif np.all(np.diff(seq) == np.diff(seq)[0]):
                result = "[{}:{}:{}]".format()
            else:
                print("placeholder")
        return "[{}]".format(result)     
    

class Matrix():
    def __init__(self, row, col, name = None, operation = None):
        global matrix_num
        self.name = name
        self.iD = matrix_num #need in addition to global variable
        self.row = row
        self.col = col
        self.shape = (row, col)
        self.operation = operation
        matrix_num += 1
        if self.name == None: #matrix will be modified as specified later on in the user's program
            print("def ${} [1:{}] [1:{}]\n\t{} ".format(self.iD, self.row, self.col, self.operation), end = ' ')
        else: #case where external data is used... I think
             print("def ${} [1:{}] [1:{}]\n\tdataset {}\nend ${}".format(self.iD, self.row, self.col, self.name, self.iD))

    def __str__(self):
        return "${}".format(self.iD)

    def modifyMatrix(self, operand, operation):
        global matrix_num
        if operation == "*": #dot product
            if type(operand) == type(None): 
                tmp = self
                return tmp 
            elif (type(operand) == int) or (type(operand) == float):
                tmp = Matrix(np.shape(self)[0], np.shape(self)[1], None, operation) #should be 455, 30
                print("${} #{}\nend ${}".format(self.iD, operand, tmp.iD))
            else:
                tmp = Matrix(np.shape(self)[0], np.shape(operand)[0], None, operation) #should be 455, 30
                print("${} ${}\nend ${}".format(self.iD, operand.iD, tmp.iD)) 
        else:
            if type(operand) == type(None): 
                tmp = self
                return tmp
            elif (type(operand) == int) or (type(operand) == float): #adding a constant
                tmp = Matrix(self.row, self.col, None, operation)
                print("${} #{}\nend ${}".format(self.iD, operand, tmp.iD))
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
                    other = Matrix(1, len(other), "sample", "none") #make ndarray into a Matrix, can't alwas hardcode 1
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
                    other = Matrix(1, len(other), "sample", "none") #make ndarray into a Matrix, can't alwas hardcode 1
                
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

    def __getitem__(self, pos): 
        if type(pos) == int:
            p = Pointer(self.iD, 1, pos).new_ptr() #not sure why pos would be a single thing...
        elif type(pos) == ForIndex:
            p = Pointer(self.iD, 1, ForIndex()).new_ptr()
        elif type(pos) == tuple or type(pos) == slice: #slice
            p = Slice(self, pos).new_slice()
        else:  
            p = Pointer(self.iD, pos[0], pos[1]).new_ptr()
        return p

    def __setitem__(self, idx, value): #no return
        global matrix_num
        if type(idx) == type(int):
            print("update ${} [1] [{}] %{}".format(self.iD, idx, matrix_num))
        else:
            print("update ${} [{}] [{}] %{}".format(self.iD, idx, idx, matrix_num))

# General methods

def wrap(obj, obj_type): #convert objects to dove_numpy objects, currently only for Matrices
    if type(obj) == type(obj_type): #obj_type
        return obj
    elif type(obj) == type(None):
        return obj
    elif obj_type == Matrix: 
        arr_np = np.array(obj) #is this okay?
        dimensions = arr_np.ndim
        if dimensions == 2: #2D array
            m = Matrix(np.shape(obj)[0], np.shape(obj)[1], "sample", None)
        else: #1D
            m = Matrix(1, np.shape(obj)[0], "sample", None)
        return m

def for_loop(start, end, step, func): #see DOVE
    global matrix_num
    global loop_indx
    matrix_num += 1
    v = ForIndex()
    index_var = v.new_index() 
    if type(end) == int:
        new_end = end
    elif type(end) == Matrix:
         new_end = end.col
    print("forloop [{}:{}:{}] \{}".format(start, new_end, step, index_var.iD)) #creates new forindex variable
    func(index_var)
    print("endloop \{}".format(index_var.iD))


def if_else(cond, path_one, path_two): 
    global matrix_num
    global reg_num 
    if type(path_one) == int:
        path_one = "#{}".format(path_one)
    if type(path_two) == int:
        path_two = "#{}".format(path_two)
    print("ifelse %{} {} {}".format(cond.iD, str(path_one), str(path_two)))
    #check if class of path_two is a matirx, if so, return result (path_two)
    #else print a set statement and create new register
    result = path_two
    if type(path_two) == Matrix:
        return result
    else:
        r = Register()
        return r 

    
# Logistic regression

def zeros(shape): #shape is int or tuple of ints
    if isinstance(shape, int): #1D array
        m = Matrix(1, shape, None, "+") 
    else: #2D
        m = Matrix(shape[0], shape[1], None, "+") 
    print("#0\nend ${}".format(m.iD)) #file.write

def dot(item1, item2): 
    if type(item2) == type(None):
        n = None
    elif type(item1) == type(None):
        m = None

    if type(item1) != Matrix and type(item1) != type(None):
        m = Matrix(np.shape(item1)[0], np.shape(item1)[1], "sample", None)
    elif type(item1) == Matrix:
        m = item1
    if type(item2) != Matrix and type(item2) != type(None):
        n = Matrix(np.shape(item2)[0], np.shape(item2)[1], "sample", None)
    elif type(item2) == Matrix:
        n = item2
    #dot operation
    mn = Matrix.modifyMatrix(m, n, "*")
    return mn

def sum(arr): #elements to sum, takes in array
    global matrix_num
    if not any(arr):
        arr = Matrix(0, 0, "placeholder", None)
    if type(arr) != Matrix:
         arr = Matrix(np.shape(arr)[0], np.shape(arr)[1], "sample", None)
    print("sum ${}".format(arr.iD))
    r = Register()
    r.new_reg()
    return r.iD
    
def exp(values): #input is a Matrix
    tmp = Matrix.modifyMatrix(values, None, "^")
    print("set ${}".format(tmp.iD)) #<--def needs some fixing
    print("update exp ${}".format(values.iD))
    return tmp

def array(data): #can accept like any object... add options later
    if len(data) > 0 and len(data[0]) > 0:    
        m = Matrix(len(data), len(data[0]), "sample", None) 
    else:
        m = Matrix(0, 0, "sample", None) #fix later
    return m
    

# Adaboost

def ones(shape): #shape is int or tuple of ints
    print("ones function")
    if isinstance(shape, int): #1D array
        m = Matrix(1, shape, None, "+") 
    else: #2D
        m = Matrix(shape[0], shape[1], None, "+") 
    print("#1\nend ${}".format(m.iD)) #file.write

def full(shape, fill_value): #will need to modify DOVE backend
    print("in full")
    if isinstance(shape, int): #1D array
        m = Matrix(1, shape, None, "+")
        print("#{}\nend ${}".format(fill_value, m.iD))
    else: #2D
        m = Matrix(shape[0], shape[1], None, "+")
        print("#{}\nend ${}".format(fill_value, m.iD))
        
def unique(array): #requires backend modifications
    m = wrap(array, Matrix)
    if m != type(None):
        size = m.row * m.col
    else:
        size = 0
    n = Matrix(1, size, None, "==") #flatten to 1D, worst case length
    print("%{} unique\nend ${}".format(m.iD, n.iD))
    return n

def log(array): #natural log, element-wise
    m = wrap(array, Matrix)
    if m != type(None):
        row = m.row
        col = m.col
    else:
        row = 0
        col = 0
    n = Matrix(row, col, None, "+") #length of new 1D matrix worst case
    print("%{} log\nend ${}".format(m.iD, n.iD))
    return n

def sign(array):
    m = wrap(array, Matrix)
    if m != type(None):
        row = m.row
        col = m.col
    else:
        row = 0
        col = 0
    n = Matrix(row, col, None, "+") #length of new 1D matrix worst case
    print("%{} sign\nend ${}".format(m.iD, n.iD))
    return n
    


    
    
    
