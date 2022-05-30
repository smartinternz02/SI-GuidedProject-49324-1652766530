# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pickle

dataset = pd.read_csv('3d printer modified.csv')

dataset['roughness'].fillna(dataset['roughness'].mean(), inplace=True)

dataset['tension_strenght'].fillna(dataset['tension_strenght'].mean(), inplace=True)

dataset['elongation'].fillna(dataset['elongation'].mean(), inplace=True)

material = {'abs': 0, 'pla': 1}
dataset.material = [material[item] for item in dataset.material]

X = dataset.loc[:, ['roughness','tension_strenght','elongation']]

from sklearn import preprocessing
minmax=preprocessing.MinMaxScaler(feature_range=(0,1))
minmax.fit(X).transform(X)


y = dataset.iloc[:, -1]

#Splitting Training and Test Set
#Since we have a very small dataset, we will train our model with all availabe data.

from sklearn import model_selection, neighbors
clf = neighbors.KNeighborsClassifier()

#Fitting model with trainig data
clf.fit(X,y)

# Saving model to disk
pickle.dump(clf, open('model.pkl','wb'))

# Loading model to compare the results
model = pickle.load(open('model.pkl','rb'))
print(model.predict([[21, 14, 1.5]]))