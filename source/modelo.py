import pandas as pd
import pickle
import os
from source.ambiente import ambiente1, ambiente3
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

def trainModel(file):
    knn = KNeighborsClassifier(n_neighbors=1)
    fingerprintsData = pd.read_csv(file, sep='\t', header=None, names=['coord', 'fingerprint'])
    fingerprints = fingerprintsData.fingerprint.str.split(',').apply(pd.Series).astype(float)
    coordTrain, coordTest, fingerprintsTrain, fingerprintsTest  = train_test_split(fingerprintsData.coord, fingerprints, train_size=0.7,random_state=8)
    knn.fit(fingerprintsTrain, coordTrain)
    return fingerprintsTest, coordTest, knn

def saveFiles(fingerprintsTest, coordTest, knn, suffix):
    fingerprintsTest.to_csv(f'data/fingerprints_test{suffix}.csv', index=True)
    coordTest.to_csv(f'data/coord_test{suffix}.csv', index=True)
    with open(f'models/knn{suffix}.pkl', 'wb') as fp:
        pickle.dump(knn, fp)

def loadFiles(suffix):
    fingerprintsTest = pd.read_csv(f'data/fingerprints_test{suffix}.csv', index_col=0)
    coordTest = pd.read_csv(f'data/coord_test{suffix}.csv', index_col=0)
    with open(f'models/knn{suffix}.pkl', 'rb') as fp:
        knn = pickle.load(fp)
    return fingerprintsTest, coordTest, knn

if os.path.exists('models/knn1.pkl'):
    fingerprintsTest1, coordTest1, knn1 = loadFiles('1')
else:
    fingerprintsTest1, coordTest1, knn1 = trainModel(ambiente1.exitFile)
    saveFiles(fingerprintsTest1, coordTest1, knn1, '1')

knn1.predict(fingerprintsTest1.iloc[[0]]) #encontra um ponto

if os.path.exists('models/knn3.pkl'):
    fingerprintsTest3, coordTest3, knn3 = loadFiles('3')
else:
    fingerprintsTest3, coordTest3, knn3 = trainModel(ambiente3.exitFile)
    saveFiles(fingerprintsTest3, coordTest3, knn3, '3')

knn3.predict(fingerprintsTest3.iloc[[0]]) #encontra um ponto


datasetTest1 = {'fingerprints': fingerprintsTest1 , 'coord': coordTest1 }

datasetTest3 = {'fingerprints': fingerprintsTest3 , 'coord': coordTest3 }