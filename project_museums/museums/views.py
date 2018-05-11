#  Rodrigo Pacheco
#  Servicios y Aplicaciones Telemáticas. Universidad Rey Juan Carlos
#  r.pachecom at alumnos dot urjc dot com


from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.db import IntegrityError
from django.db import OperationalError
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import museums.xmlparser as parser
import museums.models as DDBB


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

@csrf_exempt
def slash(request):
    if request.method == 'GET':
        try:
            if(len(DDBB.Museum.objects.all()) < 1):                                 # Check if DataBase is empty
                return(HttpResponse(                                                # Help from http://www.echoecho.com/htmlforms07.htm
                       """<form method=post accept-charset="utf-8">URL:<br>
                          <input type="hidden" name="Load" value="DDBB">
                          <input type="submit" value="Cargar BBDD"></form>"""))
        #########################################################################################################################
        ######################### Caso inicial en el que no se ha cargado la base de datos. Devolver opción de cargar #################################################
        #########################################################################################################################
        except OperationalError:                                                    # No DataBase at all
            exit('No Data Base. Please run manage.py migrate')

        top_comments = (DDBB.Museum.objects.order_by('-num_comments')               # Help obtained from https://stackoverflow.com/questions/21106869/how-to-find-top-x-highest-values-in-column-using-django-queryset-without-cutting/21279059
                        .values_list('num_comments', flat=True))                    # List with number of comments in decreasing order
        top_records = (DDBB.Museum.objects.order_by('-num_comments')                # List of museums sorted by decreasing number of comments
                       .filter(num_comments__in=top_comments[:5]))


        museums_topcomments = []
        for i in range(len(top_comments)):
            if top_comments[i] > 0:
                museums_topcomments.append(DDBB.Museum.objects
                                          .get(name=top_records[i]))
            elif i > 0:                                                             # 5 museums obtained already
                break
            else:
                break

        for i in range(len(museums_topcomments)):
            print(museums_topcomments[i].name)
        return(HttpResponse('hola'))

    elif request.method == 'POST':
        if request.POST["Load"] == 'DDBB':
            load_data()
            return(HttpResponseRedirect('/'))
        elif request.POST["Load"] == 'accessibility':
################################################################################
            Se pide mostrar accesibilidad
################################################################################
            return(HttpResponseRedirect('/'))
