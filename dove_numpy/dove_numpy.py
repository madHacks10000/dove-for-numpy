#dove.numpy
#in other file: import dove.numpy as np
#logistic regression
#zeros, dot, sum, exp, array
from xmlrpc.client import boolean
import numpy as np
from numpy import random

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
    
    def __rsub__(self, other): 
        if type(other) == int:
            other = "#{}".format(other)
        print("- {} {}".format(str(other), str(self)))
        r = Register()
        r.new_reg()
        return r
    
    def __sub__(self, other): 
        if type(self) == int:
            other = "#{}".format(other)
        print("- {} {}".format(str(self), str(other)))
        r = Register()
        r.new_reg()
        return r

    def __radd__(self, other):
        if type(other) == int or type(other) == float: #TODO: how to avoid repetition
            other = "#{}".format(other)
        print("+ {} {}".format(str(other), str(self)))
        r = Register()
        r.new_reg()
        return r

    def __add__(self, other):
        if type(other) == int:
            other = "#{}".format(other)
        print("+ {} {}".format(str(self), str(other)))
        r = Register()
        r.new_reg()
        return r
    
    def __truediv__(self, other):
        if type(other) == int:
            other = "#{}".format(other)
        print("/ {} {}".format(str(self), str(other)))
        r = Register()
        r.new_reg()
        return r
    
    def __rtruediv__(self, other):
        if type(other) == int:
            other = "#{}".format(other)
        print("/ {} {}".format(str(other), str(self)))
        r = Register()
        r.new_reg()
        return r
    
    def __mul__(self, other):
        if type(other) == int:
            other = "#{}".format(other)
        print("* {} {}".format(str(self), str(other)))
        r = Register()
        r.new_reg()
        return r

    def __rmul__(self, other):
        if type(other) == int:
            other = "#{}".format(other)
        print("* {} {}".format(str(other), str(self)))
        r = Register()
        r.new_reg()
        return r
    
    def __neg__(self):
        return self * -1


class Pointer():
    def __init__(self, name, row, col): #TODO: modify structure of init and new_ptr
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
    
    def __str__(self):
        return "\{}".format(self.iD)

    def __gt__(self, other): 
        print("> {} {}".format(self, other))
        return Register()

def parse(obj, slice_obj):
    result = ''
    for i in range(2):
        seq = obj[i]
        if type(seq) == ForIndex: #any(isinstance(x, ForIndex) for x in seq): 
            result = "{}[{}] ".format(result, str(seq))
        elif type(seq) == int: #might be missing a condition
            result = "{}#{} ".format(result, seq)
        elif type(seq) == slice:
            if(seq.start == None):
                if i == 1:
                    dim = slice_obj.row
                else:
                    dim = slice_obj.col
                result = "{}[{}:{}:{}] ".format(result, 1, dim, 1) #dimensions of original matrix
    return result    
    

