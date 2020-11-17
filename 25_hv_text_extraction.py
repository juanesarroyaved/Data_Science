"""
#-------------------------------------------------------------------------
# Author: John Alexander Garzón Vásquez , Gerencia de Inteligencia de Gestión Humana #CD: 01/06/2020 #LUD: 10/08/2020
# Description: Script para el preproceso de hojas de vida , se encarga de obtener el texto liquido de hojas de vida en formato pdf
#              incluye extracción de texto mediante OCR cuando es requerido, se toma como base las siguientes fuentes: 
#              https://stackoverflow.com/questions/34837707/how-to-extract-text-from-a-pdf-file
#              http://search.maven.org/remotecontent?filepath=org/apache/tika/tika-server/1.24/tika-server-1.24.jar
#              https://repo1.maven.org/maven2/org/apache/tika/tika-server/1.24/tika-server-1.24.jar.md5   
#
# Run: python hv_text_extraction.py arg1 arg2
#
# v0.1
# Modification:
# Description:
#-------------------------------------------------------------------------
"""

  

import os
import re
import subprocess
import textract
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

# Se configura la variable de entorno del sistema para correr TIKA OCR de forma local
os.environ['TIKA_SERVER_JAR'] ="file:/home/john/muse/libs/tika-server-1.24.jar"
from tika import parser
# Se configura el encabezado para procesar las imagenes de los pdf con TIKA OCR
vTikaHeaders = {'X-Tika-PDFextractInlineImages': 'true',}
vPdfCounter=0
vPdfImageCounter=0
vString=""

def text_filter(text):
    vFilteredText=text.rstrip()
    vFilteredText=vFilteredText.replace('\r', '')
    vFilteredText=vFilteredText.replace('\n', '')
    vFilteredText=vFilteredText.replace('\r\n', '')
    #delete spaces
    #vFilteredText= ''.join(e for e in vFilteredText if e.isalnum())
    #accents =\u00C0-\u00FF
    vFilteredText= re.sub('[^A-Za-z0-9\u00C0-\u00FF\s+#@^.]+', '', vFilteredText.strip())  
    return vFilteredText

def write_file(pathToTxt,text):
    with open(pathToTxt, 'w') as txtFile:
        print("Writing contents to " + pathToTxt)
        txtFile.write(text)


def write_text_line(pathToTxt, text):
    global vString
    vLocalString=""
    for vLine in text.splitlines():
        if vLine in ['\n','\r','\r\n','',' ','.']:
            #print('empty line')
            pass
        else: 
            vLine=text_filter(vLine)
            vLocalString=vLocalString+vLine+ ' '
            
    vString = vString+vLocalString+'\n'
        
    
def write_text(pathToTxt, text):
    vString=""
    for line in text.splitlines():
        if vLine in ['\n','\r','\r\n','',' ','.']:
            #print('empty line')
            pass
        else: 
            vLine=text_filter(vLine)
            vString=vString+vLine+'\n'
        
    write_file(pathToTxt,string)
    
    
def text_to_xlsx(text):
    vString=""
    for vLine in text.splitlines():
        if vLine in ['\n','\r','\r\n','',' ','.']:
            #print('empty line')
            pass
        else: 
            vLine=text_filter(vLine)
            vString=vString+vLine+ '\n' 
    return vString         


def extract_text_from_pdf(nombreArchivo): 
    global vPdfCounter , vPdfImageCounter
    vHvText=''
    print("Processing " + nombreArchivo)
    try:
        vPdfContents = parser.from_file(nombreArchivo)
        #for process images in pdf with Tika OCR
        #vPdfContents = parser.from_file(nombreArchivo,headers=headers) 
        #print(vPdfContents.keys())
        #print(vPdfContents['metadata'])
        if "content" in vPdfContents and vPdfContents['content'] is None:
            print('pdf is not content')
        else: 
            #vFilteredText=text_filter(vPdfContents['content'])
            vFilteredText=vPdfContents['content']
            vFilteredTextLen=len(vFilteredText)
            print('Text length = {}'.format(vFilteredTextLen))
            if vFilteredTextLen >300:
                #write_text(path_to_txt, vFilteredTextLen)
                vHvText=vFilteredText
                vPdfCounter +=1
                print('processed {} pdfs !'.format(vPdfCounter))
            else:
                print('No minimum string len, process OCR')
                vText = textract.process(nombreArchivo, method='tesseract', language='spa', encoding='utf_8')
                #write_text(path_to_txt,Text.decode('utf-8')) 
                vHvText=vText.decode('utf-8')
                vPdfImageCounter+=1
                print('processed {} pdf images !'.format(vPdfImageCounter)) 
                
    except:
          print("An exception occurred")  
          vHvText=''
        
    return vHvText
    
    
def extract_text_from_pdfs_recursively(vDir):
    global vPdfCounter , vPdfImageCounter
    for vRoot, vDirs, vFiles in os.walk(vDir):
        for vFile in vFiles:
            vPathToPdf = os.path.join(vRoot, vFile)
            [vStem, vExt] = os.path.splitext(vPathToPdf)
            if vExt == '.pdf':
                print("Processing " + vPathToPdf)
                vPdfContents = parser.from_file(vPathToPdf)
                #vPdfContents = parser.from_file(path_to_pdf,headers=headers) # for process images in pdf with Tika OCR
                #print(vPdfContents.keys())
                #print(vPdfContents['metadata'])
                vPathToTxt = vStem + '.txt'
                if "content" in vPdfContents and vPdfContents['content'] is None:
                    print('pdf is not content')
                else: 
                    #vFilteredText=text_filter(vPdfContents['content'])
                    vFilteredText=vPdfContents['content']
                    vFilteredTextLen=len(vFilteredText)
                    print('Text length = {}'.format(vFilteredTextLen))
                    if vFilteredTextLen >300:
                        #write_text(vPathToTxt,vFilteredText)
                        write_text_line(vPathToTxt, vFilteredText)
                        vPdfCounter+=1
                        print('processed {} pdfs !'.format(vPdfCounter))
                    else:
                        print('No minimum string len, process OCR')
                        vText = textract.process(vPathToPdf, method='tesseract', language='spa', encoding='utf_8')
                        #write_text(vPathToTxt,vText.decode('utf-8')) 
                        write_text_line(vPathToTxt, vText.decode('utf-8'))
                        vPdfImageCounter+=1
                        print('processed {} pdf images !'.format(vPdfImageCounter))

def get_corpus(hvDirPath,corpusOutPath):
    extract_text_from_pdfs_recursively(hvDirPath)
    write_file(corpusOutPath,vString)
    
                        
def extract_liquid_text(filePath,sheetName):
    # filePath example = '/home/john/muse/candidatos.xlsx'
    vDf = pd.read_excel(filePath, sheet_name=sheetName)
    vDf['texto_hv']=''
    for index, row in vDf.iterrows():
        print(index)
        vNombreArchivo=row['archivo']
        vText=extract_text_from_pdf('/home/john/muse/datos/hojasvida/'+vNombreArchivo)
        vResult=text_to_xlsx(vText)
        #print(vResult)
        vDf.loc[index, 'texto_hv']=vResult
 
    vDf.to_excel("/home/john/muse/datos/hojasvida/hojas_vida.xlsx", sheet_name='cantidatos')