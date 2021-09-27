import webbrowser
from listas import *
class reporte:
    def reporte_construccion(self,listado,no_lineas,componente,linea,segundos):
        inicio=0
        contadors=0
        for i in componente.recorrer():
            inicio+=1
            

            reporte = open(str(i)+".html",'w')
            html = '<!DOCTYPE html>\n'
            html += '<html lang="en">\n'
            html += '<head>\n'
            html += "<title>Reporte de Construccion de "+str(i)+"</title>\n"
            html += "</head>\n"
            html += '<body bgcolor= "B7F7DE">\n'
            html +='<center>\n'
            html +='<font face="Comic Sans MS,arial,verdana"><h1>Reporte de Construccion de '+str(i)+'</h1><br>'
            html += '<table border="1" bgcolor= "#FFFFF" style="width:60%; border: 1px ; margin: 5px">\n'
            contador=0
            html += '<tr>'

            while int(contador) < int(no_lineas)+1:      #El +1 es por la columna tiempo
                if contador==0:
                    html+= '<th align="center">Tiempo</th>'
                else:
                    html+= '<th align="center">Linea de ensamblaje'+str(contador)+'</th>'
                contador+=1
            html += "</tr>\n"
            contadorl=1
            contadorp=1

            columna=0
            columnahtml=0
            segundo=0
            inicioactual=0
            #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            for a in linea.recorrer():
                if a == "inicio":
                    inicioactual+=1
                    contadorl+=1
                    segundo=1
                    continue
                    
                if inicio==inicioactual:
                    for b in listado.recorrer():
                        if int(contadorl) == int(contadorp):
                            #print (segundo,b)
                            columna=int(a)
                            columnahtml=0
                            
                            while int(columnahtml) < int(no_lineas)+1:      #El +1 es por la columna tiempo
                                #print(columna,columnahtml)
                                if columnahtml==0:
                                    html+= '<th align="center">'+str(segundo)+'</th>'
                                else:
                                    if int(columna)==int(columnahtml):
                                        html+= '<th align="center">'+str(b)+'</th>'
                                        
                                    else:
                                        html+= '<th align="center"> </th>'
                                        

                                columnahtml+=1
                            html += "</tr>\n"


                            segundo+=1
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
                    



            #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


                


            html += "</table><br>\n"
            contadors=0
            for c in segundos.recorrer():
                print(c)
                if contadors==inicio:
                    html += '<h1>El producto '+str(i)+' Se puede elaborar en '+str(c)+' segundos</h1>'
                    contadors+=1
                    break
                else:
                    contadors+=1

            
            html += "</body>\n"
            html += '</html >'

            reporte.write(html)
            reporte.close()
            print("El reporte de tokens se ha generado exitosamente")
            webbrowser.open_new_tab(str(i)+'.html')
        