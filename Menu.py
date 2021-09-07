from tkinter import *
from tkinter import messagebox as MessageBox
from enum import auto
from abrir_archivo import*


class interfaz:
    def __init__(self, ventana):
        #inicializar la ventana
        self.ventana=ventana
        self.ventana.title("Simulacion")    #Titulo programa
        self.ventana.geometry("750x500")  #tamaño de pantalla
        self.ventana.configure(bg='skyblue')#color de fondo ventana


        #BOTONES
        self.botonSaludo = Button(ventana, text="Cargar Archivo",command=self.carga)
        self.botonSaludo.place(x=10, y=10,width=100,height=30)

        self.botonventana = Button(ventana, text="Analizar", command=self.analizar)
        self.botonventana.place(x=110, y=10,width=100,height=30)

        self.botonreportes = Button(ventana, text="Reportes", command=self.reportes)
        self.botonreportes.place(x=210, y=10,width=100,height=30)

        self.botonCerrar = Button(ventana, text="Cerrar", command=ventana.quit)
        self.botonCerrar.place(x=610, y=10,width=100,height=30)

    #FUNCION DEL BOTON CARGAR
    def carga(self):
        self.archivo= abrir()
        print(self.archivo)
        MessageBox.showinfo("Aviso!", "Archivo cargado con exito!") # título, mensaje

    #FUNCION DEL BOTON ANALIZAR
    def analizar(self):
        print("analiza")

    #FUNCION DEL BOTON REPORTES
    def reportes(self):
        print("reportes")

ventana_principal= Tk()
programa = interfaz(ventana_principal)
ventana_principal.mainloop()
