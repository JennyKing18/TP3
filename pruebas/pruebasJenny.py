###########################################################
#Elaborado por Jenny King Josue Salazar
#Fecha de creacion 02/06/23 10:30am
#Ultima modificacion 02/06/23 10:30am
#version 3.10.6
###########################################################
#importacion de librerias
from bs4 import BeautifulSoup
import requests
import re
#definicion de funciones
website= 'https://practicatest.cr/blog/licencias/tipos-licencia-conducir-costa-rica'
resultado= requests.get(website)
contenido= resultado.text

soup=BeautifulSoup(contenido,'html.parser')
tipoLicencia= soup.find_all('h2')

print(type(tipoLicencia))
patronST=r'Licencia [A-Z]\d+'
subtipo=soup.find_all('h3',string=re.compile(patronST))


for st in subtipo:
    comentario = st.find_next_sibling('p')
    requisitos_header = comentario.find_next_sibling('h4')
    requisitos = requisitos_header.find_next_sibling('ul').find_all('li')
    
    print(st.text.strip())
    print(comentario.text.strip())
    print('Requisitos:')
    for requisito in requisitos:
        print('- ' + requisito.text.strip())
    
    print('-' * 30)

