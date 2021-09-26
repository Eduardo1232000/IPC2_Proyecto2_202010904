from tkinter import *
from tkinter import messagebox as MessageBox
from enum import auto
from typing import List
from abrir_archivo import*
from listas import *
import xml.etree.ElementTree as ET
import os
from PIL import Image,ImageTk
from threading import *
import time
import re
from reporte import*
reportes= reporte()

from analizador import *
analizando = expresion()


class interfaz:
    def __init__(self, ventana):
        #inicializar la ventana
        self.ventana=ventana
        self.ventana.title("Simulacion")    #Titulo programa
        self.ventana.geometry("800x500")  #tamaño de pantalla
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
        self.pasosintermedios= Lista()
        self.lineasintermedias= Lista()
        self.pasosfinales = Cola()
        self.lineasfinales = Cola()
        self.separaciondecomponentes= Cola()
        self.l_final= Lista()
        self.p_final=Lista()
        self.reportefinal = Cola()
        self.lineasreportefinal = Cola()

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
        self.lenlista=0
        self.ancho =0
        self.comp=0

        #BOTONES
        self.botonSaludo = Button(ventana, text="Cargar Archivo",command=self.carga)
        self.botonSaludo.place(x=10, y=10,width=100,height=30)

        self.botonSaludo = Button(ventana, text="Cargar Simulacion",command=self.carga_simulacion)
        self.botonSaludo.place(x=110, y=10,width=100,height=30)

        self.botonventana = Button(ventana, text="Analizar", command=self.hilos)
        self.botonventana.place(x=210, y=10,width=100,height=30)

        self.botonreportes = Button(ventana, text="Reportes", command=self.reportes)
        self.botonreportes.place(x=310, y=10,width=100,height=30)

        self.botonayuda = Button(ventana, text="Ayuda", command=self.ayuda)
        self.botonayuda.place(x=410, y=10,width=100,height=30)

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

        #self.numero_lineas_produccion=5
        contador=0
        while int(contador) < int(self.numero_lineas_produccion):
            self.lineasintermedias.insertar(int(contador)+1)
            self.pasosintermedios.insertar("0")
            contador+=1
        self.ancho = 250/int(self.numero_lineas_produccion)

        #CREA PRIMERA FILA
        for i in range(0, int(self.numero_lineas_produccion)+1):
            cell = Entry(ventana_principal, width=10)
            cell.grid(padx=5, pady=5, row=1, column=1)
            if contadorx==0:
                cell.insert(0, "Segundo")
            else:
                cell.insert(0, "Linea "+str(contadorcolumna))
                contadorcolumna+=1
            cell.place(x= 400+contadorx, y= 60+contadory, width=self.ancho, height=40)
            contadorx+=self.ancho
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
                cell.place(x= 400+contadorx, y= 100+contadory, width=self.ancho, height=40)
                contadorx+=self.ancho
            contadorx=0
            contadory+=40
        #
        
            continue
        self.componentelabel = Label(ventana_principal, text="")
        self.componentelabel.place(x=50, y=100,width=300, height=50)
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
#ANALISIS DE PASOS-----------------------------------------------------------------------------------------------------------------------
            queseanaliza="linea"    #ANALISIS PARA IMPRIMIR CORRECTAMENTE
            contadorcomponente=1    #ANALISIS PARA IMPRIMIR CORRECTAMENTE   
            contadorlinea=1         #ANALISIS PARA IMPRIMIR CORRECTAMENTE 
            contadorgeneral=1       #ANALISIS PARA IMPRIMIR CORRECTAMENTE 
            componenteactual=0
            lineaactual=0
            lineainstruccionactual =0       #PARA SACAR LAS INSTRUCCIONES FINALES
            componenteinstruccionactual=0   #PARA SACAR LAS INSTRUCCIONES FINALES
            contadordelinea = 0 #para analizar cada uno
            posicionactuallinea=0
            posicionfinallinea=0
            for i in self.listaconstruccion.recorrer():     #RECORRE LA LISTA DE SIMULACION
                componenteconstruccion = i                  #INDICA QUE EL COMPONENTE QUE SE VA A CONSTRUIR ES EL DE I
                contadorgeneral=1
                
                print(i)
                #print("------------------")
                for j in self.componentepasos.recorrer(): 
                    if j == i:
                        #print(j)

                        contadorcomponente = 1
                        contadorlinea = 1
                        for k in self.pasos.recorrer():
                            if queseanaliza =="linea":
                                if contadorcomponente==contadorgeneral:
                                    #SOLO IMPRIME LINEAS DE CONSTRUCCION
                                    lineaactual=k
                                    lineainstruccionactual=k
                                    #print(k)

                                    #va a encontrar la posicion final de la linea para usarla despues
                                    contadorl=1
                                    contadorp=1

                                    for q in self.lineasintermedias.recorrer():
                                        if int(q) ==int(lineaactual):
                                            for w in self.pasosintermedios.recorrer():
                                                if contadorl == contadorp: 
                                                    posicionfinallinea=w
                                                    #print(q, w)
                                                    #print()
                                                    contadorp+=1
                                                    
                                                else:
                                                    contadorp+=1
                                            contadorp=1
                                            contadorl+=1
                                        else:
                                            contadorl+=1
                                    posicionactuallinea = int(posicionfinallinea)
                                                
                                            
                                    #aqui termina el analisis de la ultima pos

                                    queseanaliza="componente"
                                    contadorlinea+=1
                                    continue
                                else:
                                    queseanaliza = "componente"
                                    contadorlinea+=1
                                    continue
                            #ESTA INCOMPLETO INICIA SIEMPRE DESDE 0 ARREGLAR ESO
                            if queseanaliza =="componente":
                                if contadorcomponente==contadorgeneral:
                                    queseanaliza="linea"
                                    componenteinstruccionactual=k
                                    #SOLO IMPRIME COMPONENTES
                                    #print("L"+str(lineaactual)+"C"+str(posicionactuallinea))
                                    while int(posicionactuallinea) < int(componenteinstruccionactual):
                                        posicionactuallinea +=1
                                        #print("L"+str(lineaactual)+"C"+str(posicionactuallinea))
                                        self.lineasintermedias.insertar(lineaactual)
                                        self.pasosintermedios.insertar(posicionactuallinea)
                                        continue

                                    while int(posicionactuallinea) > int(componenteinstruccionactual):
                                        posicionactuallinea -=1
                                        #print("L"+str(lineaactual)+"C"+str(posicionactuallinea))
                                        self.lineasintermedias.insertar(lineaactual)
                                        self.pasosintermedios.insertar(posicionactuallinea)
                                        continue
                                    #print(k)
                                    
                                    contadorcomponente+=1
                                    continue
                                else:
                                    queseanaliza = "linea"
                                    contadorcomponente+=1
                                    continue
                        
                        #print (j)
                        algo= int(posicionactuallinea)
                        self.separaciondecomponentes.insertar(lineaactual)
                        self.separaciondecomponentes.insertar(algo)
                        
                        self.pasosintermedios.insertar(int(algo))
                        self.lineasintermedias.insertar(lineaactual)
                        contadorgeneral+=1
                    else: 
                        contadorgeneral+=1
                        continue
                
                
                #print("----------")
                posicionactuallinea=0
                contador=0
                while int(contador) < int(self.numero_lineas_produccion):
                    self.lineasintermedias.insertar(int(contador)+1)
                    self.pasosintermedios.insertar("0")
                    contador+=1    
                print()