class Matrix():
    def __init__(self, row, col, name = None, operation = None, slice_obj = None):
        global matrix_num
        self.iD = matrix_num 

        # Case of slicing
        if type(row) in (slice, tuple) or type(col) in (slice, tuple):
            print("slice const ${} {}${}".format(slice_obj.iD, parse((row, col), slice_obj), self.iD))
            if type(row) in (slice, tuple):
                self.row = slice_obj.row
                self.col = col
            else:
                self.row = row
                self.col = slice_obj.col
        else:
            self.row = row
            self.col = col
        self.name = name
        self.operation = operation
        self.shape = (row, col)
        matrix_num += 1

        # If matrix isn't a slice
        if slice_obj == None:
            if self.name == None: 
                print("def ${} [1:{}] [1:{}]\n\t{} ".format(self.iD, self.row, self.col, self.operation), end = ' ')
            else: # External dataset
                print("def ${} [1:{}] [1:{}]\n\tdataset {}\nend ${}".format(self.iD, self.row, self.col, self.name, self.iD))

    def modify_matrix(self, operand, operation):
        global matrix_num
        if type(operand) == type(None): 
            tmp = self
        else:
            if type(operand) == int or type(operand) == float:
                operand = "#{}".format(operand)
            tmp = Matrix(self.row, self.col, None, operation)
            print("${} {}\nend ${}".format(self.iD, str(operand), tmp.iD)) 
        return tmp

    def __str__(self):
        return "${}".format(self.iD)
    
    def __gt__(self, other): 
        print("> {} {}".format(self, other))
        return Matrix.modify_matrix(self, other, '>')
    
    def __add__(self, other): 
        return Matrix.modify_matrix(self, other, '+')

    def __sub__(self, other): 
        if type(self) == type(None):
            self = 0
        elif type(other) == type(None):
            other = 0
        return Matrix.modify_matrix(self, other, '-')

    def __rsub__(self, other):
        if type(self) == type(None):
            self = 0
        elif type(other) == type(None):
            other = 0 
        return Matrix.modify_matrix(self, other, '-')

    def __radd__(self, other):
        return Matrix.modify_matrix(self, other, '+')

    def __mul__(self, other): 
        return Matrix.modify_matrix(self, other, '*')

    def __rmul__(self, other): 
        return Matrix.modify_matrix(self, other, '*')

    def __truediv__(self, other): 
        return Matrix.modify_matrix(self, other, '/')

    def __rtruediv__(self, other): 
        return Matrix.modify_matrix(self, other, '/')

    def __rfloordiv__(self, other):
        return Matrix.modify_matrix(self, other, '/')

    def __neg__(self):
        return Matrix.modify_matrix(self, -1, '*')

    def __ne__(self, other):
        return Matrix.modify_matrix(self, other, '!=')

    def __getitem__(self, pos):
        if type(pos) == int:
            p = Pointer(self.iD, 1, pos).new_ptr() #TODO: change later, temp fix
        elif type(pos) == ForIndex:
            p = Pointer(self.iD, 1, ForIndex()).new_ptr()
        elif type(pos) == tuple or type(pos) == slice: # A slice is a Matrix
            p = Matrix(pos[0], pos[1], None, None, self)
        elif type(pos) == Matrix:
            p = Matrix.modify_matrix(self, pos, "==")
        else:  
            p = Pointer(self.iD, pos[0], pos[1]).new_ptr()
        return p

    def __setitem__(self, idx, value):
        #TODO: use the parse function here
        global matrix_num
        if type(idx) == tuple: # Ex (\1,\1)
            print("setitem tuple")
            if type(value) == int:
                value = "#" + str(value)
            print("update ${} [{}] [{}] {}".format(self.iD, str(idx[0]), str(idx[1]), str(value)))
        elif type(idx) == bool:
            print("setitem bool")
            m = Matrix.modify_matrix(self, value, "==") #TODO: FIX
            if type(value) == int:
                value = "#" + str(value)
            print("update ${} {} {}".format(self.iD, str(m), value))
        elif type(idx) == Register: #TODO: FIX 
            m = Matrix.modify_matrix(self, idx, "==")
            print("update ${} {} {}".format(self.iD, str(m), value))
        
    def append(self, element):
        if type(element) == int or type(element) == float:
            element = "#{}".format(element)
        elif type(element) != Register: # Custom objects
            element = type(element).__name__
        self.col = self.col + 1
        print("update {} {}".format(str(self), str(element)))
        


# General methods

def wrap(obj, obj_type): # Currently only for Matrices
    if type(obj) == obj_type: 
        return obj
    elif type(obj) == type(None):
        return obj
    elif obj_type == Matrix: 
        if len(np.shape(obj)) == 2: # 2D array
            m = Matrix(np.shape(obj)[0], np.shape(obj)[1], "sample", None)
        else: # 1D
            m = Matrix(1, np.shape(obj)[0], "sample", None)
        return m

