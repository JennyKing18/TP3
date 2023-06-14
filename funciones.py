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
from clases import *
from clases import Registro
import aspose.pdf as ap
from fpdf import FPDF

#variables globales
website= 'https://practicatest.cr/blog/licencias/tipos-licencia-conducir-costa-rica'
resultado= requests.get(website) 
contenido= resultado.text
soup=BeautifulSoup(contenido,'html.parser')
tipoLicencia= soup.find_all('h2')
patronST=r'Licencia [A-Z]\d+'
subtipo=soup.find_all('h3',string=re.compile(patronST))

# >>>> Instanciar clase
conductores= Registro()

# Definicion de Funciones
###############
# 1 Crear XML #
###############
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
    listaLimpia=[]
    for licencia in lista:
        elemento = re.sub(r'Licencia\s*|\(.*?\)', '', licencia).strip()
        listaLimpia.append(elemento)
    return listaLimpia

# funciones de >>> CREAR LICENCIAS
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
    nombreCompleto=[]
    nombreCompleto.append( names.get_first_name() )
    nombreCompleto.append( names.get_last_name() )
    nombreCompleto.append( names.get_last_name() )
    nombreCompleto=tuple(nombreCompleto)
    return nombreCompleto

def generarFechaNac(): #FechaNacimiento
    inicioFN,finalFN = datetime(1970, 1, 1) , datetime.now()
    rangoDia= finalFN-inicioFN
    dia=random.randint(1,rangoDia.days)
    fecha = inicioFN + timedelta(days=dia)
    formato=fecha.strftime("%d-%m-%Y")
    return formato

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
    if cedula == 1:
        ubic=list(dicc[codificacion[1]])
        sede=ubic[random.randint(0,len(ubic)-1)]
        return sede #anteriormente no tenia sede return len(ubic)
    elif cedula ==2:
        ubic=list(dicc[codificacion[2]])
        sede=ubic[random.randint(0,len(ubic)-1)]
        return sede
    elif cedula==3:
        ubic=list(dicc[codificacion[3]])
        sede=ubic[random.randint(0,len(ubic)-1)]
        return sede
    elif cedula==4:
        ubic=list(dicc[codificacion[4]])
        return len(ubic)
    elif cedula ==5:
        ubic=list(dicc[codificacion[5]])
        sede=ubic[random.randint(0,len(ubic)-1)]
        return sede
    elif cedula==6:
        ubic=list(dicc[codificacion[6]])
        sede=ubic[random.randint(0,len(ubic)-1)]
        return sede
    elif cedula==7:
        ubic=list(dicc[codificacion[7]])
        sede=ubic[random.randint(0,len(ubic)-1)]
        return sede
    else:
        ubic=list(dicc[codificacion[1]])
        sede=ubic[random.randint(0,len(ubic)-1)]
        return sede

def generarCorreo(nombreCompleto):
    '''
    F: Generar un correo
    E: nombreCompleto(tupla)
    S: correo(str)
    '''
    correo=''
    print(nombreCompleto)
    correo+=nombreCompleto[1]+nombreCompleto[2][0]+nombreCompleto[0][0]+'@gmail.com'
    return correo

def calcularEdad(fechaNac):
    fechaNac=datetime.strptime(fechaNac,"%d-%m-%Y")
    hoy = datetime.today()
    edad = hoy.year - fechaNac.year - ((hoy.month, hoy.day) < (fechaNac.month, fechaNac.day))
    if int(edad) >= 18:
        return edad 
    return False

def calcularFechaVenc(fechaNac):
    hoy = date.today()
    edad = calcularEdad(fechaNac)
    if edad >= 18 and edad <= 25:
        vencimiento = hoy + relativedelta(years=3)
        return vencimiento.strftime("%d-%m-%Y")
    vencimiento = hoy + relativedelta(years=5)
    return vencimiento.strftime("%d-%m-%Y")
#####################
# 2 Crear licencias #
#####################
def crearLicencias(num):
    i=0
    while i < num: 
        cedula= generarCedula()
        conductores.asignarCedula(cedula)
        nombre=generarNombre()
        #nombre=' '.join(nombre)
        conductores.asignarNombre(' '.join(nombre))
        fechaNac=generarFechaNac()
        conductores.asignarFechaNac(fechaNac)
        fechaExpe= date.today().strftime("%d-%m-%Y")
        conductores.asignarFechaExp(fechaExpe)
        correo=generarCorreo(nombre)
        conductores.asignarCorreo(correo)
        sangre=random.choice(['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB'])
        conductores.asignarSangre(sangre)
        if calcularEdad(fechaNac)!= False:
            tipoLicencia=asignarLicencia() 
            conductores.asignarTipoLicencia(tipoLicencia)
            fechaVenc= calcularFechaVenc(fechaNac)
            conductores.asignarFechaVenc(fechaVenc)
            donador=random.choice([True, False])
            conductores.asignarDonador(donador)
            sede= asignarSede(cedula)
            conductores.asignarSede(sede)
            puntaje= 12-random.randint(0,12)
            conductores.asignarPuntaje(puntaje)
        else:
            tipoLicencia='-' #si no es mayor de edad no tiene nada de esto
            conductores.asignarTipoLicencia(tipoLicencia)
            fechaVenc= '-'
            conductores.asignarFechaVenc(fechaVenc)
            donador='-'
            conductores.asignarDonador(donador)
            sede= '-'
            conductores.asignarSede(sede)
            puntaje='-'
            conductores.asignarPuntaje(puntaje)
        registro.append(conductores)
        print([cedula,nombre],'\n')
        grabaBinario('BaseDatos',conductores)
        i+=1
    #mostrar lista
    lista = lee('BaseDatos')
    for i in range(len(lista)):
        print(i+1,')',lista[i].indicarDatos())
        print('='.center(100,'='))
    return ''

