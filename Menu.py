from tkinter import *
from tkinter import messagebox as MessageBox
from enum import auto
from abrir_archivo import*
from listas import *
import xml.etree.ElementTree as ET
import os
from PIL import Image,ImageTk
from threading import *
import time
import re

from analizador import *
analizando = expresion()


class interfaz:
    def __init__(self, ventana):
        #inicializar la ventana
        self.ventana=ventana
        self.ventana.title("Simulacion")    #Titulo programa
        self.ventana.geometry("750x500")  #tamaño de pantalla
        self.ventana.configure(bg='skyblue')#color de fondo ventana
        self.permitir = 0

        #DATOS DEL DOCUMENTO ANALIZADO
        self.contador=0
        self.numero_lineas_produccion = 0 #NUMERO DE LINEAS DE PRODUCCION
        self.lineas_de_produccion = Lista()   #ESTRUCTURA: NUMERO, CANTIDAD COMPONENTES, TIEMPO ENSAMBLAJE
        self.listado_producto = Lista()       #ESTRUCTURA NOMBRE, ELABORACION
        self.listaconstruccion = Cola()
        self.nombresimulacion=""

        #LISTAS DE SEPARACION CON SPLIT
        self.listado_producto_nombres = Lista()
        self.listado_producto_pasos = Lista()


        #NECESARIO PARA ANALISIS
        self.pasos= Cola()
        self.componentepasos = Cola()
        self.pasosporsegundo= Lista()

        self.contadorcomas =0
        self.contadorcomponentepasos =0
        self.contadorinstruccionpasos = 0
        self.estado=0                       #En la expresion es para saber cuando agregar la instruccion a la cola
        self.instruccion_actual=""          #es para el analisis 
        self.instruccion=""                 # forma la instruccion para despues guardarla en la cola
        self.linea_actual=""                #es para el analisis y saber la linea actual
        self.componente_actual=""           #es para guiarse y realizar acciones
        self.caracter=""                    
        self.contador=0                     
        self.segundo=1                      #para saber en que segundo va y guardarlo en la cola
        self.producto_proceso =""           #Para saber en el analisis que producto esta construyendo
        self.numeroanalisis = 0             #Para la expresion, y asi saber si la instruccion ya tiene sus 2 numeros
        



        #BOTONES
        self.botonSaludo = Button(ventana, text="Cargar Archivo",command=self.carga)
        self.botonSaludo.place(x=10, y=10,width=100,height=30)

        self.botonSaludo = Button(ventana, text="Cargar Simulacion",command=self.carga_simulacion)
        self.botonSaludo.place(x=110, y=10,width=100,height=30)

        self.botonventana = Button(ventana, text="Analizar", command=self.hilos)
        self.botonventana.place(x=210, y=10,width=100,height=30)

        self.botonreportes = Button(ventana, text="Reportes", command=self.reportes)
        self.botonreportes.place(x=310, y=10,width=100,height=30)

        self.botonCerrar = Button(ventana, text="Cerrar", command=ventana.quit)
        self.botonCerrar.place(x=610, y=10,width=100,height=30)

        self.img = ImageTk.PhotoImage(Image.open('reloj.png'))
        self.imagen = Label(ventana, image= self.img)
        self.imagen.place(x=550,y=350)

    #FUNCION DEL BOTON CARGAR
    def carga(self):
        self.archivo= abrir()
        #print(self.archivo)
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
        contadorx=0
        contadory=0
        contadorcolumna=1

        self.numero_lineas_produccion=5
        ancho = 250/int(self.numero_lineas_produccion)

        #CREA PRIMERA FILA
        for i in range(0, int(self.numero_lineas_produccion)+1):
            cell = Entry(ventana_principal, width=10)
            cell.grid(padx=5, pady=5, row=1, column=1)
            if contadorx==0:
                cell.insert(0, "Tiempo")
            else:
                cell.insert(0, "Linea "+str(contadorcolumna))
                contadorcolumna+=1
            cell.place(x= 400+contadorx, y= 60+contadory, width=ancho, height=40)
            contadorx+=ancho
        #CREA CONTENIDO DE LA TABLA
        for i in range(0, 5):
            contadorx=0
            for j in range(0, int(self.numero_lineas_produccion)+1):
                cell = Entry(ventana_principal, width=10)
                cell.grid(padx=5, pady=5, row=j, column=i)
                if contadorx==0:
                    cell.insert(0, "")
                else:
                    cell.insert(0, "")
                cell.place(x= 400+contadorx, y= 100+contadory, width=ancho, height=40)
                contadorx+=ancho
            contadorx=0
            contadory+=40
        #
            continue
        self.permitir=1
        MessageBox.showinfo("Aviso!", "Archivo cargado con exito!") # título, mensaje
        #MOSTRAR LISTAS CREADAS
    #    print()
    #    print("------------------------Informacion de:Lineas de produccion-------------------------")
    #    for i in self.lineas_de_produccion.recorrer():
    #        print(i)
    #    print()
    #    print("------------------------Informacion de: Listado Productos-------------------------")
    #    for i in self.listado_producto.recorrer():
    #        print(i)
    
    #FUNCION PARA CARGAR SIMULACION
    def carga_simulacion(self):
        if self.permitir ==0:
            MessageBox.showinfo("Error!", "Debe seleccionar primero un archivo de maquina!") # título, mensaje
        else:
            self.contador=0
            self.archivo= abrir()
            #print(self.archivo)
            self.raiz = ET.parse(self.archivo)
            self.data = self.raiz.getroot()
            #print(len(self.data))
            while self.contador < len(self.data):
                #print(self.data[self.contador].tag)
                if self.data[self.contador].tag=="Nombre":
                    self.nombresimulacion = self.data[self.contador].text
                    #print(self.nombresimulacion) SI COLOCA EL NOMBRE DEL SIMULADOR
                elif self.data[self.contador].tag=="ListadoProductos":
                    self.listado = self.data[self.contador]
                    for i in self.listado:
                        self.listaconstruccion.insertar(i.text)
                    for i in self.listaconstruccion.recorrer():
                        print(i)
                    self.contador+=1
                    continue
                self.contador+=1
                continue

            MessageBox.showinfo("Aviso!", "Archivo cargado con exito!") # título, mensaje
    
    #FUNCION LLAMADO DE HILOS (ANALIZAR)
    def hilos(self):
        if self.permitir ==0:
            MessageBox.showinfo("Error!", "Debe seleccionar primero un archivo de maquina!") # título, mensaje
        else:
            print("analiza")
            #ANALIZADOR DE LISTA
            for i in self.listado_producto.recorrer():
                print(len(i))
                contador=0
                print(i)
                #print(i[contador])
                while contador < len(i):
                    #print(i[contador])
                    if int(self.estado) == 0:
                        if re.search(r"[a-zA-Z]", i[contador]):
                            self.instruccion+=i[contador]
                            contador+=1
                            self.estado = 1
                            continue
                        elif re.search(r"[0-9]", i[contador]):
                            self.estado= 2
                            self.instruccion = ""
                            self.instruccion += i[contador]
                            self.numeroanalisis+=1
                            contador+=1
                            continue
                        elif re.search(r" ", i[contador]):
                            contador+=1
                            continue
                        else:
                            contador+=1
                            continue

                    elif self.estado == 1:
                        if re.search(r"[a-zA-Z]", i[contador]):
                            self.instruccion+=i[contador]
                            contador+=1
                            self.estado = 1
                            continue

                        elif re.search(r',', i[contador]):
                            if self.contadorcomas==0:
                                self.producto_proceso= self.instruccion

                                self.instruccion=""
                                contador+=1
                                self.estado = 0
                            else:
                                self.contadorcomas=0
                                contador+=1
                                continue
                        else:
                            self.estado = 0 

                    elif self.estado == 2:
                        if self.numeroanalisis ==1:
                            if re.search(r"[0-9]", i[contador]):
                                self.instruccion=""
                                self.instruccion += i[contador]
                                contador+=1
                                continue
                            else:
                                self.estado=0
                                self.pasos.insertar(self.instruccion)
                                #self.componentepasos.insertar(self.producto_proceso)
                                self.instruccion=""
                                continue

                        if self.numeroanalisis ==2:
                            if re.search(r"[0-9]", i[contador]):
                                self.instruccion=""
                                self.instruccion += i[contador]
                                contador+=1
                                continue
                            else:
                                self.numeroanalisis=0
                                self.estado=0
                                self.pasos.insertar(self.instruccion)
                                self.componentepasos.insertar(self.producto_proceso)
                                self.instruccion=""
                                continue
                        else:
                            contador+=1
                #self.pasos.insertar(",")
                #self.componentepasos.insertar(",")
                print("TERMINE")
