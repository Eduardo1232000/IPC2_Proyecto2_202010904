import os
import sys
from listas import *
class grafica:
    def imagen(self,listado,numero):
        inicio=0
        posicioncomparar=1
        posicion=1
        dott = open("grafica.dot",'w')
        dott.write('digraph G {')
        for i in listado.recorrer():                          
            if str(i)=="inicio":
                inicio+=1
                continue 
            else:  
                if int(inicio)==int(numero):
                    dott.write(str(i)+"->")
                else:
                    continue
        dott.write("fin")
        dott.write('[constraint=false];}')
        dott.close()
        os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'
        os.system('dot -Tpng grafica.dot -o grafica.png')

                    
