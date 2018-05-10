#  Rodrigo Pacheco
#  Servicios y Aplicaciones Telemáticas. Universidad Rey Juan Carlos
#  r.pachecom at alumnos dot urjc dot com


from django.shortcuts import render
from django.http import HttpResponse
import museums.xmlparser as parser
import museums.models as DDBB

URL = 'https://raw.githubusercontent.com/CursosWeb/CursosWeb.github.io/master/etc/201132-0-museos.xml'

def other(self):
    museum_matrix = []
    museum_matrix = parser.parse_to_matrix(URL, True)
    for raw in museum_matrix:
        museum = DDBB.Museum(name = raw[0],
                             description = raw[1],
                             open_hours = raw[2],
                             transport = raw[3],
                             accessibility = raw[4],
                             url = raw[5],
                             address = raw[6],
                             quarter = raw[7],
                             district = raw[8],
                             tlf_number = raw[9],
                             email = raw[10])
        museum.save()
    return(HttpResponse('Completado'))
