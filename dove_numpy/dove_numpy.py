#dove.numpy
from xmlrpc.client import boolean
import numpy as np
from numpy import random
#from numpy import linalg

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
            print("floor {}".format(r))
            r2 = Register()
            r2.new_reg()
            return r2
    
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
    
    def __ge__(self, other): 
        other = "#{}".format(other) if isinstance(other, (int, float)) else other
        if type(self) == Matrix:
            return Matrix.modify_matrix(self, other, '>=')
        else:
            print(">= {} {}".format(self, other))
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

    def __le__(self, other): 
        other = "#{}".format(other) if isinstance(other, (int, float)) else other
        if type(self) == Matrix:
            return Matrix.modify_matrix(self, other, '<=')
        else:
            print("<= {} {}".format(self, other))
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

    def __eq__(self, other):
        if type(self) == Matrix:
            return Matrix.modify_matrix(self, other, '==')
        else:
            print("== {} {}".format(self, other))
            r = Register()
            r.new_reg()
            return r

    def __len__(self):
        return self.row

    def __iadd__(self, other):
        other = "#{}".format(other) if isinstance(other, (int, float)) else other
        if type(self) == Matrix:
            return Matrix.modify_matrix(self, other, '+')
        else:
            print("+ {} {}".format(self, other))
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
        return "{}@({},{})".format(self.name, self.row, str(self.col))

class ForIndex(DoveNumpy):
    def __init__(self):
        global loop_indx
        self.iden = loop_indx

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
            result = "{}[{}] ".format(result, seq)
        elif type(seq) == slice:
            if(seq.start == None):
                if i == 1:
                    dim = slice_obj.row
                else:
                    dim = slice_obj.col
                result = "{}[{}:{}:{}] ".format(result, 1, dim, 1) #dimensions of original matrix
            else:
                result = "{}[{}:{}:{}] ".format(result, obj.start, obj.end, obj.stop)
    return result    


class Matrix(DoveNumpy):
    def __init__(self, row, col, name = None, operation = None, slice_obj = None):
        global matrix_num
        self.iden = matrix_num
        sliced = False
        # Case of slicing
        if type(row) in (slice, tuple) or type(col) in (slice, tuple): # Maybe just check if slice_obj is None
            print("slice const ${} {}${}".format(slice_obj.iden, parse((row, col), slice_obj), self.iden))
            sliced = True
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
        self.slice_obj = slice_obj

        # If matrix isn't a slice
        if sliced == False and slice_obj == None:
            if self.name == None: 
                print("def ${} [1:{}] [1:{}]\n\t{} ".format(self.iden, self.row, self.col, self.operation), end = ' ')
            elif operation == "empty": 
                print("def ${} [1:{}] [1:{}]\n\empty\nend ${}".format(self.iden, self.row, self.col, self.iden))
            else: # External dataset
                print("def ${} [1:{}] [1:{}]\n\tdataset {}\nend ${}".format(self.iden, self.row, self.col, self.name, self.iden))
    
    @property
    def T(self): #Transpose
        m = Matrix(self.col, self.row, "empty", None)
        i = 0 
        i = for_index(i)
        loop1 = for_loop(0, self.row, 1, i)
        j = 0 
        j = for_index(j)
        loop2 = for_loop(0, self.col, 1, j)
        m[j, i] = self[i, j]
        end_for(loop2)
        end_for(loop1)
        return m

    def modify_matrix(obj, operand, operation):
        global matrix_num
        bind = False
        if type(operand) == type(None): 
            operand = ""
        else:
            if operation == "*" and type(operand) == Matrix:
                row = obj.row
                col = operand.col
            elif operation == "cbind" or operation == "rbind":
                bind = True
                param = ""

            if type(obj) == tuple:
                row = obj[0]
                col = obj[1]
                param = ""
            elif bind != True:
                row = obj.row
                col = obj.col
                param = "{} ".format(obj)
            operand = "#{}".format(operand) if isinstance(operand, (int, float)) else operand
            tmp = Matrix(row, col, None, operation)
            print("{}{}\nend ${}".format(param, operand, tmp.iden)) #first param was obj.iden
            
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
            if type(value) == int:
                value = "#" + str(value)
            print("update ${} [{}] [{}] {}".format(self.iden, str(idx[0]), str(idx[1]), str(value)))
        elif type(idx) == bool:
            m = Matrix.modify_matrix(self, value, "==") #TODO: FIX
            if type(value) == int:
                value = "#" + str(value)
            print("update ${} {} {}".format(self.iden, str(m), value))
        elif type(idx) == Register: #TODO: FIX 
            m = Matrix.modify_matrix(self, idx, "==")
            print("update ${} {} {}".format(self.iden, str(m), value))

    def append(self, element, invisible=False):
        if invisible == False:
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

