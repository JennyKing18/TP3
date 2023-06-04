import pickle

def graba(nomArchGrabar,lista):
    #Función que graba un archivo en una lista 
    try:
        f=open(nomArchGrabar,"wb")
        pickle.dump(lista,f)
        f.close()
    except TypeError:
        print('Error: Se esperaba un dato str y una lista/matriz/tupla/str')
    except:
        print('Error inesperado al guardar archivo:'+ nomArchGrabar)

def lee (nomArchLeer):
    #Función que lee un archivo con una lista de estudiantes
    lista=[]
    try:
        f=open(nomArchLeer,"rb")
        lista = pickle.load(f)
        f.close()
    except:
        print("Error al leer el archivo: ", nomArchLeer)
    return lista