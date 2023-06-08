import sys
sys.path.append('../')
import dove_numpy.dove_numpy as np

#init data- move to separate file later


# Decision stump used as weak classifier
class DecisionStump:
    def __init__(self):
        self.polarity = 1
        self.feature_idx = None
        self.threshold = None
        self.alpha = None

    def predict(self, X):
        n_samples = X.shape[0]
        X_column = X[:, self.feature_idx]
        predictions = np.ones(n_samples)
        if self.polarity == 1:
            predictions[X_column < self.threshold] = -1
        else:
            predictions[X_column > self.threshold] = -1

        return predictions


class Adaboost:
    def __init__(self, n_clf=5):
        self.n_clf = n_clf
        self.clfs = []

    def fit(self, X, y):
        n_samples, n_features = X.shape

        # Initialize weights to 1/N
        w = np.full(n_samples, (1 / n_samples))
        
        self.clfs = []
        
        # Iterate through classifiers

        #for _ in range(self.n_clf):
        loop_var = 0
        loop_var = np.for_index(loop_var)
        np.for_loop(0, self.n_clf, 1, loop_var)
        clf = DecisionStump()
        min_error = float("inf")

        # greedy search to find best threshold and feature
        #for feature_i in range(n_features):
        feature_i = 0 
        feature_i = np.for_index(feature_i)
        np.for_loop(0, n_features, 1, feature_i)
        X_column = X[:, feature_i] #ndarray
        
        thresholds = np.unique(X_column)

        #for threshold in thresholds:
        threshold = 0
        threshold = np.for_index(threshold)
        np.for_loop(0, thresholds, 1, threshold)
        # predict with polarity 1
        p = 1
    
        predictions = np.ones(n_samples)
    
        #print(type(threshold)) #Register

        predictions[X_column < threshold] = -1

        # Error = sum of weights of misclassified samples
        misclassified = w[y != predictions]
        error = np.sum(misclassified) #used to be just sum(misclassified)

        if error > 0.5:
            error = 1 - error
            p = -1

        # store the best configuration
        if error < min_error:
            clf.polarity = p
            clf.threshold = threshold
            clf.feature_idx = feature_i
            min_error = error

        np.end_for(0) #TODO: make this more efficient
        np.end_for(1)

        # calculate alpha
        EPS = 1e-10
        clf.alpha = 0.5 * np.log((1.0 - min_error + EPS) / (min_error + EPS))

        # calculate predictions and update weights
        predictions = clf.predict(X)

        w *= np.exp(-clf.alpha * y * predictions)
        # Normalize to one
        w /= np.sum(w)

        # Save classifier
        self.clfs.append(clf)
        
        np.end_for(2)
            

    def predict(self, X):
        clf_preds = [clf.alpha * clf.predict(X) for clf in self.clfs]
        y_pred = np.sum(clf_preds, axis=0)
        y_pred = np.sign(y_pred)

        return y_pred


# Testing
if __name__ == "__main__":
    # Imports
    from sklearn import datasets
    from sklearn.model_selection import train_test_split
    import sys
    sys.path.append('../')
    import dove_numpy.dove_numpy as np      

    def accuracy(y_true, y_pred):
        accuracy = np.sum(y_true == y_pred) / len(y_true)
        return accuracy

    data = datasets.load_breast_cancer()
    X, y = data.data, data.target

    # Manually convert
    #X = np.array(X)
    #y = np.array(y)

    y[y == 0] = -1

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=5
    )

    #Temporary solution
    X = np.array(X)
    y = np.array(y)
    X_train = np.array(X_train)
    X_test = np.array(X_test)
    y_train = np.array(y_train)
    y_test = np.array(y_test)

    # Adaboost classification with 5 weak classifiers
    clf = Adaboost(n_clf=5)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    acc = accuracy(y_test, y_pred)
    print("Accuracy:", acc)
