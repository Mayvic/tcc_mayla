import numpy as np
import pandas as pd

from source.modelo import datasetTest1, datasetTest3

class fingerprint:
    id: int
    value: list

parameterCount = 4
parameters = {
    'swap': [2, 3, 4, 5],
    'shift': [1, 2, 3, 4],
    'math': [(40, 1), (40, 3), (20, 1), (20, 3)],
    'mathVector': [10, 20, 40, 60],
    'mathMatrix': [0.05, 0.1, 0.2, 0.4]
}

#printa o fingerprint e os dummys
def printFingerprintAndDummys(dummys,fingerprint): 
    print("f",fingerprint)
    for d in dummys:
        print("d",d)

#altera o valor de qtPos posições aleatórias do fingerprint
def generateDummySwap(fingerprint, qtPos=2): 
    #qtPos = qt de posições a serem alteradas
    dummysResp = fingerprint.copy()
    randomPos = np.random.choice(range(0,len(fingerprint)-1),qtPos, replace=False) 
    #sorteia qtPos posições entre 0 e 7(tamanho do fingerprint) com valores unicos(replace=False)
    pos =[]
    for rp in randomPos:
        pos.append(fingerprint[rp]) #cria um vetor so com as posições sorteadas
    pos = pos[1:] + pos[: 1] #muda as posições do vetor
    i=0
    for rp in randomPos:
        dummysResp[rp] = pos[i] #volta os valores, agora com as posições trocadas, para o vetor original
        i=i+1
    return dummysResp

#realiza o shift left das posições do fingerprint
def generateDummyShift( fingerprint, qtPos=1):
    #qtPos = qt de posições a serem alteradas
    pos = (qtPos) % len(fingerprint) 
    #a cada dummy ira alterar (qtPos) casas
    #caso esse valor seja maior que o tamanho do vetor é feito o modulo
    dummyResp =  fingerprint[pos:] + fingerprint[: pos]
    return dummyResp

#soma um valor aleatório a qtPos aleatorias do fingerprint
def generateDummyMath( fingerprint, value, qtPos=1):
    #qtPos = qt de posições a serem alteradas
    #if(not value): value = np.random.random() * 20 -10 #sorteia um valor para ser somado
    dummysResp = fingerprint.copy()
    randomPos = np.random.choice(range(0,len(fingerprint)-1),qtPos, replace=False)
    #sorteia qtPos posições entre 0 e 7(tamanho do fingerprint) com valores unicos(replace=False)
    #print(randomPos)
    for rp in randomPos:
            dummysResp[rp] += value #soma o valor apenas nas posições sorteadas
    return dummysResp

#soma um vetor aleatório ao fingerprint
def generateDummyMathVector( fingerprint, vector):
    dummysResp=[]
    #if(not vector): vector = np.random.random(len(fingerprint)) * 20 -10  #sorteia um vetor de valores para ser somado
    dummysResp = np.add(fingerprint,vector) #soma os vetores
    return dummysResp

#multiplica uma matriz aleatória próxima a identidade pelo fingerprint 
def generateDummyMathMatrix(fingerprint, variation=0.1):
    #qtDummy = qt de fingerprints dummy a serem criados
    matrix = np.eye(len(fingerprint)) #cria a matriz aleatoria do tamanho do fingerprint
    qtPos = np.random.randint(0,10) #sorteia uma quantidade de posições da matriz identidade para ser alterada
    for rnd in range(qtPos):
        posX = np.random.randint(0,len(fingerprint)) #sorteia uma posição X
        posY = np.random.randint(0,len(fingerprint)) #sorteia uma posição Y
        value = np.random.uniform(-variation, variation)#sorteia um valor entre -variation e variation
        matrix[posX][posY] += value #soma o valor na posição [X][Y] da matriz
    dummysResp = np.matmul(matrix,fingerprint) #multiplica a matriz pelo fingerprint
    return dummysResp