#ANALISIS DE PASOS
            queseanaliza="linea"    #ANALISIS PARA IMPRIMIR CORRECTAMENTE
            contadorcomponente=1    #ANALISIS PARA IMPRIMIR CORRECTAMENTE   
            contadorlinea=1         #ANALISIS PARA IMPRIMIR CORRECTAMENTE 
            contadorgeneral=1       #ANALISIS PARA IMPRIMIR CORRECTAMENTE 
            componenteactual=0
            lineaactual=0
            contadorfor=1
            componenteconstruccion =""
            componenteparavalidacion =""
            validacion = 0
            for i in self.listaconstruccion.recorrer():     #RECORRE LA LISTA DE SIMULACION
                componenteconstruccion = i                  #INDICA QUE EL COMPONENTE QUE SE VA A CONSTRUIR ES EL DE I
                contadorgeneral=1
                
                print(i)
                print("------------------")
                for j in self.componentepasos.recorrer(): 
                    if j == i:
                        print(j)

                        contadorcomponente = 1
                        contadorlinea = 1
                        for k in self.pasos.recorrer():
                            if queseanaliza =="linea":
                                if contadorcomponente==contadorgeneral:
                                    print(k)
                                    queseanaliza="componente"
                                    contadorlinea+=1
                                    continue
                                else:
                                    queseanaliza = "componente"
                                    contadorlinea+=1
                                    continue
                            
                            if queseanaliza =="componente":
                                if contadorcomponente==contadorgeneral:
                                    queseanaliza="linea"
                                    print(k)
                                    contadorcomponente+=1
                                    continue
                                else:
                                    queseanaliza = "linea"
                                    contadorcomponente+=1
                                    continue
                        #print (j)
                        contadorgeneral+=1
                    else: 
                        contadorgeneral+=1
                        continue
                print("----------")    
                print()

