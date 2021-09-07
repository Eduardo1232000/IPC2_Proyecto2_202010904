from tkinter import *
from tkinter.filedialog import askopenfilename

def abrir():
    Tk().withdraw()
    ruta = askopenfilename()                                                     #el nombre de la ruta
    archivo = open(ruta, 'r+')                                                   #abre el archivo en la ruta especificada
    print("El archivo se cargo correctamente")                                   #RUTA (opcional) imprime ruta
    datos= archivo.read() 
    archivo.close
    return datos