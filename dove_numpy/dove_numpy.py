#dove.numpy
from xmlrpc.client import boolean
import numpy as np
from numpy import random
from numpy import linalg

matrix_num = 1 #total number of operations
loop_indx = 1 #renam
reg_num = 1
TRANSCRIPT = "transcript.txt"
file = open(TRANSCRIPT, "w")

class DoveNumpy():

    def __rsub__(self, other): 
        other = "#{}".format(other) if isinstance(other, (int, float)) else other
        if type(self) == Matrix:
            return Matrix.modify_matrix(self, other, '-')
        else:
            print("- {} {}".format(other, self))
            r = Register()
            r.new_reg()
            return r
    
    def __sub__(self, other): 
        other = "#{}".format(other) if isinstance(other, (int, float)) else other
        if type(self) == Matrix:
            return Matrix.modify_matrix(self, other, '-')
        else:
            print("- {} {}".format(self, other))
            r = Register()
            r.new_reg()
            return r

    def __radd__(self, other):
        other = "#{}".format(other) if isinstance(other, (int, float)) else other
        if type(self) == Matrix:
            return Matrix.modify_matrix(self, other, '+')
        else:
            print("+ {} {}".format(other, self))
            r = Register()
            r.new_reg()
            return r

    def __add__(self, other):
        other = "#{}".format(other) if isinstance(other, (int, float)) else other
        if type(self) == Matrix:
            return Matrix.modify_matrix(self, other, '+')
        else:
            print("+ {} {}".format(self, other))
            r = Register()
            r.new_reg()
            return r
    
    def __truediv__(self, other):
        other = "#{}".format(other) if isinstance(other, (int, float)) else other
        if type(self) == Matrix:
            return Matrix.modify_matrix(self, other, '/')
        else:
            print("/ {} {}".format(self, other))
            r = Register()
            r.new_reg()
            return r
    
    def __rtruediv__(self, other):
        other = "#{}".format(other) if isinstance(other, (int, float)) else other
        if type(self) == Matrix:
            return Matrix.modify_matrix(self, other, '/')
        else:
            print("/ {} {}".format(other, self))
            r = Register()
            r.new_reg()
            return r
    
    def __rfloordiv__(self, other):
        other = "#{}".format(other) if isinstance(other, (int, float)) else other
        if type(self) == Matrix:
            return Matrix.modify_matrix(self, other, '/')
        else:
            print("/ {} {}".format(other, self))
            r = Register()
            r.new_reg()
            return r
    
    def __mul__(self, other):
        other = "#{}".format(other) if isinstance(other, (int, float)) else other
        if type(self) == Matrix:
            return Matrix.modify_matrix(self, other, '*')
        else:
            print("* {} {}".format(self, other))
            r = Register()
            r.new_reg()
            return r

    def __rmul__(self, other):
        other = "#{}".format(other) if isinstance(other, (int, float)) else other
        if type(self) == Matrix:
            return Matrix.modify_matrix(self, other, '*')
        else:
            print("* {} {}".format(other, self))
            r = Register()
            r.new_reg()
            return r
    
    def __gt__(self, other): 
        other = "#{}".format(other) if isinstance(other, (int, float)) else other
        if type(self) == Matrix:
            return Matrix.modify_matrix(self, other, '>')
        else:
            print("> {} {}".format(self, other))
            r = Register()
            r.new_reg()
            return r

    def __lt__(self, other): 
        other = "#{}".format(other) if isinstance(other, (int, float)) else other
        if type(self) == Matrix:
            return Matrix.modify_matrix(self, other, '<')
        else:
            print("< {} {}".format(self, other))
            r = Register()
            r.new_reg()
            return r
    
    def __neg__(self):
        return self * -1

    def __ne__(self, other):
        other = "#{}".format(other) if isinstance(other, (int, float)) else other
        if type(self) == Matrix:
            return Matrix.modify_matrix(self, other, '!=')
        else:
            print("!= {} {}".format(self, other))
            r = Register()
            r.new_reg()
            return r

class Register(DoveNumpy):
    def __init__(self):
        global reg_num
        self.iden = reg_num
        reg_num += 1
    
    def new_reg(self):
        print("set %{}".format(self.iden)) 

    def __str__(self):  
        return "%{}".format(self.iden)

class Pointer(DoveNumpy):
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

class ForIndex(DoveNumpy):
    def __init__(self):
        global loop_indx
        self.iden = loop_indx
        loop_indx += 1

    def new_index(self):
        return ForIndex()
    
    def __str__(self):
        return "\{}".format(self.iden)

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
    

