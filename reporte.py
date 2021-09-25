import webbrowser
from listas import *
class reporte:
    def reporte_construccion(self,listado,no_lineas,componente):
        for i in componente.recorrer():
            

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


            html += "</table><br>\n"
            html += "</body>\n"
            html += '</html >'

            reporte.write(html)
            reporte.close()
            print("El reporte de tokens se ha generado exitosamente")
            webbrowser.open_new_tab(str(i)+'.html')
        