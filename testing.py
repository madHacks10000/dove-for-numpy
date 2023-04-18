#File for testing syntax outputs correctly
import dove_numpy.dove_numpy as np


test1 = np.Matrix(2, 2, "test1") #but this isn't realistic??
test2 = np.Matrix(2, 2, "test2")
dotproduct = np.dot(test1, test2)
zeromatrix = np.zeros((2, 1))
matrix = np.Matrix('1 2; 3 4')
sum = np.sum(matrix)