def for_loop(start, end, step, obj): # Obj is string or function
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
    loop_indx += 1
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
    m = Matrix.modify_matrix(dims, 0, "+")
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
    if axis == None:
        print("sum ${}".format(arr.iden))
        r = Register()
        r.new_reg()
        return r
    else:
        l = 0
        l = for_index(l)
        if axis == 0:
            m = Matrix(1, arr.col, None, "empty")
            arr.col = l
        elif axis == 1:
            m = Matrix(1, arr.row, None, "empty")
            arr.row = l
        loop1 = for_loop(0, arr, 1, l)
        n = Matrix(arr.row, l, None, None, arr)
        print("sum {}".format(n.iden))
        r = Register()
        print(r.new_reg())
        m[n.row, n.col] = r
        end_for(loop1)
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

def array(data, dtype = None): 
    if type(data) == Matrix:
        if dtype != None and type(data) != dtype:
            print("float32 {}".format(data))
        else:
            return data
    elif len(data) == 0:
        return Matrix.modify_matrix((1, 1), None, "empty")
    

# Adaboost
def ones(shape): #TODO: may need to remove
    dims = (1, shape) if isinstance(shape, int) else (shape[0], shape[1])
    m = Matrix.modify_matrix(dims, "1", "+")
    return m

def full(shape, fill_value): 
    dims = (1, shape) if isinstance(shape, int) else (shape[0], shape[1])
    m = Matrix.modify_matrix(dims, fill_value, "+")
    return m

def binding(first, second, mode):
    output_str = ""
    if mode == "cbind":
        if type(first) == Pointer:
            output_str += str(first)
        elif first.shape[1] > 1:
            for i in range(first.col):
                x = first[:,i]
                output_str += "{} ".format(x)
        else: # Col = 1
            output_str = str(first)
        if type(second) == Pointer:
            output_str += str(first)
        elif second.shape[1] > 1:
            for i in range(second.col):
                x = second[:,i]
                output_str += "{} ".format(x)
        else:
            output_str = str(second)
    if mode == "rbind":
        if type(first) == Pointer:
            output_str += str(second)
        elif first.shape[0] > 1:
            for i in range(first.row):
                x = first[i,:]
                output_str += "{} ".format(x)
        else:
            output_str = str(first)

        if type(second) == Pointer:
            output_str += str(first)
        elif second.shape[0] > 1:
            for i in range(second.row):
                x = second[i,:]
                output_str += " ${}".format(x)
        else:
            output_str = str(second)

    return output_str

def unique(array): # TODO: come back to
    # Returns Matrix of sorted unique values
    #TODO: figure out how to deal with ForIndex dimensions
    row = array.slice_obj.row if isinstance(array.shape[0], (tuple, slice)) else None
    row = 1 if isinstance(array.shape[0], ForIndex) else row
    row = array.shape[0] if row == None else row
    col = array.slice_obj.col if isinstance(array.shape[1], (tuple, slice)) else None
    col = 1 if isinstance(array.shape[1], ForIndex) else col
    col = array.shape[1] if col == None else col

    length = row * col
    m = Matrix(1, length, "empty", None)
    # Unique array
    l = 0
    l = for_index(l)
    loop1 = for_loop(0, array, 1, l)
    tmp = array.row
    if array.row != 1:
        k = 0
        k = for_index(k)
        loop2 = for_loop(0, array, 1, k)
        array.col = k
        array.row = l
    else:
        array.col = l
    p = Pointer(array, array.row, array.col)
    n = Matrix.modify_matrix(m, p, "==") # See if the element is already in unique or not
    print("any {}".format(n))
    r = Register()
    r.new_reg()
    print("! {}".format(r))
    r2 = Register()
    r2.new_reg()
    # True condition
    output = binding(m, p, "cbind")
    o = Matrix.modify_matrix((row, col), output, "cbind") # TODO: maybe just update the original unique matrix
    print("3")
    # False
    q = Matrix.modify_matrix(m, None, "+")
    print("4")
    #ifelse 
    print("ifelse {} {} {}".format(r2, o, q))
    r3 = Register()
    r3.new_reg()
    end_for(loop1)
    end_for(loop2) if tmp != 1 else None


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
    m = zeros(array.col) 
    p = 0
    p = make_ptr(array) # P is a Register
    loop1 = for_loop(0, array, 1, p)
    m[p] = m[p] + 1 # TODO: might need to modify setitem
    end_for(loop1)
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
    m = Matrix(1, cond.row * cond.col, "empty", None) #TODO: properly set size, 1 and 10 are placeholders
    l = 0
    l = for_index(l)
    loop1 = for_loop(0, cond, 1, l)
    tmp = m.row
    if m.row != 1:
        k = 0
        k = for_index(k)
        loop2 = for_loop(0, cond, 1, k)
        m.col = k
        m.row = l
    else:
        m.col = l
    p = Pointer(m, m.row, m.col)
    c = Pointer(cond, cond.row, cond.col)
    print("+ {}".format(c)) # False option
    r = Register()
    r.new_reg()
    print("ifelse {} {} {}".format(cond, p, c))
    r2 = Register()
    r2.new_reg()
    m[p] = r2 # Call update (setitem)
    end_for(loop1)
    end_for(loop2) if tmp != 1 else None

