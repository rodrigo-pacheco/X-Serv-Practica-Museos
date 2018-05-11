#  Rodrigo Pacheco
#  Servicios y Aplicaciones Telemáticas. Universidad Rey Juan Carlos
#  r.pachecom at alumnos dot urjc dot com


from django.shortcuts import render
from django.http import HttpResponse
from django.db import IntegrityError
import museums.xmlparser as parser
import museums.models as DDBB
from django.utils import timezone

URL1 = 'https://raw.githubusercontent.com/CursosWeb/CursosWeb.github.io/master/etc/201132-0-museos.xml'
URL2 = 'https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full'

def load_data():
    museum_matrix = []
    museum_matrix = parser.parse_to_matrix(URL2, True)
    for raw in museum_matrix:
        museum = DDBB.Museum(name = raw[0],         description = raw[1],
                             open_hours = raw[2],   transport = raw[3],
                             url = str(raw[5]),     address = str(raw[6]),
                             quarter = raw[7],      district = raw[8],
                             tlf_number = raw[9],   email = raw[10],
                             accessibility = raw[4])
        try:
            museum.save()
        except IntegrityError:
            print('Did not add ' + raw[0] + '. Already in DataBase')
            continue
    return True

def add_comment(comment, museum):
    DDBB.Comment(text = comment, museum=museum).save()
    museum.num_comments += 1
    museum.save()

def slash(request):
    # topcoments = get
    # load_data()
    # add_comment('ME gusta montonazo', DDBB.Museum.objects.get(name='Templo de Debod'))
    # add_comment('A mirar las estrellas', DDBB.Museum.objects.get(name='Museo de la Guardia Civil'))
    # try:
    top_comments = (DDBB.Museum.objects.order_by('-num_comments')
                        .values_list('num_comments', flat=True).distinct())
    top_records = (DDBB.Museum.objects.order_by('-num_comments')
                       .filter(num_comments__in=top_comments[:5]))
    # for museo in top_comments:
    #     print(museo)

    for i in range(5):
        print(i)
        print(top_comments)
        # if top_comments[i] > 0:
            # print(top_records[i])
    return(HttpResponse('hola'))
