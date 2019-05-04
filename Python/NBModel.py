import csv
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression as LR
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from random import choice
from keras.models import Sequential
from keras.layers import Dense

from sklearn.decomposition import PCA
import sys
import numpy as np
class dataprocess:
    # Method to fetch the CSV Data
    def loadcsv(self,filepath):
        with open(filepath, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            data = list(reader)
            return data

    # Clean up
    def cleanup(self, data):
        X = [[float(x) for x in y[1:]] for y in data]
        Y = [x[0] for x in data]
        return X,Y

    # Fetch Data
    def fetch_data(self, flag=True):
        # Load CSV
        data_test = self.loadcsv('data_test.csv')
        data_train = self.loadcsv('data_train.csv')
        # Clean up module
        if flag == True:
            X_train, Y_train = self.cleanup(data_train)

        X_test, Y_test = self.cleanup(data_test)

        if flag == True:
            return X_train, Y_train, X_test, Y_test
        else:
            return X_test, Y_test

class Models(dataprocess):
    #Extract user from url
    def getUser(self):
        query = os.environ['QUERY_STRING']
        user = query.split("=")[1]
        return user

    # Fit the Data
    def nb_fit(self, filename):
        data_tr, label_tr, data_ts, label_ts = self.fetch_data()
        dicky = {'S1': 1, 'S10': 2, 'S100': 3, 'S101': 4, 'S102': 5, 'S103': 6, 'S104': 7, 'S105': 8, 'S106': 9,
                 'S107': 10}
        #dicky = {'S1': 1, 'S2': 2, 'S3': 3, 'S4': 4, 'S5': 5, 'S6': 6, 'S7': 7, 'S8': 8, 'S9': 9, 'S10': 10}
        label_ts = [dicky[x] for x in label_ts]
        label_tr = [dicky[x] for x in label_tr]
        gnb = GaussianNB()
        gnb.fit(data_tr, label_tr)
        joblib.dump(gnb, filename)
        predict = gnb.predict(data_ts)
        accuracy = [1 if predict[i] == label_ts[i] else 0 for i in range(len(predict))]
        accuracy = sum(accuracy)/len(accuracy)
        print('The Gaussian Accuracy is ', accuracy)

    def svm_fit(self, kernel):
        data_tr, label_tr, data_ts, label_ts = self.fetch_data()
        if kernel == 'poly':
            svm = SVC(kernel=kernel, degree=5, gamma='scale')
        else:
            svm = SVC(kernel=kernel, gamma='scale')
        print('data has been fitted')
        svm.fit(data_tr, label_tr)
        predict = svm.predict(data_ts)
        self.dumpcsv(self.file_prd, predict)

        accuracy = [1 if predict[i] == label_ts[i] else 0 for i in range(len(predict))]
        accuracy = sum(accuracy) / len(accuracy)
        print('The SVM ', kernel, ' accuracy: ', accuracy)

    def lr_fit(self, filename='Model_LR.sav'):
        data_tr, label_tr, data_ts, label_ts = self.fetch_data()
        dicky = {'S1':1, 'S10':2, 'S100':3, 'S101':4, 'S102':5, 'S103':6, 'S104':7, 'S105':8, 'S106':9, 'S107':10 }
        #dicky = {'S1':1, 'S2': 2, 'S3': 3, 'S4': 4, 'S5':5, 'S6':6, 'S7':7, 'S8':8, 'S9':9, 'S10':10}
        label_ts = [dicky[x] for x in label_ts]
        label_tr = [dicky[x] for x in label_tr]

        # data_tr =StandardScaler().fit_transform(data_tr)
        # data_ts =StandardScaler().fit_transform(data_ts)

        # pca = PCA(n_components=10)
        # data_tr = pca.fit_transform(data_tr)
        # data_ts = pca.fit_transform(data_ts)

        print('PCA done')

        regression_model = LR(C=1e5, solver='lbfgs',multi_class='multinomial')
        regression_model.fit(data_tr, label_tr)

        joblib.dump(regression_model, filename)
        # Print the coefficients of training
        print('Coefficients: ', regression_model.intercept_, regression_model.coef_)

        # Make predictions based on training
        predict = regression_model.predict(data_ts)
        accuracy = [1 if predict[i] == label_ts[i] else 0 for i in range(len(predict))]
        accuracy = sum(accuracy) / len(accuracy)

        print('Accuracy: ', accuracy)

    def knn_fit(self, file):
        data_tr, label_tr, data_ts, label_ts = self.fetch_data()
        #dicky = {'S1':1, 'S2': 2, 'S3': 3, 'S4': 4, 'S5':5, 'S6':6, 'S7':7, 'S8':8, 'S9':9, 'S10':10}
        dicky = {'S1': 1, 'S10': 2, 'S100': 3, 'S101': 4, 'S102': 5, 'S103': 6, 'S104': 7, 'S105': 8, 'S106': 9,
                 'S107': 10}
        label_ts = [dicky[x] for x in label_ts]
        label_tr = [dicky[x] for x in label_tr]
        data_tr = StandardScaler().fit_transform(data_tr)
        data_ts = StandardScaler().fit_transform(data_ts)

        knn_model = KNeighborsClassifier(n_neighbors=3, n_jobs=-1)
        knn_model.fit(data_tr, label_tr)
        joblib.dump(knn_model, file)
        predict = knn_model.predict(data_ts)
        accuracy = metrics.accuracy_score(predict, label_ts)
        print(accuracy)


    def test(self, user, filepath, flag=True):
        #data_tr, label_tr, data_ts, label_ts = self.fetch_data()
        data_ts, label_ts = self.fetch_data(flag=False)
        dicky = {'S1': 1, 'S10': 2, 'S100': 3, 'S101': 4, 'S102': 5, 'S103': 6, 'S104': 7, 'S105': 8, 'S106': 9,
                  'S107': 10}
        #dicky = {'S0': 1, 'S1': 2, 'S2': 3, 'S3': 4, 'S4': 5, 'S5': 6, 'S6': 7, 'S7': 8, 'S8': 9, 'S9': 10}
        #dicky = {'S1': 1, 'S2': 2, 'S3': 3, 'S4': 4, 'S5': 5, 'S6': 6, 'S7': 7, 'S8': 8, 'S9': 9, 'S10': 10}
        label_ts = [dicky[x] for x in label_ts]

        index = [i for i, x in enumerate(label_ts) if x == int(user)]
        if flag == True:
            test = data_ts[choice(index)]
        else:
            index1 = index[0] + 65
            test = data_ts[index[0]:index1]
        model = joblib.load(filepath)

        predict = model.predict([test])
        predict_prob = model.predict_proba([test])
        print(predict_prob)
        predict_prob = np.array(predict_prob[0])
        predictions = [x + 1 for x in predict_prob.argsort()[-3:][::-1]]

        print(predict)
        print('\n')
        print(predictions)

        if user in predictions:
            output = '1'
        else:
            output = '0'
        print(output)

    def neural_fit(self, filepath):
        data_tr, label_tr, data_ts, label_ts = self.fetch_data()
        #dicky = {'S1': 1, 'S2': 2, 'S3': 3, 'S4': 4, 'S5': 5, 'S6': 6, 'S7': 7, 'S8': 8, 'S9': 9, 'S10': 10}
        dicky = {'S1': 1, 'S10': 2, 'S100': 3, 'S101': 4, 'S102': 5, 'S103': 6, 'S104': 7, 'S105': 8, 'S106': 9,
                 'S107': 10}
        label_ts = [dicky[x] for x in label_ts]
        label_tr = [dicky[x] for x in label_tr]

        data_tr = np.array(data_tr)
        label_tr = np.array(label_tr)
        data_ts = np.array(data_ts)
        label_ts = np.array(label_ts)

        # Create Model
        model = Sequential()
        model.add(Dense(12, input_dim=65, activation='relu'))
        model.add(Dense(8, activation='relu'))
        model.add(Dense(1, activation='sigmoid'))

        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Fit the model
        model.fit(data_tr, label_tr, epochs=20, batch_size=10)
        joblib.dump(model, filepath)
        # evaluate the model
        scores = model.evaluate(data_ts, label_ts)
        print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

#user =  input("Which user are you? (1-10)")  #sys.argv[1]
nb = Models()
nb.nb_fit('NB_Model.sav')
print('Training is done')
# # print('\n')
# nb.test(user, 'Model_LR.sav')
# #nb.lr_fit()