#cria o item no formato certo para ser salvo no arquivo
def createItemDataFrame(idFingerprint, dummy, method, parameter):
    # print( 'id', idFingerprint)
    # print( 'dummy', dummy)
    # print( 'method', method)
    # print( 'parameters', parameter)
    dummyStr = ','.join([str(x) for x in dummy])
    return pd.DataFrame({
            'idFingerprint': [idFingerprint],
            'dummy': [dummyStr],
            'method': [method],
            'parameter': [parameter]
        })

#cria dummys para todos os metodos variando os parametros dentro do range passado como parametro
def createAllDummys(qtDummy, fingerprint):
    dummys = pd.DataFrame(columns=['idFingerprint','dummy','method','parameter'])
    dummysSwap = []
    dummysShift = []
    dummysMath = []
    dummysMathVector = []
    dummysMathMatrix = []

#itera sobre os parametros de teste
    for i in range(parameterCount):
        #parameter SWAP
        qtPosSwap = parameters['swap'][i]
        #parameter SHIFT
        qtPosShift = parameters['shift'][i]
        #parameter MATH
        variationMath = parameters['math'][i][0]
        qtPosMath = parameters['math'][i][1]
        #parameter VECTOR
        variationVector = parameters['mathVector'][i]
        #parameter MATRIX
        variationMatrix = parameters['mathMatrix'][i]
        
        fgps = []
        fgps.append(createItemDataFrame(fingerprint.id, fingerprint.value, 'swap', qtPosSwap))
        fgps.append(createItemDataFrame(fingerprint.id, fingerprint.value, 'shift', qtPosShift))
        fgps.append(createItemDataFrame(fingerprint.id, fingerprint.value, 'math', (variationMath, qtPosMath)))
        fgps.append(createItemDataFrame(fingerprint.id, fingerprint.value, 'mathVector', variationVector))
        fgps.append(createItemDataFrame(fingerprint.id, fingerprint.value, 'mathMatrix', variationMatrix))
        fgps = pd.concat(fgps)
        dummys = pd.concat([dummys, fgps])
        
        #itera sobre a quantidade de dummys a serem criados
        for j in range(0,qtDummy):
            ####SWAP
            swap= generateDummySwap(fingerprint.value,qtPosSwap)
            dummysSwap = createItemDataFrame(fingerprint.id, swap, 'swap', qtPosSwap)
            dummys = pd.concat([dummys,dummysSwap])

            ####SHIFT
            shift = generateDummyShift(fingerprint.value,qtPosShift+j)
            dummysShift = createItemDataFrame(fingerprint.id, shift, 'shift', qtPosShift)
            dummys = pd.concat([dummys,dummysShift])

            ####MATH
            valueMath = np.random.uniform(-variationMath,variationMath) #sorteia um valor para ser somado
            math = generateDummyMath(fingerprint.value, valueMath, qtPosMath)
            dummysMath = createItemDataFrame(fingerprint.id, math, 'math', (variationMath, qtPosMath))
            dummys = pd.concat([dummys,dummysMath])

            ####VECTOR
            vector = np.random.uniform(-variationVector,variationVector,len(fingerprint.value))  #sorteia um vetor de valores para ser somado
            mathVector = generateDummyMathVector(fingerprint.value,vector)
            dummysMathVector = createItemDataFrame(fingerprint.id, mathVector, 'mathVector', variationVector)
            dummys = pd.concat([dummys,dummysMathVector])

            ####MATRIX
            ##testar valores de alteração da matriz 
            mathMatrix = generateDummyMathMatrix(fingerprint.value, variationMatrix)
            dummysMathMatrix = createItemDataFrame(fingerprint.id, mathMatrix, 'mathMatrix', variationMatrix)
            dummys = pd.concat([dummys,dummysMathMatrix])
    return dummys

def createAndSaveDummys(dataset, qtDummy, filename):
    fingerprint1 = fingerprint()
    allDummys = []
    for index, values in dataset.iterrows(): #itera sobre os fingerprints do conjunto de teste
        fingerprint1.id = index #referencia o id na tabela de dados inicial
        fingerprint1.value = values.tolist()
        dummysOneFingerprint = createAllDummys(qtDummy,fingerprint1)
        allDummys.append(dummysOneFingerprint)
    dummys = pd.concat(allDummys)
    dummys.to_csv(filename, ',', index=False)
    return dummys
