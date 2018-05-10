#  Rodrigo Pacheco
#  Servicios y Aplicaciones Telemáticas. Universidad Rey Juan Carlos
#  r.pachecom at alumnos dot urjc dot com


from django.shortcuts import render
from django.http import HttpResponse
import museums.xmlparser as parser
import museums.models as DDBB

URL1 = 'https://raw.githubusercontent.com/CursosWeb/CursosWeb.github.io/master/etc/201132-0-museos.xml'
URL2 = 'https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full'

def other(self):
    museum_matrix = []
    museum_matrix = parser.parse_to_matrix(URL2, True)
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
        print('Nombre = ' + raw[0])
        print('Accesibilidad = ' + str(raw[4]))
        print('Addderss = ' + raw[6])
        print('Email = ' + raw[10])
        print(museum)
        museum.save()
    return(HttpResponse('Completado'))
