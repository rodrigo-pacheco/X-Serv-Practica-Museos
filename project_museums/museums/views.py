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
from django.template.loader import get_template
from django.template import Context
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

import museums.xmlparser as parser
import museums.models as DDBB

from itertools import cycle


URL1 = 'https://raw.githubusercontent.com/CursosWeb/CursosWeb.github.io/master/etc/201132-0-museos.xml'
URL2 = 'https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full'

accessibilityDic = {True: 'checked="True"',
                    False: ''}                                                  # Show checkbox checked or not

ACCESSIBILITY = False
DISTRICT = 'TODOS'

USER_WEB = """<p><a href={} >{}</a> {} </p><hr>"""

def add_comment(comment, museum):
    DDBB.Comment(text = comment, museum=museum).save()
    museum.num_comments += 1
    museum.save()


def get_user_webs():
    users_webs = ''
    for user in User.objects.all():
        title = ''
        try:
            title = DDBB.Style.objects.get(user__username=user.username).title
        except DDBB.Style.DoesNotExist:
            pass
        if title == '':                                                         # '' is default value
            users_webs += USER_WEB.format('/museos/' + str(user.id,),
                                          'Página de ' + str(user.username),
                                          '')
        else:
            users_webs += USER_WEB.format('/museos/' + str(user.id,),
                                          title,
                                          '  por ' + str(user.username))
    return users_webs


def museums_top_comments():
    museums_topcomments = DDBB.Museum.objects.all()                             # At first I tryed doing it as I had learnt from here: https://stackoverflow.com/questions/21106869/how-to-find-top-x-highest-values-in-column-using-django-queryset-without-cutting/21279059
    museums_topcomments = museums_topcomments.exclude(num_comments=0)           # It worked but filtering by accessibility aftwerwars was not easy
    museums_topcomments = museums_topcomments.order_by('-num_comments')         # Then I found the following way, that is much easier
    if ACCESSIBILITY:
        museums_topcomments = museums_topcomments.exclude(accessibility=False)
    return museums_topcomments[:5]


@csrf_exempt
def slash(request):
    global ACCESSIBILITY

    if request.method == 'GET':
        try:
            if(len(DDBB.Museum.objects.all()) < 1):                             # Check if DataBase is empty
                return(HttpResponseRedirect('/load'))
        except OperationalError:                                                # No DataBase at all
            exit('No Data Base. Please run manage.py migrate')

        top_museums = museums_top_comments()
        try:
            template = get_template('museums/slash.html')
        except NameError:
            exit('Server stopped working. Template missing')

        button_status = accessibilityDic[ACCESSIBILITY]                         # Get string to check button or nor
        context = Context({'aut': request.user.is_authenticated(),
                           'name': request.user.username,
                           'users': get_user_webs(),
                           'accessible': button_status,
                           'museums': top_museums})
        return(HttpResponse(template.render(context)))

    elif request.method == 'POST':
        if request.POST['Change'] == 'accessibility':
            ACCESSIBILITY = not ACCESSIBILITY
            return(HttpResponseRedirect('/'))
        else:
            return(HttpResponseRedirect('/not_found'))
    else:
        return(HttpResponseRedirect('/not_found'))


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


@csrf_exempt
def load_DDBB(request):
    if request.method == 'GET':
        try:
            template = get_template('museums/loadDDBB.html')
        except NameError:
            exit('Server stopped working. Template missing')

        context = Context({'aut': request.user.is_authenticated(),
                           'name': request.user.username,
                           'users': get_user_webs()})
        return(HttpResponse(template.render(context)))
    elif request.method == 'POST':
        if request.POST['Load'] == 'DDBB':
            load_data()
            return(HttpResponseRedirect('/'))
    else:
        return(HttpResponseRedirect('/not_found'))


@csrf_exempt
def my_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)                                                    # Help from 'How to log a user in': https://docs.djangoproject.com/en/2.0/topics/auth/default/
        return(HttpResponseRedirect('/'))
    else:
        return(HttpResponseRedirect('/'))


def get_museum_list(district):
    try:
        museum_selection = DDBB.Museum.objects.filter(district=district)
    except DDBB.Museum.DoesNotExist:
        museum_selection = []
    if district == 'TODOS':
        museum_selection = DDBB.Museum.objects.all()
    return(museum_selection)


def get_district_names():
    districts = ['TODOS']
    for museum in DDBB.Museum.objects.all():
        if museum.district not in districts:
            districts.append(museum.district)
    return(districts)


@csrf_exempt
def museums(request):
    global DISTRICT
    if request.method == 'GET':
        try:
            template = get_template('museums/museums.html')
        except NameError:
            exit('Server stopped working. Template missing')

        context = Context({'aut': request.user.is_authenticated(),
                           'name': request.user.username,
                           'users': get_user_webs(),
                           'districts': get_district_names(),
                           'museums': get_museum_list(DISTRICT)})
        return(HttpResponse(template.render(context)))

    elif request.method == 'POST':
        print(DISTRICT)
        DISTRICT = request.POST['District']
        print(DISTRICT)
        return(HttpResponseRedirect('/museos'))
    else:
        return(HttpResponseRedirect('/not_found'))


def get_museum_comments(id):
    try:
        return(DDBB.Comment.objects.get(museum__id=id))
    except DDBB.Comment.DoesNotExist:
        return([])


@csrf_exempt
def museum_info(request, id):
    if request.method == 'GET':
        try:
            template = get_template('museums/museum_info.html')
        except NameError:
            exit('Server stopped working. Template missing')

        context = Context({'museum': DDBB.Museum.objects.get(id=id),
                           'comments': get_museum_comments(id),
                           'aut': request.user.is_authenticated()})
        return(HttpResponse(template.render(context)))

    elif request.method == 'POST':
        print(request.POST)
        return(HttpResponseRedirect('/not_found')) ########################################################################
    else:
        return(HttpResponseRedirect('/not_found'))

def not_found(request):
    try:
        template = get_template('museums/not_found.html')
    except NameError:
        exit('Server stopped working. Template missing')
    context = Context({'aut': request.user.is_authenticated(),
                       'name': request.user.username,
                       'users': get_user_webs()})
    return(HttpResponse(template.render(context)))
