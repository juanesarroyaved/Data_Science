"""
#-------------------------------------------------------------------------
# Author: John Alexander Garzón Vásquez , Gerencia de Inteligencia de Gestión Humana #CD: 01/06/2020 #LUD: 10/08/2020
# Description: Script para el ranking de hojas de vida , se encarga de obtener los vectores del texto de las hojas de vida 
#              y delas descripciones de cargo y calcular las distancias que determinan el orden de similaridad
#              incluye extracción de texto mediante OCR cuando es requerido, se toma como base las siguientes fuentes: 
#              module_url = 'https://tfhub.dev/google/universal-sentence-encoder-multilingual/3' #@param ['https://tfhub.dev/google/universal-sentence-encoder-multilingual/3', 'https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3'] 
#Documentacion de la libreria SimpleNeighbors :  https://simpleneighbors.readthedocs.io/en/latest/index.html 
#                                                https://pypi.org/project/annoy/
#
# Run: python muse_ranking.py arg1 arg2
#
# v0.1
# Modification:
# Description:
#-------------------------------------------------------------------------
"""

import numpy as np
import os
import pandas as pd
import tensorflow.compat.v2 as tf
import tensorflow_hub as hub
from tensorflow_text import SentencepieceTokenizer
import sklearn.metrics.pairwise
from simpleneighbors import SimpleNeighbors
from tqdm import tqdm
from tqdm import trange


vModuleUrl = '/home/john/muse/model/muse_simpler'
vModel = hub.load(vModuleUrl)

def embed_text(input):
    return vModel(input)


vLanguageCode='es'
vLanguageName = 'Spanish'

vLanguageToSentences = {}
vLanguageToNewsPath = {}
language_to_ids={}
language_to_names={}
vBatchSize = 64 
vNumIndexTrees = 40
vNumResults = 200
vCorpusPath ='/home/john/muse/datos/corpus.txt'

def construct_embeddings_index(idPosicion, vRutaHv):
    df = pd.read_excel(vRutaHv, sheet_name='cantidatos')
    df = df.loc[df['ID de solicitud de puesto'] == idPosicion]
    df['texto_hv'].replace('', np.nan, inplace=True)
    df.dropna(subset=['texto_hv'], inplace=True)
    df.reset_index(drop=True, inplace=True)

    vLanguageToSentences[language_code] = df['texto_hv']#[:19]#pd.read_csv(news_path, sep='\n', header=None)[0]
    vLanguageToSentences['nombre'] = df['NombreCandidato']
    vLanguageToSentences['id'] = df['ID de candidato']
    vLanguageToNewsPath[vLanguageCode] = vCorpusPath
    print('{:,} {} sentences'.format(len(vLanguageToSentences[vLanguageCode]), vLanguageName))


    vLanguageToEmbeddings = {}

    print('\nComputing {} embeddings'.format(vLanguageName))
    with tqdm(total=len(vLanguageToSentences[vLanguageCode])) as pbar:
        for batch in pd.read_csv(vLanguageToNewsPath[vLanguageCode], sep='\n',header=None, chunksize=vBatchSize):
            vLanguageToEmbeddings.setdefault(vLanguageCode, []).extend(embed_text(batch[0]))
            pbar.update(len(batch))


    vLanguageNameToIndex = {}
    vEmbeddingDimensions = len(list(vLanguageToEmbeddings.values())[0][0])


    print('\nAdding {} embeddings to index'.format(vLanguageName))
    vIndex = SimpleNeighbors(vEmbeddingDimensions, metric='dot')

    for i in trange(len(vLanguageToSentences[vLanguageCode])):
        vIndex.add_one(vLanguageToSentences[vLanguageCode][i], vLanguageToEmbeddings[vLanguageCode][i])

    print('Building {} index with {} trees...'.format(vLanguageName, vNumIndexTrees))
    vIndex.build(n=vNumIndexTrees)
    vLanguageNameToIndex[vLanguageName] = vIndex




def get_muse_ranking(idPosicion,perfilCandidato,vRutaHv):
    #Ejemplo vRutaHv = '/home/john/muse/datos/hojas_vida.xlsx'
    construct_embeddings_index(idPosicion,vRutaHv)
    vQueryEmbedding = embed_text(perfilCandidato)
    vQueryEmbeddingTranspose =tf.transpose(vQueryEmbedding)
    vSearchResults = language_name_to_index[vLanguageName].nearest_dist( vQueryEmbeddingTranspose, n=vNumResults)
    print('{} sentences similar to: "{}"\n'.format(vLanguageName, perfilCandidato))

    vidCandidato=[]
    vRanking=[]
    vDistancia=[]
    for i, sr in enumerate(vSearchResults['sentence']):
        vidCandidato.append(sr.split('.')[0])
        vRanking.append(i+1)
    for i, sr in enumerate(search_results['index_dist'][1]): 
        vDistancia.append(sr)

    vData = {'ID': vidCandidato, 'RANK': vRanking  ,'DISTANCIA':vDistancia}
    vDf = pd.DataFrame(vData, columns = ['ID', 'RANK','DISTANCIA'])
    vDf.to_excel("/home/john/muse/results/ranking_{}.xlsx".format(idPosicion), sheet_name='ranking')