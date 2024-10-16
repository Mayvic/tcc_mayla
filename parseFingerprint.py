# %%
import pandas as pd
import numpy as np
from dataclasses import dataclass

# %%
#print('Hello World!')
@dataclass
class ambiente:
    coord: str
    trace: str
    exitFile: str

ambiente1 = ambiente('pos-1000-20-20-1-7-9-0-1-1','trace-1000-20-20-1-7-9-0-1-1','fingerprints1');
ambiente3 = ambiente('pos-1000-20-20-3-7-9-0-1-1','trace-1000-20-20-3-7-9-0-1-1','fingerprints3');

usedAmbiente = ambiente3

coordPoints = pd.read_csv(usedAmbiente.coord, sep='\t', header=None, names=['id', 'coord'])

# %%
trace = pd.read_csv(usedAmbiente.trace, sep='\t', header=None, names=['timestamp', 'transmissor', 'receptor', 'snr'])

# %%
trace = trace.sort_values(['receptor','transmissor','timestamp']) #ordena na ordem dos parãmetros

# %%
trace['time'] = np.floor(trace.timestamp) #corta o tempo em inteiro

# %%
groupedByTime = trace.groupby(['receptor','transmissor','time'], as_index= False).agg({'snr':'mean'}) #calcula a media do snr para cada par receptor-transmissor no tempo X

# %%
groupedByReceptor = groupedByTime.pivot(columns='transmissor', index=['receptor','time'],values='snr') #indexa o snr de cada transmissor ao par receptor-tempo

# %%
groupedByReceptor= groupedByReceptor-98 # calcula o dbm

# %%

#groupedByReceptor = groupedByReceptor.dropna() #apaga todos os NAN
#groupedByReceptor = groupedByReceptor.fillna(0) #substitui todos os NAN
groupedByReceptor = groupedByReceptor.apply(lambda line: ','.join(line.astype(str)),axis=1) #junta todos os dbm para formar o vetor fingerprint
groupedByReceptor = groupedByReceptor.rename('fingerprint') 

# %%
coordPoints.id = coordPoints.index + 1 #acerta o index para que a contagem de transmissores e receptores seja continua
coordPoints.id = coordPoints.id.map(lambda id : '00:00:00:00:00:{:02X}'.format(id)) #formata e converte o index para HEX

# %%
groupedByReceptor= groupedByReceptor.reset_index() #receptor e time voltam a ser colunas

# %%
fingerprint1 = groupedByReceptor.merge(coordPoints,how='left',  left_on='receptor', right_on='id') #juntas as duas tabelas

# %%
fingerprint1 = fingerprint1[['coord', 'fingerprint']] #remove os campos extras

# %%
fingerprint1.to_csv(usedAmbiente.exitFile, '\t', index=False, header=False)
