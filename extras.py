from listas import *

Palabra = Lista()
Palabra.insertar("hola")
Palabra.insertar("hola")
Palabra.insertar("hola")

for i in Palabra.recorrer():
    print(i)

listacola = Cola()
listacola.insertar("1")
listacola.insertar("2")
listacola.insertar("3")
listacola.insertar("4")
listacola.insertar("5")
for i in listacola.recorrer():
    print(i)
print()
listacola.eliminar()
listacola.eliminar()
listacola.eliminar()
for i in listacola.recorrer():
    print(i)