#FIN ANALISIS PASOS


            #t1=Thread(target=self.work) 
            #t1.start() 

    #LO QUE HACE MIENTRAS EL HILO ESTA ACTIVO
    def work(self): 
        #HILO
        print("sleep time start") 
        for o in range(10): 
            print(o) 

            contadorx=0
            contadory=0
            self.numero_lineas_produccion=5
            ancho = 250/int(self.numero_lineas_produccion)
            #VA AGREGANDO TABLAS A MODO QUE SE VA CAMBIANDO CUANDO AVANZA EL HILO
            for i in range(0, 5):
                contadorx=0
                for j in range(0, int(self.numero_lineas_produccion)+1):
                    cell = Entry(ventana_principal, width=10)
                    cell.grid(padx=5, pady=5, row=j, column=i)
                    if contadorx==0:
                        cell.insert(0, "Tiempo")
                    else:
                        cell.insert(0, o)
                    cell.place(x= 400+contadorx, y= 100+contadory, width=ancho, height=40)
                    contadorx+=ancho
                contadorx=0
                contadory+=40

            time.sleep(1) 
        print("sleep time stop") 
     
    #FUNCION DEL BOTON REPORTES
    def reportes(self):
        if self.permitir ==0:
            MessageBox.showinfo("Error!", "Debe seleccionar primero un archivo de maquina!") # título, mensaje
        else:
            print("reportes")

    
    
                            

                    
                
        


ventana_principal= Tk()
programa = interfaz(ventana_principal)
ventana_principal.mainloop()
