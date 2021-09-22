import re
from listas import *

class expresion:
    def __init__(self):
        self.pasos= Cola()
        self.pasosporsegundo= Lista()
        self.instruccion_actual=""
        self.linea_actual=""
        self.componente_actual=""
        self.caracter=""
        self.contador=0
        self.segundo=1

    def analizar(self, entrada):
        contador=0
        while int(contador) < int(len(entrada)):
            print(contador)
            contador+=1
            
        
