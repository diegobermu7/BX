#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 20:58:09 2021

@author: diegoalejandrobermudezsierra
"""
import pandas as pd
import re
import string

#Importaamos la base de datos que descargamos con los tweets de brandwatch 
path="/Users/diegoalejandrobermudezsierra/OneDrive - Universidad de los Andes/BAROMETRO DE XENOFOBIA/XENOFOBIA/mentions_xenofobia.xlsx"
xenofobia=pd.read_excel(path)
del path

#Eliminamos las primeras filas del df que tienen información que no necesitamos
#Eliminamos la primera columna que es un conteo dado por brandwatch
xenofobia=xenofobia.iloc[7:len(xenofobia),1:]


#Tomamos la primera fila como nombre de las columnas
column_names=xenofobia.iloc[0,:].tolist()
#Cambiamos los espacios por _
column_names=[re.sub('\\s', '_', x) for x in column_names]
#Renombramos las columnas
xenofobia.columns=column_names
#Eliminamos la fila que tomamos como nombre de las columnas
xenofobia=xenofobia.iloc[1:,:]
#Hacemos un reset al index
xenofobia=xenofobia.reset_index(drop=True)
del column_names

#Tomamos solo la columna Full Text
tweets=pd.DataFrame(xenofobia.Full_Text)

#Limpiamos los tweets

#Eliminamos todos los @Usuario (i.e. @ClaudiaLopez)
tweets['Clean_Text']=tweets.Full_Text.replace('@\\w+', '', regex=True)
#Eliminamos todos los signos de puntuación
tweets['Clean_Text']=tweets.Clean_Text.replace(r'[^\w\s]+', '', regex=True)
#Remplazamos los acentos de las palabras y los emojis
tweets['Clean_Text']=tweets.Clean_Text.str.normalize('NFKD')\
        .str.encode('ascii', errors='ignore')\
        .str.decode('utf-8')
#Eliminamos los dobles espacios 
tweets['Clean_Text']=tweets.Clean_Text.replace('\s+', ' ', regex=True).str.strip()

#Exportamos la base limpia en formato txt
path="/Users/diegoalejandrobermudezsierra/OneDrive - Universidad de los Andes/BAROMETRO DE XENOFOBIA/XENOFOBIA/Xenofobia_Clean.txt"
tweets.Clean_Text.to_csv(path, header=None, index=None)

#Para efectos del ejercico de afinar la regla de Xenofobia dejamos los
#"Tweets unicos"
path="/Users/diegoalejandrobermudezsierra/OneDrive - Universidad de los Andes/BAROMETRO DE XENOFOBIA/XENOFOBIA/Xenofobia_Clean_Unicos.txt"
tweets_unicos=pd.DataFrame(tweets.Clean_Text.unique())
tweets_unicos.to_csv(path, header=None, index=None)

del path, tweets, tweets_unicos, xenofobia