class Matrix(DoveNumpy):
    def __init__(self, row, col, name = None, operation = None, slice_obj = None):
        global matrix_num
        self.iden = matrix_num 

        # Case of slicing
        if type(row) in (slice, tuple) or type(col) in (slice, tuple):
            print("slice const ${} {}${}".format(slice_obj.iden, parse((row, col), slice_obj), self.iden))
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
                print("def ${} [1:{}] [1:{}]\n\t{} ".format(self.iden, self.row, self.col, self.operation), end = ' ')
            elif operation == "empty": 
                print("def ${} [1:{}] [1:{}]\n\empty\nend ${}".format(self.iden, self.row, self.col, self.iden))
            else: # External dataset
                print("def ${} [1:{}] [1:{}]\n\tdataset {}\nend ${}".format(self.iden, self.row, self.col, self.name, self.iden))

    def modify_matrix(obj, operand, operation):
        global matrix_num
        if type(operand) == type(None): 
            print("NONE")
            tmp = obj
        else:
            if operation == "*" and type(operand) == Matrix:
                row = obj.row
                col = operand.col
            if type(obj) == tuple:
                row = obj[0]
                col = obj[1]
                param = ""
            else:
                row = obj.row
                col = obj.col
                param = "{} ".format(obj.iden)
            operand = "#{}".format(operand) if isinstance(operand, (int, float)) else operand
            tmp = Matrix(row, col, None, operation)
            print("{}{}\nend ${}".format(param, str(operand), tmp.iden)) #first param was obj.iden
            
        return tmp

    def __str__(self):
        return "${}".format(self.iden)

    def __getitem__(self, pos):
        if type(pos) == int:
            p = Pointer(self.iden, 1, pos).new_ptr() #TODO: change later, temp fix
        elif type(pos) == ForIndex:
            p = Pointer(self.iden, 1, ForIndex()).new_ptr()
        elif type(pos) == tuple or type(pos) == slice: # A slice is a Matrix
            p = Matrix(pos[0], pos[1], None, None, self)
        elif type(pos) == Matrix:
            p = Matrix.modify_matrix(self, pos, "==")
        else:  
            p = Pointer(self.iden, pos[0], pos[1]).new_ptr()
        return p

    def __setitem__(self, idx, value):
        #TODO: use the parse function here
        global matrix_num
        if type(idx) == tuple: # Ex (\1,\1)
            print("setitem tuple")
            if type(value) == int:
                value = "#" + str(value)
            print("update ${} [{}] [{}] {}".format(self.iden, str(idx[0]), str(idx[1]), str(value)))
        elif type(idx) == bool:
            print("setitem bool")
            m = Matrix.modify_matrix(self, value, "==") #TODO: FIX
            if type(value) == int:
                value = "#" + str(value)
            print("update ${} {} {}".format(self.iden, str(m), value))
        elif type(idx) == Register: #TODO: FIX 
            m = Matrix.modify_matrix(self, idx, "==")
            print("update ${} {} {}".format(self.iden, str(m), value))
        
    def append(self, element):

        if type(element) == int or type(element) == float:
            element = "#{}".format(element)
        elif type(element) != Register: # Custom objects
            element = type(element).__name__
        self.col = self.col + 1
        print("update {} {}".format(str(self), str(element)))
        
# General methods

def set_attr(value):
    if type(value) == int:
            value = "#{}".format(value)
    
    print("+ {}".format(value))
    r = Register()
    r.new_reg()
    return r

def get_attr(name):
    return "get_attr {}".format(name)

def for_loop(start, end, step, func, obj, *args): # Obj is string or function
    global matrix_num
    global loop_indx
    matrix_num += 1
    if type(obj) == ForIndex:
        index_var = " \{}".format(obj.iden)
    elif type(obj) == Register or type(obj) == type(None):
        index_var = ""

    if type(end) == int:
        new_end = end
    elif type(end) == Matrix:
         new_end = end.col

    print("forloop [{}:{}:{}]{}".format(start, new_end, step, index_var)) 
    func(obj, *args) #obj and *args
    print("endloop {}".format(index_var))
    return index_var

def for_index(var):
    var = ForIndex()
    v = var.new_index()
    return v

def make_ptr(matrix): #TODO: see if I even need this
    if len(np.shape(matrix)) == 2:
        var = Pointer(matrix.iden, ForIndex(), ForIndex())
    else:
        var = Pointer(matrix.iden, 1, ForIndex())
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
    print("ifelse %{} {} {}".format(cond.iden, str(path_one), str(path_two)))
    result = path_two
    if type(path_two) == Matrix:
        return result
    else:
        r = Register()
        return r 

    
# Logistic regression

def zeros(shape): # Shape is int or tuple of ints
    dims = (1, shape) if isinstance(shape, int) else (shape[0], shape[1])
    m = Matrix.modify_matrix(dims, "0", "+")
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
    axis_str = "_{} ".format(axis) if axis != None else ""
    print("sum {}${}".format(axis_str, arr.iden))
    r = Register()
    r.new_reg()
    return r
    
def exp(obj): # Input is a Matrix
    if type(obj) == Register or type(obj) == int or type(obj) == float:
        obj = "#{}".format(obj) if type(obj) != Register else obj
        print("exp {}".format(str(obj)))
        r = Register()
        r.new_reg()
        return r
    elif type(obj) == Matrix:
        tmp = Matrix.modify_matrix(obj, None, "exp")

    return tmp

def array(data): 
    if type(data) == Matrix:
        return data
    elif len(data) == 0:
        return Matrix.modify_matrix((1, 1), None, "empty")
    else:
        print("Unable to define array. Please initialize in data.init file.")

