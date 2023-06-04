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
import xml.etree.cElementTree as ET 
from archivos import *

#definicion de funciones
website= 'https://practicatest.cr/blog/licencias/tipos-licencia-conducir-costa-rica'
resultado= requests.get(website)
contenido= resultado.text

soup=BeautifulSoup(contenido,'html.parser')
tipoLicencia= soup.find_all('h2')

patronST=r'Licencia [A-Z]\d+'
subtipo=soup.find_all('h3',string=re.compile(patronST))

# XML
raiz=ET.Element('Tipos de Licencias')
#

for tipo in tipoLicencia:
    # consigue el titulo 
    titulo = tipo.text.strip()
    subElemento=ET.SubElement(raiz, titulo)
    print(titulo)
    
    ListaSubtipo = []
    listaComentarios = []
    listaReque = []

    # Encuentra todos los datos dentro del 'h2' tag
    next_sibling = tipo.next_sibling
    while next_sibling and next_sibling.name != 'h2':
        if next_sibling.name == 'h3':
            # extrae subtipo,comentario,requerimientos 
            subTipo = next_sibling.text.strip()
            ListaSubtipo.append(subTipo)
            comentario = next_sibling.find_next_sibling('p')
            comentario=comentario.text.strip()
            listaComentarios.append(comentario)

            subTipos= ET.SubElement(subElemento,subTipo)
            subTipos.text=comentario

            if re.findall(r'Licencia D\d+', subTipo):
                listaReque = [
                    'Cédula o documento de identificación.',
                    'Dictamen médico digital para licencia.',
                    'Aprobar el curso teórico básico para licencia.'
                ]
                listaReque = [listaReque] * len(ListaSubtipo)
                listaReque.append(requerimientos)
                subTipos.text=listaReque
            else:
                requerimientos = next_sibling.find_next_sibling('ul')
                requerimientos=requerimientos.text.strip()
                listaReque.append(requerimientos)
                subTipos.text=listaReque
        
        next_sibling = next_sibling.next_sibling
    tree=ET.ElementTree(raiz)
grabar('informacion.html',tree)
print(raiz)
