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

patronST=r'Licencia [A-Z]\d+'
subtipo=soup.find_all('h3',string=re.compile(patronST))

for element in tipoLicencia:
    # Retrieve the title
    title = element.text.strip()
    print(title)
    
    # Retrieve the subtitles, comments, and requirements
    subtitles = []
    comments = []
    requirements = []

    # Find the next siblings until the next 'h2' tag
    next_sibling = element.next_sibling
    while next_sibling and next_sibling.name != 'h2':
        if next_sibling.name == 'h3':
            # Retrieve subtitles
            subtitle = next_sibling.text.strip()
            subtitles.append(subtitle)
            comment = next_sibling.find_next_sibling('p')
            comment=comment.text.strip()
            comments.append(comment)
            #print('EEEE',subtitle)

            if re.findall(r'Licencia D\d+', subtitle):
                requirements = [
                    'Cédula o documento de identificación.',
                    'Dictamen médico digital para licencia.',
                    'Aprobar el curso teórico básico para licencia.'
                ]
                requirements = [requirements] * len(subtitles)
                requirements.append(requirement)
            else:
                requirement = next_sibling.find_next_sibling('ul')
                requirement=requirement.text.strip()
                requirements.append(requirement)
        
        next_sibling = next_sibling.next_sibling

    # Imprimir todo
    #requirements = [requirements] * len(subtitles)

    # Print the subtitles, comments, and requirements
    for subtitle, comment, requirement in zip(subtitles, comments, requirements):
        print(subtitle)
        print(comment)
        print(requirement)
       
        print()

    print('-'.center(100,'-'))  # Print an empty line between each type


# for st in subtipo:
#     comentario = st.find_next_sibling('p')
#     requisitos_header = comentario.find_next_sibling('h4')
#     requisitos = requisitos_header.find_next_sibling('ul').find_all('li')
    
#     print(st.text.strip())
#     print(comentario.text.strip())
#     print('Requisitos:')
#     for requisito in requisitos:
#         print('- ' + requisito.text.strip())
    
#     print('-' * 30)