#FIN ANALISIS PASOS------------------------------------------------------------------------------------------------------------------------
        

              


            #HILOS
            t1=Thread(target=self.work) 
            t1.start() 

    #LO QUE HACE MIENTRAS EL HILO ESTA ACTIVO
    def work(self): 
        #HILO
        #IMPRIME LISTA CON LA CONSTRUCCION


        columna=1
        fila =0

        contenido1 = "1"
        contenido2 = "2"
        contenido3 = "3"
        contenido4 = "4"
        contenido5 = "5"

        columna1 = 0
        columna2 = 0
        columna3 = 0
        columna4 = 0
        colum = 0



        segundo1=0
        segundo2=0
        segundo3=0
        segundo4=0
        segundo5=0

        contadorx=0
        contadory=0
        contadorcolumna=1
                

        repetido=0
        contadorl=1
        contadorp=1
        componentefinal=-1
        lineafinal=-1

        enposicion=0
        construir=0
        mover=0
        texto=""
        contadortexto=0

        for i in self.lineasintermedias.recorrer():
            for j in self.pasosintermedios.recorrer():
                if contadorl==contadorp:

                    if int(j)==0:
                        if repetido == 0:
                            contadortexto+=1
                            self.comp=1
                            #print(contadortexto)
                            for o in self.listaconstruccion.recorrer():
                                #print(self.comp)
                                #print(contadortexto)
                                if self.comp==contadortexto:
                                    #print(contadortexto, self.comp)
                                    texto=str(o)
                                    #print(o)
                                    break
                                else:
                                    self.comp+=1
                                    texto="nada"
                            
                            #Cambiar componente
                            self.componentelabel = Label(ventana_principal, text=texto)
                            self.componentelabel.place(x=50, y=100,width=300, height=50)
                            self.componentelabel.config(font=("Verdana",24))
                            # 
                            self.reportefinal.insertar("inicio")
                            self.lineasreportefinal.insertar("inicio")
                            segundo5=1
                            repetido = 1
                            
                            
                        else:
                            repetido=0
                        enposicion=1
                        contadorp+=1
                    if int(j) == int(componentefinal):
                        if int(i) == int(lineafinal):
                            construir=1         
                            contadorp+=1
                    
                    if construir==1:
                        #print("L"+str(i)+" Construir C"+str(j))
                        
                        construir=0
                        colum = int(i)
                        contenido5="L"+str(i)+" Construir C"+str(j)
                        self.reportefinal.insertar(contenido5)
                        self.lineasreportefinal.insertar(i)
                        
                    elif enposicion==1:
                        #print("L"+str(i)+" en posicion "+str(j))
                        contenido5="L"+str(i)+" en posicion "+str(j)
                        colum = int(i)
                        enposicion=0
                        self.reportefinal.insertar(contenido5)
                        self.lineasreportefinal.insertar(i)
                    
                    else:    
                        #print("L"+str(i)+" Mover a C"+str(j))
                        colum=int(i)
                        contenido5="L"+str(i)+" Mover a C"+str(j)
                        colum = int(i)
                        self.reportefinal.insertar(contenido5)
                        self.lineasreportefinal.insertar(i)
                        

                    
                    lineafinal=int(i)
                    componentefinal = int(j) 


                    #tabla
                    #CREA CONTENIDO DE LA TABLA
                    columna=1
                    fila =0
                    contadorx=0
                    contadory=0
                    contadorcolumna=1
                    

                    for q in range(0, 5):
                        fila+=1
                        columna=1
                        contadorx=0
                        for w in range(0, int(self.numero_lineas_produccion)+1):
                            #print(fila, columna)
                            cell = Entry(ventana_principal, width=10)
                            cell.grid(padx=5, pady=5, row=w, column=q)
                            if contadorx==0:
                                if fila==1:
                                    cell.insert(0, segundo1)
                                if fila==2:
                                    cell.insert(0, segundo2)
                                    segundo1=segundo2
                                if fila==3:
                                    cell.insert(0, segundo3)
                                    segundo2=segundo3
                                if fila==4:
                                    cell.insert(0, segundo4)
                                    segundo3=segundo4
                                if fila==5:
                                    cell.insert(0, segundo5)
                                    segundo4=segundo5
                                    self.timerlabel = Label(ventana_principal, text=segundo5)
                                    self.timerlabel.place(x=620, y=350,width=50,height=50)
                                    self.timerlabel.config(bg="skyblue",font=("Verdana",24))
                                    segundo5+=1

                                columna+=1
                            else:
                                if fila== 1:
                                    
                                    if int(columna1)== int(columna)-1:  
                                        cell.insert(0, contenido1)
                                    else:
                                        cell.insert(0, "")

                                elif fila== 2:
                                    if int(columna2)== int(columna)-1:   
                                        cell.insert(0, contenido2)
                                        contenido1 = contenido2
                                        columna1=columna2
                                    else:
                                        cell.insert(0, "")

                                elif fila== 3:
                                    if int(columna3)== int(columna)-1:   
                                        cell.insert(0, contenido3)
                                        contenido2 = contenido3
                                        columna2=columna3
                                    else:
                                        cell.insert(0, "")

                                elif fila== 4:
                                    if int(columna4)== int(columna)-1:   
                                        cell.insert(0, contenido4)
                                        contenido3 = contenido4
                                        columna3=columna4
                                    else:
                                        cell.insert(0, "")

                                elif fila== 5:
                                    if int(colum)== int(columna)-1:   
                                        cell.insert(0, str(contenido5))
                                        contenido4 = contenido5
                                        columna4=colum
                                    else:
                                        cell.insert(0, "")
                                columna+=1

                            cell.place(x= 400+contadorx, y= 100+contadory, width=self.ancho, height=40)
                            contadorx+=self.ancho 
                        contadorx=0
                        contadory+=40
                        continue
                    #tabla
                    
                    time.sleep(1)





                contadorp+=1
            #print("L"+str(i)+"Construir"+str(componentefinal))
            contadorp=1
            contadorl+=1


             
     
    #FUNCION DEL BOTON REPORTES
    def reportes(self):
        if self.permitir ==0:
            MessageBox.showinfo("Error!", "Debe seleccionar primero un archivo de maquina!") # título, mensaje
        else:
            print("---------------Reportes----------------------")
            #for i in self.reportefinal.recorrer():
            #    print(i)
            reporte.reporte_construccion(self,self.reportefinal,self.numero_lineas_produccion,self.listaconstruccion, self.lineasreportefinal)
            
    def ayuda(self):
        MessageBox.showinfo("Datos personales", "Nombre: Eduardo Alexander Reyes Gonzalez, Carnet:202010904")
        MessageBox.showinfo("AYUDA!", "Este programa fue creado con la finalidad de analizar los caminos de las lineas de produccion.")
        MessageBox.showinfo("AYUDA!", "Las lineas obtienen sus coordenadas desde un archivo con extension xml, hasta que llega a la ultima coordenada termina su opcion Analizar")
        MessageBox.showinfo("AYUDA!","Boton Cargar Archivo: abre una ventana en donde el usuario puede subir los datos de la maquina")
        MessageBox.showinfo("AYUDA!", "Boton Cargar simulacion: Abre una ventana en donde el usuario puede cargar el archivo que contiene los datos de los productos deseados")
        MessageBox.showinfo("AYUDA!", "Boton analizar: Analiza y muestra los pasos que la maquina realiza en tiempo real")
        MessageBox.showinfo("AYUDA!", "Boton Salir: Finaliza el programa")
        print("-----------AYUDA-----------")
        print("Nombre: Eduardo Alexander Reyes Gonzalez")
        print("Carnet: 202010904")
        print("-----SOBRE LA APLICACION---")
        print("Este programa fue creado con la finalidad de analizar los caminos de las lineas de produccion.") 
        print("Las lineas obtienen sus coordenadas desde un archivo con extension xml")
        print("hasta que llega a la ultima coordenada termina su opcion Analizar")   
    
                            

                    
                
        


ventana_principal= Tk()
programa = interfaz(ventana_principal)
ventana_principal.mainloop()
