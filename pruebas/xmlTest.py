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

def crearXML():
    raiz=ET.Element('TiposDeLicencias')
    for tipo in tipoLicencia:
        # consigue el titulo 
        titulo = tipo.text.strip()
        subElemento=ET.SubElement(raiz, 'Tipo')
        subElemento.text=titulo
        print(f'\033[1;30;44m {titulo} \033[0;0m')
        listaSubtipo,listaComentarios,listaReque= [],[],[]
        # Encuentra todos los datos dentro del 'h2' tag
        next_sibling = tipo.next_sibling
        while next_sibling and next_sibling.name != 'h2':
            if next_sibling.name == 'h3':
                # extrae subtipo,comentario,requerimientos 
                subTipo = next_sibling.text.strip()
                listaSubtipo.append(subTipo)
                comentario = next_sibling.find_next_sibling('p')
                comentario=comentario.text.strip()
                listaComentarios.append(comentario)
                subTipos= ET.SubElement(subElemento,'SubTipo')
                subTipos.text=subTipo
                child=ET.SubElement(subTipos,'info')
                child.text=comentario
                if re.findall(r'Licencia D\d+', subTipo):
                    listaReque = 'Cédula o documento de identificación.\nDictamen médico digital para licencia.\nAprobar el curso teórico básico para licencia.'
                    listaReque = [listaReque] * len(listaSubtipo)
                    child.text=str(listaReque)
                else:
                    requerimientos = next_sibling.find_next_sibling('ul')
                    requerimientos=requerimientos.text.strip()
                    listaReque.append(requerimientos)
                    child.text=str(listaReque)
            next_sibling = next_sibling.next_sibling
        for subTipo, comentario, requerimientos in zip(listaSubtipo, listaComentarios, listaReque):
            print('-'.center(100,'-'))
            print(subTipo+'\n'+comentario+'\n''\nRequerimientos:\n'+requerimientos+'\n')
        print('-'.center(100,'-'))
    tree=ET.ElementTree(raiz)
    tree.write(str('informacion.xml'), encoding="UTF-8")
    #hacer leible
    temp=BeautifulSoup(open('informacion.xml'),'xml')
    prettyTemp= temp.prettify()
    graba('informacion.xml',prettyTemp)
    return ''
print(crearXML())


'''
def definirSubtipos():
    tree=ET.parse('informacion.xml')
    root=tree.getroot()
    lista=[]
    subtipos=root.findall('Subtipo')
    for elemento in subtipos:
        texto = elemento.text.strip()
        print(texto)
        lista.append(texto)
    return lista
    '''