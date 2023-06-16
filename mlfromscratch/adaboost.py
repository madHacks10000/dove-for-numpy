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
        self.clfs = np.array(self.clfs)

    def fit(self, X, y):
        n_samples, n_features = X.shape

        # Initialize weights to 1/N
        w = np.full(n_samples, (1 / n_samples))
        
        self.clfs = []
        self.clfs = np.array(self.clfs)

        # Iterate through classifiers

        # for _ in range(self.n_clf):
        def func1(obj, self, X, y, w, n_features, n_samples, *args): #self.clfs was a slight issue
            clf = DecisionStump()
            min_error = float("inf")

            # greedy search to find best threshold and feature
            #for feature_i in range(n_features):
            def func2(obj, self, X, y, w, n_features, n_samples, min_error, *args):
                
                X_column = X[:, feature_i]
                thresholds = np.unique(X_column)

                #for threshold in thresholds:
                def func3(obj, y, w, n_samples, X_column, min_error, *args):
                    
                    # predict with polarity 1
                    p = 1
                    predictions = np.ones(n_samples)
                    predictions[X_column < threshold] = -1

                    # Error = sum of weights of misclassified samples
                    misclassified = w[y != predictions]
                    error = np.sum(misclassified)

                    if error > 0.5:
                        error = 1 - error
                        p = -1

                    # store the best configuration
                    if error < min_error:
                        clf.polarity = p
                        clf.threshold = threshold
                        clf.feature_idx = feature_i
                        min_error = error

                threshold = 0
                threshold = np.make_ptr(thresholds)
                np.for_loop(0, thresholds, 1, func3, threshold, y, w, n_samples, X_column, min_error)
            
            feature_i = 0 
            feature_i = np.for_index(feature_i)
            np.for_loop(0, n_features, 1, func2, feature_i, self, X, y, w, n_features, n_samples, min_error)

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
        
        loop_var = 0
        loop_var = np.for_index(loop_var)
        
        np.for_loop(0, self.n_clf, 1, func1, loop_var, self, X, y, w, n_features, n_samples, loop_var) # for _ in range(self.n_clf):

    def predict(self, X):
        #clf_preds = [clf.alpha * clf.predict(X) for clf in self.clfs] 
        #or:
        #clf_preds = []
        #for clf in self.clfs:
            #prediction = clf.alpha * clf.predict(X)  # Calculate the prediction for current clf
            #clf_preds.append(prediction)
        
        
        def func4(obj, clf_preds, X, *args):
            prediction = clf.alpha * clf.predict(X)
            clf_preds.append(prediction)

        clf = 0
        clf_preds = []
        clf = np.make_ptr(self.clfs) #self.clfs is a list and clf is now a register
        np.for_loop(0, self.clfs, 1, func4, clf, clf_preds, X)

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
