import pickle

def grabaN(nomArchGrabar,lista):
    #Función que graba un archivo en una lista 
    try:
        f=open(nomArchGrabar,"w")
        f.write(lista)
        f.close()
    except TypeError:
        print('Error: Se esperaba un dato str y una lista/matriz/tupla/str')
    except:
        print('Error inesperado al guardar archivo:'+ nomArchGrabar) 

def grabaBinario(nomArchGrabar,lista):
    #Función que graba un archivo en una lista 
    try:
        f=open(nomArchGrabar,"ab")
        pickle.dump(lista,f)
        f.close()
    except TypeError:
        print('Error: Se esperaba un dato str y una lista/matriz/tupla/str')
    except:
        print('Error inesperado al guardar archivo:'+ nomArchGrabar)

def lee (nomArchLeer):
    #Función que lee un archivo 
    try:
        f=open(nomArchLeer,"rb")
        objs = []
        while True:
            try:
                obj = pickle.load(f)
            except EOFError:
                break
            objs.append(obj) # esta mica es quien mete la mlista dentro de una lista
        return objs
    except FileNotFoundError:
        lista = []
    except:
        print("Error al leer el archivo: ", nomArchLeer)
        return False
    return lista