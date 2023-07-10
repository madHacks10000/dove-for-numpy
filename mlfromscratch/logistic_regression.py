#import numpy as np
import sys
sys.path.append('../')
import dove_numpy.dove_numpy as np

class LogisticRegression:
    def __init__(self, learning_rate=0.001, n_iters=1000):
        self.lr = learning_rate
        self.n_iters = n_iters
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape

        # init parameters
        self.weights = np.zeros(n_features)
        self.bias = 0

        # gradient descent
        #for _ in range(self.n_iters):
        iter_obj = 0 
        iter_obj = np.for_index(iter_obj)
        loop1 = np.for_loop(0, self.n_iters, 1, iter_obj)

        # approximate y with linear combination of weights and x, plus bias
        #X type: numpy array
        #self.weight: Matrix
        #self.bias: float
        linear_model = np.dot(X, self.weights) + self.bias #self.weights = None
        # apply sigmoid function
        y_predicted = self._sigmoid(linear_model) 
        # compute gradients
        dw = (1 / n_samples) * np.dot(X.T, (y_predicted - y)) 
        db = (1 / n_samples) * np.sum(y_predicted - y)
        # update parameters
        self.weights -= self.lr * dw
        self.bias -= self.lr * db
        np.end_for(loop1)
        
    def predict(self, X):
        linear_model = np.dot(X, self.weights) + self.bias
        y_predicted = self._sigmoid(linear_model)

        #y_predicted_cls = [1 if i > 0.5 else 0 for i in y_predicted] <-- original statement
        #for i in y_predicated:
        #    if i > 0.5:
        #        y_predicated_cls.append(1)
        #    else:
        #        y_predicated_cls.append(0)
        y_predicted_cls = []
        i = 0 
        i = np.for_index(i)
        loop1 = np.for_loop(0, y_predicted, 1, i)
        result = np.if_else(y_predicted[i] > 0.5, 1, 0)
        y_predicted_cls.append(result)
        np.end_for(loop1)
        return np.array(y_predicted_cls)

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))


# Testing
if __name__ == "__main__":
    # Imports
    from sklearn.model_selection import train_test_split
    from sklearn import datasets
    from dove_numpy.dove_numpy import Matrix 

    def accuracy(y_true, y_pred):
        accuracy = np.sum(y_true == y_pred) / len(y_true)
        return accuracy

    bc = datasets.load_breast_cancer()
    X, y = bc.data, bc.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=1234
    )

    X = Matrix(X.shape[0], X.shape[1], "X")
    y = Matrix(1, y.shape[0], "y")
    X_train = Matrix(X_train.shape[0], X_train.shape[1], "X_train")
    X_test = Matrix(X_test.shape[0], X_test.shape[1], "X_test")
    y_train = Matrix(1, y_train.shape[0], "y_train")
    y_test = Matrix(1, y_test.shape[0], "y_test")

    regressor = LogisticRegression(learning_rate=0.0001, n_iters=1000)
    regressor.fit(X_train, y_train)
    predictions = regressor.predict(X_test)

    print("LR classification accuracy:", accuracy(y_test, predictions))
