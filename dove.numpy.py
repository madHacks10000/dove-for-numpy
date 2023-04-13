#dove.numpy
#in other file: import dove.numpy as np
#logistic regression
#zeros, dot, sum, exp, array

opNum = 0 #total number of operations
TRANSCRIPT = "transcript.txt"
file = open(TRANSCRIPT, "w")

class Matrix():
    def __init__(self, row, col, name = None, operation = None):
        global opNum
        self.name = name
        self.id = id #need in addition to global variable
        self.row = row
        self.col = col
        self.operation = operation
        opNum += 1
        if self.name == None: #matrix will be modified as specified later on in the user's program
            print("def ${} [1:{}] [1:{}]\n\t{} ".format(opNum, self.row, self.col, self.operation))
        else: #case where external data is used... I think
             print("def ${} [1:{}] [1:{}]\n\tdataset {}\nend ${}".format(self.id, self.row, self.col, self.name, self.id))

    def newMatrix(self, operand, operation):
        tmp = Matrix(self.row, self.col, None, operation)
        print("${} ${}\nend ${}".format(self.id, operand, tmp.id)) 
        return tmp

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



    
    
    
    
    
