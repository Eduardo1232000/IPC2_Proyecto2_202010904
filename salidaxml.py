from typing import Text
from listas import *
import xml.etree.ElementTree as ET
import os
class salida:
    def salidaxml(self,listado,no_lineas,componente,linea,nombresimulacion,segundos):
        inicio=0
        contador=0
        root = ET.Element("SalidaSimulacion")
        ET.SubElement(root, "Nombre").text = str(nombresimulacion)
        listadoproductos= ET.SubElement(root, "ListadoProductos")

        for i in componente.recorrer():
            inicio+=1
            contadorl=1
            contadorp=1
            inicioactual=0
            
            
            producto=ET.SubElement(listadoproductos, "Producto")
            ET.SubElement(producto, "Nombre").text= str(i)
            contador=0
            for c in segundos.recorrer():
                print(c)
                if contador==inicio:
                    ET.SubElement(producto, "TiempoTotal").text= str(c)                       #MODIFICAR TIEMPO
                    contador+=1
                else:
                    contador+=1
            elaboracion=  ET.SubElement(producto, "ElaboracionOptima")

            for a in linea.recorrer():
                if a == "inicio":
                    #print()
                    seg=1
                    inicioactual+=1
                    contadorl+=1
                    continue
                    
                if inicio==inicioactual:
                    for b in listado.recorrer():
                        if int(contadorl) == int(contadorp):
                            tiempo=  ET.SubElement(elaboracion, "Tiempo", NoSegundo=str(seg))         #MDOFICAR TIEMPO

                            ET.SubElement(tiempo, "LineaEnsamblaje", NoLinea=str(a)).text=str(b) 
                            #print (b)
                            seg+=1
                            contadorp+=1
                            break
                        else:
                            contadorp+=1
                            continue
                else:
                    contadorl+=1
                    continue
                contadorp=1
                contadorl+=1
            
        tree = ET.ElementTree(root)
        tree.write("Salida.xml")
        print("Archivo xml generado con exito")