def for_loop(start, end, step, obj): # Obj is string or function
    global matrix_num
    global loop_indx
    matrix_num += 1
    if type(obj) == ForIndex:
        index_var = " \{}".format(obj.iD)
    elif type(obj) == Register or type(obj) == type(None):
        index_var = ""
    elif callable(obj):
        index_var = loop_indx
    
    if type(end) == int:
        new_end = end
    elif type(end) == Matrix:
         new_end = end.col

    print("forloop [{}:{}:{}]{}".format(start, new_end, step, index_var)) 

    if callable(obj):
        obj(ForIndex())
        print("endloop {}".format(index_var))
    return index_var

def for_index(var):
    var = ForIndex()
    v = var.new_index()
    return v

def make_ptr(matrix): #TODO: see if I even need this
    matrix = wrap(matrix, Matrix)
    if len(np.shape(matrix)) == 2:
        var = Pointer(matrix.iD, ForIndex(), ForIndex())
    else:
        var = Pointer(matrix.iD, 1, ForIndex())
    v = var.new_ptr()
    return v

def end_for(indx):
    print("endloop{}".format(indx))

def if_else(cond, path_one, path_two): 
    global matrix_num
    global reg_num 
    if type(path_one) == int:
        path_one = "#{}".format(path_one)
    if type(path_two) == int:
        path_two = "#{}".format(path_two)
    print("ifelse %{} {} {}".format(cond.iD, str(path_one), str(path_two)))
    result = path_two
    if type(path_two) == Matrix:
        return result
    else:
        r = Register()
        return r 

    
# Logistic regression

def zeros(shape): # Shape is int or tuple of ints
    if isinstance(shape, int): # 1D array
        m = Matrix(1, shape, None, "+") 
    else: # 2D
        m = Matrix(shape[0], shape[1], None, "+") 
    print("#0\nend ${}".format(m.iD)) # file.write
    return m

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

    # Dot operation
    mn = Matrix.modify_matrix(m, n, "*")
    return mn

def sum(arr, axis = None): # Elements to sum, takes in array
    global matrix_num

    if axis != None:
        axis_str = "_{} ".format(axis)
    else:
        axis_str = ""
    
    m = wrap(arr, Matrix)
    print("sum {}${}".format(axis_str, m.iD)) # Backend modification
    r = Register()
    r.new_reg()
    return r
    
def exp(obj): # Input is a Matrix
    if type(obj) == Register or type(obj) == int or type(obj) == float:
        if type(obj) != Register:
            obj = "#{}".format(obj)
        print("exp {}".format(str(obj)))
        r = Register()
        r.new_reg()
        return r
    elif type(obj) == Matrix:
        tmp = Matrix.modify_matrix(obj, None, "exp")

    return tmp

def array(data): # TODO: fix
    if len(np.shape(data)) == 2: # 2D array 
        m = Matrix(np.shape(data)[0], np.shape(data)[1], "sample", None) 
    else: # 1D
        m = Matrix(1, np.shape(data)[0], "sample", None)
    return m
    

# Adaboost

def ones(shape): # Shape is int or tuple of ints
    if isinstance(shape, int): # 1D array
        m = Matrix(1, shape, None, "+") 
    else: # 2D
        m = Matrix(shape[0], shape[1], None, "+") 
    print("#1\nend ${}".format(m.iD)) 
    return m

def full(shape, fill_value): # Will need to modify DOVE backend
    if isinstance(shape, int): #1D array
        m = Matrix(1, shape, None, "+")
        print("#{}\nend ${}".format(fill_value, m.iD))
    else: #2D
        m = Matrix(shape[0], shape[1], None, "+")
        print("#{}\nend ${}".format(fill_value, m.iD))
    return m
        