# Adaboost

def ones(shape): #TODO: may need to remove
    dims = (1, shape) if isinstance(shape, int) else (shape[0], shape[1])
    m = Matrix.modify_matrix(dims, "1", "+")
    return m

def full(shape, fill_value): 
    if isinstance(fill_value, (int, float, str)):
        print("full method: {} {}".format(shape, fill_value))
        print("Unable to define array. Please initialize in data.init file.")
    else:
        dims = (1, shape) if isinstance(shape, int) else (shape[0], shape[1])
        m = Matrix.modify_matrix(dims, fill_value, "+")
        return m
        
def unique(array): 
    # Returns Matrix of sorted unique values
    if type(array) == type(None):
        size = 0
    elif type(array.row) == ForIndex: #TODO: figure out how to deal with ForIndex dimensions
        size = (1, array.col)
    elif type(array.col) == ForIndex:
        size = (1, array.row)
    else:
        size = (1, array.row * array.col)
    m = Matrix.modify_matrix(size, array.iden, "unique")
    return m

def log(obj): # Natural log, element-wise
    if type(obj) == int or type(obj) == float or type(obj) == Register:
        print("log {}".format(obj))
        n = Register()
        n.new_reg()
    else:
        if obj != type(None):
            dims = (obj.row, obj.col)
        else:
            dims = (0, 0)
        n = Matrix.modify_matrix(dims, obj.iden, "log")
    return n

def sign(array):
    if type(array) == Matrix:
        dims = (array.row, array.col)
        n = Matrix.modify_matrix(dims, array.iden, "sign")
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
    print("max ${}".format(array.iden))
    r = Register()
    r.new_reg()
    return r

def bincount(array): # Count number of occurrences of each value in array of non-negative ints
    max_int = max(array)
    m = Matrix.modify_matrix((1, max_int), array.iden, "bincount") #TODO: find better name than 'bincount'
    return m

def log2(obj):
    if type(obj) == int or type(obj) == float or type(obj) == Register:
        print("log {}".format(obj))
        n = Register()
        n.new_reg()
    else:
        if obj != type(None):
            dims = (obj.row, obj.col)
        else:
            dims = (0, 0)
        n = Matrix.modify_matrix(dims, obj, "log2")
    return n

def choice(obj, size = None, replace = True): # From numpy.random
    # Generates a random sample from a given 1-D array
    if size == None:
        size = (1, 1)
    elif type(size) == int:
        size = (1, size)
    
    obj = "#{}".format(obj) if type(obj) == int else obj #TODO: figure out format for printing params, need more than obj
    m = Matrix(size, obj, "rand")
    return m

def argwhere(cond): # Find the indices of array elements that are non-zero, grouped by element.
    # Example input: x > 1 where x is an array
    m = Matrix.modify_matrix((1, 10), cond, "argwhere") #TODO: properly set size, 1 and 10 are placeholders
    return m

# Kmeans

def seed(int): # From np.random
    print("seed") # TODO: figure out what to do here since the seed should remain secret...
    r = Register()
    r.new_reg()
    return r
    
def sqrt(obj):
    if type(obj) == Matrix:
        m = Matrix.modify_matrix(obj, None, "sqrt")
        return m
    else:
        obj = "#{}".format(obj) if isinstance(obj, (int, float)) else obj
        print("sqrt {}".format(obj))
        r = Register()
        r.new_reg()
        return r

def empty(shape):
    shape = (1, shape) if type(shape) == int else shape
    m = Matrix.modify_matrix(shape, None, "empty")
    return m

def argmin(array): # Returns indices of the min values along an axis
    print("min {}".format(array))
    r = Register()
    r.new_reg()
    return r

def mean(array, axis = None):
    if axis != None:
        m = Matrix.modify_Matrix(array, None, "mean") #TODO: figure out syntax to denote axis
        return m
    else:
        print("mean {}".format(array))
        r = Register()
        r.new_reg()
        return r

# Knn

def argsort(array):
    # Default: axis = 1, sort = quicksort
    m = Matrix.modify_matrix(array, None, "argsort")
    print("${}\nend ${}".format(array.iden, m.iden))
    return m

# Ida- both from linalg module

def inv(array): # Calculate inverse of a Matrix
    m = Matrix.modify_matrix(array, None, "inv")
    print("${}\nend ${}".format(array.iden, m.iden))
    return m

def eig(array): # Calculate eigenvalues and eigenvectors
    print("eig ${}".format(array.iden))
    r = Register()
    r.new_reg()
    return r

# Linear Regression

def corrcoef(x, y): # Return Pearson product-moment correlation coefficients
    m = Matrix.modify_matrix(x, y, "corrcoef")
    print("${} ${}\nend ${}".format(x.iden, y.iden, m.iden))
    return m

# Load data

def float32(num): #TODO: figure out how to differentiate between data types
    print("+ #{}".format(num))
    r = Register()
    r.new_reg()
    return r

    

#genfromtxt, asarray

# Pretty sure we can not support the loadtext or genfromtxt functions
    
    
    
