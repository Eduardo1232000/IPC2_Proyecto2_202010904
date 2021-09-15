from tkinter import *
from tkinter import messagebox as MessageBox
from enum import auto
from abrir_archivo import*
from analizar_archivo import *
from listas import *
import xml.etree.ElementTree as ET
import os
from threading import *
import time




class interfaz:
    def __init__(self, ventana):
        #inicializar la ventana
        self.ventana=ventana
        self.ventana.title("Simulacion")    #Titulo programa
        self.ventana.geometry("750x500")  #tamaño de pantalla
        self.ventana.configure(bg='skyblue')#color de fondo ventana
        self.permitir=0
        #DATOS DEL DOCUMENTO ANALIZADO
        self.contador=0
        self.numero_lineas_produccion = 0 #NUMERO DE LINEAS DE PRODUCCION
        self.lineas_de_produccion = Lista()   #ESTRUCTURA: NUMERO, CANTIDAD COMPONENTES, TIEMPO ENSAMBLAJE
        self.listado_producto = Lista()       #ESTRUCTURA NOMBRE, ELABORACION



        #BOTONES
        self.botonSaludo = Button(ventana, text="Cargar Archivo",command=self.carga)
        self.botonSaludo.place(x=10, y=10,width=100,height=30)

        self.botonSaludo = Button(ventana, text="Cargar Archivo",command=self.carga)
        self.botonSaludo.place(x=10, y=10,width=100,height=30)

        self.botonventana = Button(ventana, text="Analizar", command=self.analizar)
        self.botonventana.place(x=210, y=10,width=100,height=30)

        self.botonreportes = Button(ventana, text="Reportes", command=self.reportes)
        self.botonreportes.place(x=310, y=10,width=100,height=30)

        self.botonreportes = Button(ventana, text="hilos", command = self.threading)
        self.botonreportes.place(x=310, y=210,width=100,height=30)

        self.botonCerrar = Button(ventana, text="Cerrar", command=ventana.quit)
        self.botonCerrar.place(x=610, y=10,width=100,height=30)


    #FUNCION DEL BOTON CARGAR
    def carga(self):
        print("hola")
        

    #FUNCION DEL BOTON ANALIZAR
    def analizar(self):
        self.archivo = "D:/Escritorio/Proyectos Python/IPC2/proyecto 2/Archivos de prueba - Proyecto 2-20210914T193047Z-001/Archivos de prueba - Proyecto 2/maquina.xml"
        #print("analiza")
        self.doc_analizado=Cola()

        self.raiz = ET.parse(self.archivo)
        self.data = self.raiz.getroot()
        #print(self.data)
        while self.contador < len(self.data):

        #OBTIENE EL NUMERO DE LINEAS DE PRODUCCION------------------------------------------------------------------------------------
            if self.data[self.contador].tag=="CantidadLineasProduccion":
                self.numero_lineas_produccion = self.data[self.contador].text
                #print(self.lineas_produccion)          FUNCIONA
                self.contador+=1
                continue
        # 
        #ANALIZA LISTADO LINEAS DE PRODUCCION-----------------------------------------------------------------------------------------
            elif self.data[self.contador].tag == "ListadoLineasProduccion":
                self.listadolineasproduccion = self.data[self.contador]
                for i in self.listadolineasproduccion:
                    self.unionfrase=""
                    for j in i:
                        if j.tag =="Numero":
                            self.unionfrase+= j.text
                            self.unionfrase+=","
                            #print(self.unionfrase) IMPRIME EL NUMERO DE LINEA DE PRODUCCION
                        elif j.tag == "CantidadComponentes":
                            self.unionfrase+= j.text
                            self.unionfrase+=","
                        elif j.tag == "TiempoEnsamblaje":
                            self.unionfrase+= j.text
                    self.lineas_de_produccion.insertar(self.unionfrase)
                self.contador+=1
                continue
        #
        #ANALIZA LISTADO PRODUCTOS----------------------------------------------------------------------------------------------------
            elif self.data[self.contador].tag == "ListadoProductos":
                self.producto = self.data[self.contador]
                for i in self.producto:
                    self.unionfrase=""
                    for j in i:
                        if j.tag=="nombre":
                            self.unionfrase += j.text
                            self.unionfrase += ","
                        elif j.tag == "elaboracion":
                            self.unionfrase += j.text
                            self.unionfrase += ","
                    self.listado_producto.insertar(self.unionfrase)
        
                self.contador+=1
                continue
        #
            
            continue

                        
            




    #FUNCION DEL BOTON REPORTES

    def reportes(self):
        #print("reportes")
        print()
        print("------------------------Informacion de:Lineas de produccion-------------------------")
        for i in self.lineas_de_produccion.recorrer():
            print(i)
        print()
        print("------------------------Informacion de: Listado Productos-------------------------")
        for i in self.listado_producto.recorrer():
            print(i)
        
    
    def threading(self): 
        t1=Thread(target=self.work) 
        t1.start() 
  
    def work(self): 
        print("sleep time start") 
        for i in range(10): 
            print(i) 
            time.sleep(1) 
        print("sleep time stop") 

ventana_principal= Tk()
programa = interfaz(ventana_principal)
ventana_principal.mainloop()