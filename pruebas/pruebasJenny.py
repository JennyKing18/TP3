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
import random
import names
from datetime import *
from dateutil.relativedelta import relativedelta
#variables globales
website= 'https://practicatest.cr/blog/licencias/tipos-licencia-conducir-costa-rica'
resultado= requests.get(website) 
contenido= resultado.text
soup=BeautifulSoup(contenido,'html.parser')
tipoLicencia= soup.find_all('h2')
patronST=r'Licencia [A-Z]\d+'
subtipo=soup.find_all('h3',string=re.compile(patronST))
#definicion de funciones
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

def obtenerSubtipos():
    tree = ET.parse('informacion.xml')
    root = tree.getroot()
    lista = []
    for elemento in root.iter('SubTipo'):
        subtipo = elemento.text.strip()
        lista.append(subtipo)
    return lista

# CREAR LICENCIAS
def generarCedula(): 
    cedula=''
    cedula+=str(random.randint(1, 9))
    cedula += "-" 
    for i in range(4):
        cedula += str(random.randint(0, 9)) 
    cedula += "-"
    for i in range(4):
        cedula += str(random.randint(0, 9))
    return cedula

def generarNombre():
    nombre= names.get_first_name() 
    apellido1= names.get_last_name()
    apellido2= names.get_last_name()
    nomCompleto=[nombre,apellido1,apellido2]
    return tuple(nomCompleto)

def generarFN(): #FechaNacimiento
    inicioFN,finalFN = datetime(1970, 1, 1) , datetime.now()
    rangoDia= finalFN-inicioFN
    dia=random.randint(1,rangoDia.days)
    fecha = inicioFN + timedelta(days=dia)
    formato=fecha.strftime("%d-%m-%Y")
    return formato
#fecha vencimiento
def asignarLicencia():
    listaTipos= obtenerSubtipos()
    tope=len(listaTipos)
    num=random.randint(0,tope-1)
    licencia=listaTipos[num]
    return licencia

def limpiarTexto(texto):
    texto = re.sub(r'[*\n]', '', texto)
    texto = texto.replace('\u200b', '')
    return texto

def generarSedes():
    sede={}
    ubic=[]
    archivo=open(r'sedes.txt',encoding="utf8").readlines()
    for linea in archivo:
        if re.match("^[*]{1}\w+",linea):
            ubic=[]
            llave=limpiarTexto(linea)
            sede[llave] =''
        else:
            ubic.append(limpiarTexto(linea))
            sede[llave]=ubic
    return sede

def asignarSede(cedula):
    codificacion={1:'San jose',2:'Alajuela',3:'Cartago',4:'Heredia',5:'Guanacaste',6:'Puntarenas',7:'Limon'}
    cedula=int(cedula[0])
    dicc=generarSedes()
    #sedes=list(dicc.keys())
    if cedula == 1:
        ubic=list(dicc[codificacion[1]])
        return len(ubic)
    elif cedula ==2:
        ubic=list(dicc[codificacion[2]])
        return len(ubic)
    elif cedula==3:
        ubic=list(dicc[codificacion[3]])
        return len(ubic)
    elif cedula==4:
        ubic=list(dicc[codificacion[4]])
        return len(ubic)
    elif cedula ==5:
        ubic=list(dicc[codificacion[5]])
        return len(ubic)
    elif cedula==6:
        ubic=list(dicc[codificacion[6]])
        return len(ubic)
    elif cedula==7:
        ubic=list(dicc[codificacion[7]])
        return len(ubic)
    else:
        ubic=list(dicc[codificacion[1]])
        return len(ubic)

def generarCorreo(nombreCompleto):
    '''
    F: Generar un correo
    E: nombreCompleto(tupla)
    S: correo(str)
    '''
    correo=''
    correo+=nombreCompleto[1]+nombreCompleto[1][0:2]+nombreCompleto[2][0:2]+'@gmail.com'
    return correo

def calcularEdad(fechaNac):
    fechaNac=datetime.strptime(fechaNac,"%d-%m-%Y")
    hoy = datetime.today()
    edad = hoy.year - fechaNac.year - ((hoy.month, hoy.day) < (fechaNac.month, fechaNac.day))
    if int(edad) >= 18:
        return edad 
    return False

def calcularFechaVN(fechaNac):
    hoy = date.today()
    edad = calcularEdad(fechaNac)
    if edad >= 18 and edad <= 25:
        vencimiento = hoy + relativedelta(years=3)
        return vencimiento.strftime("%d-%m-%Y")
    vencimiento = hoy + relativedelta(years=5)
    return vencimiento.strftime("%d-%m-%Y")

def crearLicencias(num):
    BD=[]
    i=0
    while i < num:
        persona=[]
        cedula= generarCedula()
        nombre=generarNombre()#hacer join para sacar de la tupla
        fechaNac=generarFN()
        fechaExpe= date.today().strftime("%d-%m-%Y")
        correo=generarCorreo(nombre)
        sangre=random.choice(['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB'])
        if calcularEdad(fechaNac)!= False:
            tipoLicencia=asignarLicencia() 
            fechaVenc= calcularFechaVN(fechaNac)
            donador=random.choice([True, False])
            sede= asignarSede(cedula)
            puntaje= 12-random.randint(0,12)
        else:
            tipoLicencia='-' #si no es mayor de edad no tiene nada de esto
            fechaVenc= '-'
            donador='-'
            sede= '-'
            puntaje='-'
        persona.extend([cedula,nombre,fechaNac,fechaExpe,correo,sangre,tipoLicencia,fechaVenc,donador,sede,puntaje])
        BD.append(persona)
        i+=1
    return BD

# fecha=generarFN()
# print(date.today().strftime("%d-%m-%Y"))
# print(calcularEdad(fecha))
# print(calcularFechaVN(fecha))

print(crearLicencias(3))