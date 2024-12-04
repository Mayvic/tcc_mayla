import pandas as pd
import numpy as np
from scipy.stats import entropy

dummys1 = pd.read_csv("data/dummys1.csv")
dummys3 = pd.read_csv("data/dummys3.csv")

#calcula o desvio padrao no array que contem qtDummysXfingerprintSize
def calculateStandardDeviation(dummys):
    dummys = dummys.str.split(',') #lê separando por ','
    dummys = np.array(dummys.tolist(), dtype=float) #cria um array com todos os valores float
    standardDeviation = dummys.std(axis=0) #faz o desvio padrao
    return standardDeviation.mean()



def calculateEntropy(coords):
    # dummys = dummys.str.split(',')
    # dummys = np.array(dummys.tolist(), dtype=float)
    # hist, _ = np.histogram(dummys, density=True) 
    # ent = entropy(hist)
    _, counts = np.unique_counts(coords)
    ent = entropy(counts)
    return ent

def calculateMetrics(dummys):
    dummys["parameter"] = dummys["parameter"].astype(str)
    metrics = dummys.groupby(["idFingerprint", "method", "parameter"]).agg(
        standardDeviation=('dummy', calculateStandardDeviation),
        entropy=('coords', calculateEntropy)
    )
    metrics = metrics.reset_index()
    return metrics

# metrics3 = dummys3.groupby(["idFingerprint", "method", "parameter"]).agg(
#     standardDeviation=('dummy', calculateStandardDeviation),
#     entropy=('dummy', calculateEntropy)
# )
# metrics3 = metrics3.reset_index()
# metrics3.to_csv("metrics3.csv", index=False)