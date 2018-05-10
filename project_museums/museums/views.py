#  Rodrigo Pacheco
#  Servicios y Aplicaciones Telemáticas. Universidad Rey Juan Carlos
#  r.pachecom at alumnos dot urjc dot com


from django.shortcuts import render
from django.http import HttpResponse
import museums.xmlparser as parser

URL = 'https://raw.githubusercontent.com/CursosWeb/CursosWeb.github.io/master/etc/201132-0-museos.xml'

def other(self):
    museum_matrix = []
    museum_matrix = parser.parse_to_matrix(URL, True)
    for raw in museum_matrix:
        print(raw[0])
        import time
        time.sleep(1)
    HTTPResponse('Completado')