######################
# 3 Renovar Licencia #
######################

#################
# 4 Generar PDF #
#################
def validarCedula(cedula):
    if re.match('^[1-9]{1}\d{8}$',cedula):
        print('Cedula valida!')
        return cedula
    else:
        print('Cedula cumple con el formato 0-0000-0000.')

def obtenerDatos(cedula):
    lista=lee('BaseDatos')
    for i in range(len(lista)):
        if cedula == lista[i].mostrarCedula():
            fechaExp= lista[i].mostrarFechaExp()
            fechaNac= lista[i].mostrarFechaNac()
            fechaVenc= lista[i].mostrarFechaVenc()
            tipo= lista[i].mostrarTipoLicencia()
            donador= lista[i].mostrarDonador()
            sangre= lista[i].mostrarSangre()
            nombre= lista[i].mostrarNombre()
            sede=lista[i].mostrarSede()
            return generarPDF(cedula,fechaExp,fechaNac,fechaVenc,tipo,donador,sangre,nombre,sede)
    else:
        print('No se encontro la cedula que busca')

def generarPDF(cedula,fechaExp,fechaNac,fechaVenc,tipo,donador,sangre,nombre,sede):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_text_color(12, 182, 242)  
    pdf.set_font('helvetica', 'B', 12)  
    pdf.multi_cell(200, 10, txt='REPUBLICA DE COSTA RICA')
    pdf.ln(1)

    pdf.set_text_color(242, 46, 46)  #rojo
    pdf.set_font('helvetica','B', 10)  
    pdf.cell(200, 10, txt='Licencia de conducir')
    pdf.ln(6)

    pdf.set_text_color(0, 0, 0)  
    pdf.set_font('helvetica','B', 10)
    pdf.write(10, 'N°: ')
    pdf.set_text_color(242, 46, 46) 
    pdf.cell(200,10,f'CI-{cedula}')
    pdf.ln(6)

    pdf.set_text_color(0, 0, 0)  
    pdf.set_font('helvetica','B', 10)
    pdf.write(10, 'Expedición: ')
    pdf.set_font('helvetica','', 10)
    pdf.cell(200,10,f'{fechaExp}')
    pdf.ln(6)

    pdf.set_text_color(0, 0, 0)  
    pdf.set_font('helvetica','B', 10)
    pdf.write(10, 'Nacimiento: ')
    pdf.set_font('helvetica','', 10)
    pdf.cell(200,10,f'{fechaNac}')
    pdf.ln(6)

    pdf.set_text_color(0, 0, 0)  
    pdf.set_font('helvetica','B', 10)
    pdf.write(10, 'Vencimiento: ')
    pdf.set_font('helvetica','', 10)
    pdf.set_text_color(242, 46, 46)
    pdf.cell(200,10,f'{fechaVenc}')
    pdf.ln(6)
    
    #pdf.set_text_color(242, 46, 46)
    pdf.set_font('helvetica','B', 10)
    pdf.write( 10, 'Tipo: ')
    pdf.set_font('helvetica','B', 13)
    pdf.cell(200,10,f'{tipo}')
    pdf.ln(6)

    pdf.set_text_color(242, 46, 46)
    pdf.set_font('helvetica','B', 10)
    pdf.write(10,'Donador: ')
    pdf.set_font('helvetica','', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200,10,f'{donador}')
    pdf.ln(6)

    pdf.write(10, 'T.S. ')
    pdf.set_text_color(242, 46, 46)
    pdf.cell(200,10,f'{sangre}')
    pdf.ln(6)

    pdf.set_text_color(0, 0, 0)
    pdf.set_font('helvetica','B', 20)
    pdf.cell(200, 10, nombre)
    pdf.ln(6)

    pdf.set_font('helvetica','', 8)
    pdf.cell(200, 10, f'{date.today().strftime("%d-%m-%Y")} {datetime.now().strftime("%H:%M")} {sede}')

    pdf.output(f'Licencia-{cedula}.pdf')   
    return ''

####################
# 5 Reportes Excel #
####################

###############
# 6 Acerca de #
###############

# 7 Salir

# fecha=generarFechaNac()
# print(date.today().strftime("%d-%m-%Y"))
# print(calcularEdad(fecha))
# print(calcularFechaVenc(fecha))

print(crearLicencias(2))
#print(obtenerDatos('4-5092-5826'))
#print(obtenerSubtipos())