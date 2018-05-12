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

from itertools import cycle
accessIterator = cycle(['checked="True"', ''])  # Show checkbox checked or not          # Help from https://stackoverflow.com/questions/10986970/python-how-to-toggle-between-two-values and https://stackoverflow.com/questions/12700626/what-is-the-proper-way-to-check-and-uncheck-a-checkbox-in-html5


URL1 = 'https://raw.githubusercontent.com/CursosWeb/CursosWeb.github.io/master/etc/201132-0-museos.xml'
URL2 = 'https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full'


ACCESSIBILITY = ''
FORM_SLASH =  """ <form method=post accept-charset="utf-8">
                  <input type="hidden" name="Load"   value="{}">
                  <input type="hidden" name="Change" value="{}">
                  {}
                  </form>"""                                                            # Help from http://www.echoecho.com/htmlforms07.htm
BUTTON = """<input type="radio" onclick="this.form.submit();" {}">"""                   # Help from: https://forums.digitalpoint.com/threads/html-checkbox-onclick-submit.1271195/

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
    global ACCESSIBILITY
    global FORM_SLASH
    if request.method == 'GET':
        try:
            if(len(DDBB.Museum.objects.all()) < 1):                                 # Check if DataBase is empty
                return(HttpResponse(FORM_SLASH.format(
                       'DDBB', '_', '<input type="submit" value="Cargar BBDD">')))
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
        added_museums = 0
        for i in range(len(top_comments)):
            added_museums += 1
            if added_museums > 5:                                                   # 5 museums obtained already
                break
            elif top_comments[i] >= 0:
                museums_topcomments.append(DDBB.Museum.objects
                                          .get(name=top_records[i]))
            else:
                break

        print('Accesibilidad: ' + ACCESSIBILITY)
        return(HttpResponse('Accesibilidad: ' +
               FORM_SLASH.format('_', 'accessibility', BUTTON.format(ACCESSIBILITY))))
################################################################################
#            Botón para accesibilidad
################################################################################
        # for i in range(len(museums_topcomments)):
        #     print(museums_topcomments[i].name)
        # return(HttpResponse('hola'))

    elif request.method == 'POST':
        print(request.POST)
        if request.POST['Load'] == 'DDBB':
            load_data()
            return(HttpResponseRedirect('/'))
        elif request.POST['Change'] == 'accessibility':
            ACCESSIBILITY = next(accessIterator)
            return(HttpResponseRedirect('/'))
        else:
            return(HttpResponseRedirect('/'))
################################################################################
#            Redirigir a Página nula
################################################################################