# Kmeans
def seed(int): # From np.random
    print("seed") # Note: placeholder, need to write function
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
    if axis == None:
        print("sum {}".format(array))
        r = Register()
        r.new_reg()
        print("/ {} #{}".format(r, array.row * array.col))
        r2 = Register()
        r2.new_reg()
    else:
        l = 0
        l = for_index(l)
        loop1 = for_loop(0, array, 1, l)
        tmp = array.row
        if array.row != 1:
            k = 0
            k = for_index(k)
            loop2 = for_loop(0, array, 1, k)
            array.col = k
            array.row = 1
        else:
            array.col = l
        if axis == 0: # Rows
            m = Matrix(l, slice(0, array.col, 1), None, None, array)
        elif axis == 1: #Cols
            m = Matrix(slice(0, array.row, 1), l, None, None, array)
        print("sum {}".format(m.iden))
        r2 = Register()
        r2.new_reg()
        print("/ {} #{}".format(r2, m.row * m.col))
        r3 = Register()
        r3.new_reg()
        end_for(loop1)
        end_for(loop2) if tmp != 1 else None

# Knn
def which(array, val):
    val = "#{}".format(val) if isinstance(val, (int, float)) else val
    m = Matrix.modify_matrix(array, val, "==")
    return m

def quicksort(array, return_indices = False):
    global loop_indx
    print("recur {} {} {}".format(array.col <= 1, array, loop_indx)) # New syntax
    loop_indx += 1
    pivot = array[array.col // 2]
    #left = [x for x in arr if x < pivot]
    left = Matrix(array.row, array.col, "empty", None)
    p = 0
    p = np.make_ptr(array)
    loop1 = np.for_loop(0, array, 1, p)
    print("< {} {}".format(p, pivot))
    r = Register()
    r.new_reg()
    c = Matrix.modify_matrix(left, p, "cbind") # True
    print("+ {}".format(left)) # False 
    r2 = Register()
    r2.new_reg()
    print("ifelse {} {} {}".format(r, c, r2))
    #equal = [x for x in arr if x == pivot]
    equal = Matrix(array.row, array.col, "empty", None)
    p2 = 0
    p2 = np.make_ptr(array)
    loop2 = np.for_loop(0, array, 1, p2)
    print("< {} {}".format(p2, pivot))
    r3 = Register()
    r3.new_reg()
    c2 = Matrix.modify_matrix(equal, p2, "cbind") # True
    print("+ {}".format(equal)) # False 
    r4 = Register()
    r4.new_reg()
    print("ifelse {} {} {}".format(r3, c2, r4))
    #right = [x for x in arr if x > pivot]
    right = Matrix(array.row, array.col, "empty", None)
    p3 = 0
    p3 = np.make_ptr(array)
    loop3 = np.for_loop(0, array, 1, p3)
    print("< {} {}".format(p3, pivot))
    r4 = Register()
    r4.new_reg()
    c3 = Matrix.modify_matrix(right, p3, "cbind") # True
    print("+ {}".format(right)) # False 
    r5 = Register()
    r5.new_reg()
    print("ifelse {} {} {}".format(r4, c3, r5))

    if return_indices:
        #quicksort(left) + which(array, pivot) * equal.col + quicksort(right)
        print("endrecur {} {}".format(left, loop_indx))
        r5 = Register()
        r5.new_reg()
        print("+ {} {}".format(r5, which(array, pivot) * equal.col))
        r6 = Register()
        r6.new_reg()
        print("+ {} {}".format(r6, right))
        r7 = Register()
        r7.new_reg()
    else:
        #quicksort(left) + equal + quicksort(right)
        print("endrecur {} {}".format(left, loop_indx))
        r8 = Register()
        r8.new_reg()
        print("+ {} {}".format(r8, equal))
        r9 = Register()
        r9.new_reg()
        print("+ {} {}".format(r9, right))
        r10 = Register()
        r10.new_reg()

def argsort(array):
    # Default: axis = 1, sort = quicksort
    return quicksort(array, True)
    
# Ida
def identity(n):
        m = zeros((n,n))
        i = 0 
        i = for_index(i)
        loop1 = for_loop(0, n, 1, i)
        j = 0 
        j = for_index(j)
        loop2 = for_loop(0, n, 1, j)
        print("== {} {}".format(i, j))
        r = Register()
        r.new_reg()
        p = Pointer(m, i, j)
        p.new_ptr()
        print("ifelse {} #10 {}".format(r,p))
        r2 = Register()
        r2.new_reg()
        m[i,j] = r2
        end_for(loop2)
        end_for(loop1)
        return m

def abs(arr):
    if isinstance(arr, (int, float)):
        print("abs #{}".format(arr))
        r = Register()
        r.new_reg()
        return r
    else:
        m = Matrix.modify_matrix(arr, None, "abs")
        return m

def diag(matrix):
    if matrix.row != 1:
        # Loop through the zeros matrix on the outside
        m = zeros((1, matrix.col))
        i = 0 
        i = for_index(i)
        loop1 = for_loop(0, m, 1, i)
        j = 0 
        j = for_index(j)
        loop2 = for_loop(0, matrix, 1, j)
        k = 0 
        k = for_index(k)
        loop3 = for_loop(0, matrix, 1, k)
        print("== {} {}".format(j, k))
        r = Register()
        r.new_reg()
        p = Pointer(matrix, j, k)
        p.new_ptr()
        print("ifelse {} {} #0".format(r,p))
        r2 = Register()
        r2.new_reg()
        m[i] = r2
        end_for(loop3)
        end_for(loop2)
        end_for(loop1)
    else: # 1D array
        i = 0 
        i = for_index(i)
        loop1 = for_loop(0, matrix, 1, i)
        m = zeros((matrix.col, matrix.col))
        matrix.col = i
        j = 0 
        j = for_index(j)
        loop2 = for_loop(0, m, 1, j)
        k = 0 
        k = for_index(k)
        loop3 = for_loop(0, m, 1, k)
        print("== {} {}".format(j, k))
        r = Register()
        r.new_reg()
        p = Pointer(matrix, 1, i)
        p.new_ptr()
        print("ifelse {} {} #0".format(r,p))
        r2 = Register()
        r2.new_reg()
        m[j,k] = r2
        end_for(loop3)
        end_for(loop2)
        end_for(loop1)

class linalg:
    def norm(arr):
        # Default is Frobenius norm/2-norm
        f = 0
        i = 0 
        i = for_index(i)
        loop1 = for_loop(0, arr, 1, i)
        tmp = arr.row
        if arr.row != 1:
            j = 0
            j = for_index(j)
            loop2 = for_loop(0, arr, 1, j)
            arr.col = j
            arr.row = i
        else:
            arr.col = i
        a = abs(arr[i, j])
        print("^ {} {}".format(a, 2))
        r = Register()
        r.new_reg()
        f = f + r
        end_for(loop2) if tmp != 1 else None
        end_for(loop1)
        

    def qr(matrix):
        # May need: matrix = matrix.astype(np.float64)
        m, n = matrix.shape
        q = zeros((m, n))
        r = zeros((n, n))
        #for j in range(n):
        j = 0 
        j = for_index(j)
        loop1 = for_loop(0, n, 1, j)
        v = matrix[:, j]
        #for i in range(j):
        i = 0 
        i = for_index(i)
        loop2 = for_loop(0, j, 1, i)
        r[i, j] = dot(q[:, i], matrix[:, j])
        v -= r[i, j] * q[:, i]
        end_for(loop2)
        r[j, j] = np.linalg.norm(v)
        q[:, j] = v / r[j, j]
        end_for(loop1)
        return q, r

    def inv(matrix): # Calculate inverse of a Matrix
        iden = identity(matrix.col)
        m = Matrix.modify_matrix(matrix, iden, "cbind") # Augmented matrix
        i = 0 # Rows
        i = for_index(i)
        loop1 = for_loop(0, m, 1, i)
        p = Pointer(m, i, 0)
        p.new_ptr()
        print("!= {} #0".format(p))
        r = Register()
        r.new_reg()
        print("ifelse {} #1 #0".format(r)) #test in other file
        r2 = Register()
        r2.new_reg()
        end_for(loop1)
        print("== {} #0".format(r2))
        r3 = Register()
        r3.new_reg()
        print("ifelse {}".format(r3))

    def eig(matrix): # Calculate eigenvalues and eigenvectors
        epsilon = 1e-6
        max_iterations = 100
        n = matrix.shape[0]
        eigenvalues = zeros(n)
        eigenvectors = identity(n)

        for _ in range(max_iterations):
            q, r = linalg.qr(matrix)
            matrix = dot(r, q)
            eigenvectors = dot(eigenvectors, q)
            # Check for convergence
            off_diag_sum = sum(abs(matrix - diag(diag(matrix))))
            if off_diag_sum < epsilon:
                break
        for i in range(n):
            eigenvalues[i] = matrix[i, i]
        return eigenvalues, eigenvectors

# Linear Regression
def corrcoef(x, y): # Return Pearson product-moment correlation coefficients
    n = x.col
    mean_x = sum(x) / n
    mean_y = sum(y) / n

    numerator = 0
    l = 0
    l = make_ptr(x)
    loop1 = for_loop(0, x, 1, l)
    xi = x[l]
    yi = y[l]
    numerator += (xi - mean_x) * (yi - mean_y)
    end_for(loop1)

    denominator_x = 0
    k = 0
    k = make_ptr(x)
    loop2 = for_loop(0, x, 1, k)
    print("- {} {}".format(k, mean_x))
    r = Register()
    r.new_reg()
    print("^ {} {}".format(r, "#2"))
    r2 = Register()
    r2.new_reg()
    end_for(loop2)
    sqrt(sum(x))

    denominator_y = 0
    p = 0
    p = make_ptr(y)
    loop3 = for_loop(0, y, 1, p)
    print("- {} {}".format(p, mean_y))
    r3 = Register()
    r3.new_reg()
    print("^ {} {}".format(r, "#2"))
    r4 = Register()
    r4.new_reg()
    end_for(loop3)
    sqrt(sum(y))
    correlation = numerator / (denominator_x * denominator_y)
    return correlation

# Load data
def float32(num): #TODO: backend changes
    print("float32 #{}".format(num))
    r = Register()
    r.new_reg()
    return r

# Naivebytes
def argmax(matrix): # Returns indices of max values along an axis
    if matrix.row != 1:
        m = Matrix(1, matrix.row * matrix.col, "empty", None) # Flatten array
        ctr = 0
        i = 0
        i = for_index(matrix)
        loop1 = for_loop(0, matrix, 1, i)
        j = 0
        j = for_index(matrix)
        loop2 = for_loop(0, matrix, 1, j)
        m[ctr] = matrix[i, j]
        ctr = ctr + 1
        end_for(loop2)
        end_for(loop1)
    else:
        m = matrix
    print("max {}".format(m)) # Max func returns max value
    r = Register()
    r.new_reg()
    n = Matrix.modify_matrix(m, r, "==") # Get index of max value
    p = Pointer(n, 1, 1)
    p.new_ptr()
    return p

# Pca
def conjugate(data):
    if type(data) == Matrix:
        c = Matrix.modify_matrix(data, None, "conjugate")
    else:
        print("conjugate {}".format(data))
        c = Register()
        c.new_reg()
    return c

def cov(matrix): # Estimate a covariance matrix
    transposed = matrix.T
    ddof = 1
    avg = mean(transposed, axis = 1)
    transposed = transposed - avg[:,None]
    fact = transposed.shape[1] - ddof
    tmp = transposed.T
    cmplx_conj = conjugate(tmp)
    c = dot(transposed, cmplx_conj)
    c = c * (1 /fact)
    return c

# Perceptron
def where(cond, true, false): # Return elements chosen from x or y depending on condition
    m = Matrix(cond.row, cond.col, "empty", None)
    i = 0
    i = for_index(cond)
    loop1 = for_loop(0, cond, 1, i)
    print("ifelse {} {} {}".format(cond, true, false))
    r = Register()
    r.new_reg()
    m[i] = r
    end_for(loop1)

def amin(matrix):
    print("min {}".format(matrix))
    r = Register()
    r.new_reg()
    return r

def amax(matrix):
    print("max {}".format(matrix))
    r = Register()
    r.new_reg()
    return r

# Random_forests
def swapaxes(matrix, axis1, axis2):
    return matrix.T


    
    
    
