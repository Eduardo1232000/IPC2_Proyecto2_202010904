from listas import *
linea = Lista()

linea.insertar(str(10))
linea.insertar(str(20))
linea.insertar(str(11))
linea.insertar(str(21))
linea.insertar(str(12))
linea.insertar(str(22))
linea.insertar(str(13))


linea.insertar(str(10))
linea.insertar(str(11))
linea.insertar(str(20))
linea.insertar(str(21))
linea.insertar(str(12))
linea.insertar(str(22))

algo=0
otrocontador=0
#len
for i in linea.recorrer():
    algo+=1
otro=0
contador=0
validacion=0
l=1
lineas_produccion =2

#print(algo)
dato=""
while contador<algo:
    validacion =0
    otrocontador=0
    for i in linea.recorrer():
        if i[0] ==str(l):
            #print(i)
            validacion=1
            dato = i
            break
    l+=1
    print(dato)
    linea.eliminar_dato(dato)
    if l> lineas_produccion:
        l=1
    if validacion==1:
        contador+=1

    


    
