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
        def func1(obj):
            # approximate y with linear combination of weights and x, plus bias
            #X type: numpy array
            #self.weight: Matrix
            #self.bias: float
            linear_model = np.dot(X, self.weights) + self.bias #self.weights = None
            # apply sigmoid function
            y_predicted = self._sigmoid(linear_model) 

            dw = (1 / n_samples) * np.dot(X.T, (y_predicted - y)) 
            db = (1 / n_samples) * np.sum(y_predicted - y)
        
            self.weights -= self.lr * dw
            self.bias -= self.lr * db
        
        #for _ in range(self.n_iters):
        iter_obj = 0 
        iter_obj = np.for_index(iter_obj)
        np.for_loop(0, self.n_iters, 1, func1, iter_obj)

    def predict(self, X):
        linear_model = np.dot(X, self.weights) + self.bias
        y_predicted = self._sigmoid(linear_model)

        #replacing if-else with a function that emits the correct DOT syntax
        #y_predicted_cls = [1 if i > 0.5 else 0 for i in y_predicted] <-- original statement
        y_predicted_cls = []
        
        def func2(obj):
            np.if_else(y_predicted[i] > 0.5, 1, 0)

        i = 0 
        i = np.for_index(i)
        np.for_loop(0, y_predicted, 1, func2, i)

        #for i in y_predicated:
        #    if i > 0.5:
        #        y_predicated_cls.append(1)
        #    else:
        #        y_predicated_cl.append(0)
        return np.array(y_predicted_cls)

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-x))


# Testing
if __name__ == "__main__":
    # Imports
    from sklearn.model_selection import train_test_split
    from sklearn import datasets
    import numpy as n

    def accuracy(y_true, y_pred):
        accuracy = np.sum(y_true == y_pred) / len(y_true)
        return accuracy

    bc = datasets.load_breast_cancer()
    X, y = bc.data, bc.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=1234
    )

    X = np.array(X)
    y = np.array(y)
    X_train = np.array(X_train)
    X_test = np.array(X_test)
    y_train = np.array(y_train)
    y_test = np.array(y_test)

    regressor = LogisticRegression(learning_rate=0.0001, n_iters=1000)
    regressor.fit(X_train, y_train)
    predictions = regressor.predict(X_test)

    print("LR classification accuracy:", accuracy(y_test, predictions))