def unique(array): # Requires backend modifications
    # Returns Matrix of sorted unique values
    m = wrap(array, Matrix)
    if type(m) != type(None):
        if type(m.row) == ForIndex: 
            size = m.col
        elif type(m.col) == ForIndex:
            size = m.row
        else:
            size = m.row * m.col
    else:
        size = 0
    n = Matrix(1, size, None, "==") # Flatten to 1D, worst case length
    print("${} unique\nend ${}".format(m.iD, n.iD))
    return n

def log(obj): # Natural log, element-wise
    if type(obj) == int or type(obj) == float or type(obj) == Register:
        print("log {}".format(obj))
        n = Register()
        n.new_reg()
    else:
        m = wrap(obj, Matrix)
        if m != type(None):
            row = m.row
            col = m.col
        else:
            row = 0
            col = 0
        n = Matrix(row, col, None, "+") 
        print("${} log\nend ${}".format(m.iD, n.iD))
    return n

def sign(array):
    if type(array) == Matrix:
        n = Matrix(array.row, array.col, None, "+")
        print("%{} sign\nend ${}".format(m.iD, n.iD))
        return n
    elif type(array) == Register:
        print("sign {}".format(str(array)))
        r = Register()
        r.new_reg()
        return r
    else:
        return None
    
# Decision Tree

def max(array): # Find max value of array
    print("max ${}".format(array.iD))
    r = Register()
    r.new_reg()
    return r

def bincount(array): # Count number of occurrences of each value in array of non-negative ints
    # Inefficient to use 'unique' syntax, need another backend modification
    max_int = max(array)
    m = Matrix(1, max_int, None, "+")
    print("{} bincount\nend ${}".format(array.iD, m.iD)) #TODO: find better name than 'bincount'

def log2(obj):
    if type(obj) == int or type(obj) == float or type(obj) == Register:
        print("log {}".format(obj))
        n = Register()
        n.new_reg()
    else:
        m = wrap(obj, Matrix)
        if m != type(None):
            row = m.row
            col = m.col
        else:
            row = 0
            col = 0
        n = Matrix(row, col, None, "+") 
        print("${} log2\nend ${}".format(m.iD, n.iD)) #TODO: figure out better syntax
    return n

def choice(obj, size=None, replace=True): # From numpy.random
    # Generates a random sample from a given 1-D array
    m = Matrix(1, obj, None, "+")
    if type(obj) == int: #TODO: figure out format for printing params, need more than obj
        params = "#{}".format(obj)
    else:
        params = "${}".format(obj.iD)
    print("{} rand\nend ${}".format(params, m.iD))

def argwhere(cond): # Find the indices of array elements that are non-zero, grouped by element.
    # Input is like x > 1 where x is an array
    m = Matrix(1, 10, None, "+") # TODO: properly set size, 1 and 10 are placeholders
    print("${} argwhere\nend ${}".format(cond.iD, m.iD))
    return m

# Kmeans

def seed(int): # From np.random
    print("seed #{}") # TODO: change later because the seed should probably be protected...
    r = Register()
    r.new_reg()
    return r
    
def sqrt(obj):
    if type(obj) == Matrix:
        m = Matrix.modify_matrix(obj, None, "+")
        print("${} sqrt\nend ${}".format(obj.iD, m.iD))
        return m
    else:
        if type(obj) == int:
            obj = "#{}".format(obj)
        print("sqrt {}".format(obj))
        r = Register()
        r.new_reg()
        return r

def empty(shape):
    if type(shape) == int:
        m = Matrix(1, shape, None, "empty")
    else:
        m = Matrix(shape[0], shape[1], None, "empty")
    print("\nend ${}".format(m.iD))
    return m

def argmin(array): # Returns indices of the min values along an axis
    print("min {}".format(array))
    r = Register()
    r.new_reg()
    return r

def mean(array, axis = None):
    if axis != None:
        m = Matrix(10, 10, None, "+")
        print("${} mean\nend ${}".format(array.iD, m.iD))
        return m
    else:
        print("mean {}".format(array))
        r = Register()
        r.new_reg()
        return r






    
    
    
