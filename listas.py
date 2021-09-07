class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class Lista:
    def __init__(self):
        self.cabeza = None                          
        self.cola = None                            
        self.longitud = 0
    
    def insertar(self, dato):
        nodo_nuevo = Nodo(dato)
        if self.cabeza:
            self.cabeza.siguiente = nodo_nuevo      #DEFINE QUE EL SIGUIENTE DATO DE LA LISTA SERA EL NUEVO NODO
            self.cabeza = nodo_nuevo                #DEFINE QUE LA CABEZA ES EL NUEVO NODO
        else:
            self.cabeza = nodo_nuevo                #SI ESTA VACIO ENTONCES LA CABEZA DE LA LISTA SERA EL NUEVO
            self.cola = nodo_nuevo                  # Y EL FINAL DE LA LISTA TAMBIEN SERA EL NUEVO NODO (SOLO SI ESTA VACIO)
    
    def recorrer(self):
        valor_actual = self.cola
        while valor_actual:
            dato = valor_actual.dato
            valor_actual = valor_actual.siguiente
            yield dato

class Cola:
    def __init__(self):
        self.cabeza = None                          
        self.cola = None                            
        self.longitud = 0
    
    def insertar(self, dato):
        nodo_nuevo = Nodo(dato)
        actual= self.cola
        if actual=="nada":
            self.cabeza=nodo_nuevo
            self.cola=nodo_nuevo
            self.longitud+=1
            return
        if self.cabeza:
            self.cabeza.siguiente = nodo_nuevo      #DEFINE QUE EL SIGUIENTE DATO DE LA LISTA SERA EL NUEVO NODO
            self.cabeza = nodo_nuevo                #DEFINE QUE LA CABEZA ES EL NUEVO NODO
            self.longitud +=1
        else:
            self.cabeza = nodo_nuevo                #SI ESTA VACIO ENTONCES LA CABEZA DE LA LISTA SERA EL NUEVO
            self.cola = nodo_nuevo                  # Y EL FINAL DE LA LISTA TAMBIEN SERA EL NUEVO NODO (SOLO SI ESTA VACIO)
            self.longitud +=1
    
    def recorrer(self):
        valor_actual = self.cola
        while valor_actual:
            dato = valor_actual.dato
            valor_actual = valor_actual.siguiente
            yield dato

    def eliminar(self):
        actual = self.cola
        if int(self.longitud)>1:
            self.cola = actual.siguiente
            self.longitud -= 1
        elif int(self.longitud)==1:
            actual.siguiente = "nada"
            self.cola= actual.siguiente
            self.longitud -= 1
        return