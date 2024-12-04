import pandas as pd
import numpy as np
from source.ambiente import usedAmbiente

coordPoints = pd.read_csv(usedAmbiente.coord, sep='\t', header=None, names=['id', 'coord'])

trace = pd.read_csv(usedAmbiente.trace, sep='\t', header=None, names=['timestamp', 'transmissor', 'receptor', 'snr'])

trace = trace.sort_values(['receptor','transmissor','timestamp']) #ordena na ordem dos parãmetros
aps = ['00:00:00:00:00:01','00:00:00:00:00:02','00:00:00:00:00:03','00:00:00:00:00:04','00:00:00:00:00:05','00:00:00:00:00:06','00:00:00:00:00:07']
trace = trace[~trace.receptor.isin(aps)]

coordPoints = coordPoints.iloc[7:]

trace['time'] = np.floor(trace.timestamp) #corta o tempo em inteiro

groupedByTime = trace.groupby(['receptor','transmissor','time'], as_index= False).agg({'snr':'mean'}) #calcula a media do snr para cada par receptor-transmissor no tempo X

groupedByReceptor = groupedByTime.pivot(columns='transmissor', index=['receptor','time'],values='snr') #indexa o snr de cada transmissor ao par receptor-tempo

groupedByReceptor= groupedByReceptor-98 # calcula o dbm

#groupedByReceptor.isna().groupby(level=0).sum().to_csv('nan.tsv', '\t') #visualiza quantos NAN tem AP-RP
#groupedByReceptor[groupedByReceptor['id'].isna()].receptor.unique()

groupedByReceptor = groupedByReceptor.dropna() #apaga todos os NAN
groupedByReceptor = groupedByReceptor.apply(lambda line: ','.join(line.astype(str)),axis=1) #junta todos os dbm para formar o vetor fingerprint
groupedByReceptor = groupedByReceptor.rename('fingerprint') 

coordPoints.id +=8 #acerta o index para que a contagem de transmissores e receptores seja continua
coordPoints.id = coordPoints.id.map(lambda id : '00:00:00:00:00:{:02X}'.format(id).lower()) #formata e converte o index para HEX

groupedByReceptor= groupedByReceptor.reset_index() #receptor e time voltam a ser colunas

fingerprint = groupedByReceptor.merge(coordPoints,how='left',  left_on='receptor', right_on='id') #juntas as duas tabelas

fingerprint = fingerprint[['coord', 'fingerprint']] #remove os campos extras

fingerprint.to_csv(usedAmbiente.exitFile, '\t', index=False, header=False)
