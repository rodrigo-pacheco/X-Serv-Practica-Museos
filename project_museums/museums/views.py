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
from django.utils.datastructures import MultiValueDictKeyError
from collections import OrderedDict

import json
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
PAGE_LINK = '<a href="/{}/{}">{}</a>'


def user_title(user):
    try:
        title = DDBB.Style.objects.get(user__username=user.username).title
    except DDBB.Style.DoesNotExist:
        title = 'Página de ' + str(user.username)
    return(title)

def get_user_webs():
    users_webs = ''
    for user in User.objects.all():
        if user.is_staff == True:                                               # Avoid showing admin's sites
            continue
        title = user_title(user)
        users_webs += USER_WEB.format('/' + str(user.username),
                                     title, '  por ' + str(user.username))
    return users_webs


def museums_top_likes():
    museums_toplikes = DDBB.Museum.objects.all()                                # At first I tryed doing it as I had learnt from here: https://stackoverflow.com/questions/21106869/how-to-find-top-x-highest-values-in-column-using-django-queryset-without-cutting/21279059
    museums_toplikes = museums_toplikes.exclude(num_likes=0)                    # It worked but filtering by accessibility aftwerwars was not easy
    museums_toplikes = museums_toplikes.order_by('-num_likes')                  # Then I found the following way, that is much easier
    if ACCESSIBILITY:
        museums_toplikes = museums_toplikes.exclude(accessibility=False)
    return museums_toplikes[:5]


@csrf_exempt
def slash(request):
    global ACCESSIBILITY

    if request.method == 'GET':
        try:
            if(len(DDBB.Museum.objects.all()) < 1):                             # Check if DataBase is empty
                return(HttpResponseRedirect('/load'))
        except OperationalError:                                                # No DataBase at all
            exit('No Data Base. Please run manage.py migrate')

        top_museums = museums_top_likes()
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
        DISTRICT = request.POST['District']
        return(HttpResponseRedirect('/museos'))
    else:
        return(HttpResponseRedirect('/not_found'))

def add_like(museumname, username):
    try:                                                                        # If like already exists there is no need to add it again
        DDBB.Like.objects.get(museum=DDBB.Museum.objects.get(name=museumname),
                              user=DDBB.User.objects.get(username=username))
        return()
    except DDBB.Like.DoesNotExist:                                              # If it doesn't exist, exeption will raies and it will be added
        museum = DDBB.Museum.objects.get(name=museumname)
        DDBB.Like(date = timezone.now(),
                  museum=museum,
                  user=DDBB.User.objects.get(username=username)).save()
        museum.num_likes += 1
        museum.save()
        return True


@csrf_exempt
def museums_like(request):
    if request.method == 'POST':
        museum = request.POST['Museum']
        add_like(museum, request.user.username)
        return(HttpResponseRedirect('/museos'))
    else:
        return(HttpResponseRedirect('/not_found'))


def add_comment(comment, museum, username):
    DDBB.Comment(text = comment,
                 museum=museum,
                 user=DDBB.User.objects.get(username=username)).save()
    museum.save()
    return()


def get_museum_comments(id):
    try:
        return(DDBB.Comment.objects.filter(museum__id=id))
    except DDBB.Comment.DoesNotExist:
        return([])


@csrf_exempt
def museum_info(request, id):
    if request.method == 'GET':
        try:
            template = get_template('museums/museum_info.html')
        except NameError:
            exit('Server stopped working. Template missing')

        context = Context({'users': get_user_webs(),
                           'name': request.user.username,
                           'museum': DDBB.Museum.objects.get(id=id),
                           'comments': get_museum_comments(id),
                           'aut': request.user.is_authenticated()})
        return(HttpResponse(template.render(context)))

    elif request.method == 'POST':
        try:
            museum = DDBB.Museum.objects.get(name=request.POST['Museum'])
            add_comment(request.POST['Comment'], museum, request.user.username)
            return(HttpResponseRedirect(''))
        except DDBB.Museum.DoesNotExist:
            return(HttpResponseRedirect(''))                                    # Help from: https://stackoverflow.com/questions/39560175/django-redirect-to-same-page-after-post-method-using-class-based-views
    else:
        return(HttpResponseRedirect('/not_found'))


def its_valid_user(username):
    try:                                                                        # Check if user exists
        DDBB.User.objects.get(username=user)
        return True
    except DDBB.User.DoesNotExist:
        return False


def user_first(request, user):
    if its_valid_user == False:
        return(HttpResponseRedirect('/not_found'))
    return(HttpResponseRedirect('/' + user + '/1'))                             # Fist acccess to user's page. Redirected to user/1 to start with first museum views


def save_style(username, title, background, textsize):
    user = DDBB.User.objects.get(username = username)
    try:
        style = DDBB.Style.objects.get(user=user)                               # Style already existis for this user
        style.title = title
        style.text_size = textsize
        style.colour = background
        style.save()
    except DDBB.Style.DoesNotExist:
        DDBB.Style(title = title,
                   text_size=textsize,
                   colour=background,
                   user=user).save()
    return(True)


def get_navigation_links(username, numpage):
    museums_liked = DDBB.Like.objects.filter(user__username=username)
    nummuseums = museums_liked.count()                                          # Help from: https://stackoverflow.com/questions/5439901/getting-a-count-of-objects-in-a-queryset-in-django?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    if nummuseums == 0:
        return('<h3>Este usuario aún no ha seleccionado museos</h3>')

    numpages = round((nummuseums/5)-0.5)                                        # Help from: https://docs.python.org/3/library/functions.html#round
    if nummuseums%5 != 0:                                                       # Unless it is a multiple of 5 one more page should be added
        numpages += 1

    nav_links = ''
    for i in range(1, numpages+1):
        if i == numpage:
            nav_links += str(numpage)
        else:
            nav_links += PAGE_LINK.format(username, str(i), str(i))
        if i != numpages:
            nav_links += '  -  '                                                # Separator
    return(nav_links)


def get_liked_museums(user, numpage):
    museums_liked = DDBB.Like.objects.filter(user__username=user)               # This returns a 'Liked' object, with its user, date and museum
    museums_liked = museums_liked.order_by('-id')                               # Museums have to be ordered some way in order not to repeat them

    museums_in_page = []
    for i in range(5*(numpage-1), 5*numpage):
        try:
            museums_in_page.append(museums_liked[i])
        except IndexError:
            break

    return museums_in_page


@csrf_exempt
def user_page(request, user, numpage):
    if request.method == 'GET':
        if its_valid_user == False:
            return(HttpResponseRedirect('/not_found'))
        try:
            template = get_template('museums/user.html')
        except NameError:
            exit('Server stopped working. Template missing')

        itsuserspage = (user == request.user.username)
        context = Context({'aut': request.user.is_authenticated(),
                           'name': request.user.username,
                           'users': get_user_webs(),
                           'liked_museums': get_liked_museums(user, int(numpage)),
                           'title': user_title(DDBB.User.objects.get(username = user)),
                           'page_link': get_navigation_links(user, int(numpage)),
                           'user': DDBB.User.objects.get(username = user),
                           'itsuserspage': itsuserspage})
        return(HttpResponse(template.render(context)))
    elif request.method == 'POST':
        if its_valid_user == False:
            return(HttpResponseRedirect('/not_found'))
        title = request.POST['Title']
        textsize = request.POST['Textsize']
        background = request.POST['Colour']
        save_style(user, title, background, textsize)
        return(HttpResponseRedirect(''))
    else:
        return(HttpResponseRedirect('/not_found'))


def user_json(request, username):
    museums_liked = DDBB.Like.objects.filter(user__username=username)
    print(museums_liked)
    user_data = OrderedDict()
    user_data['Museos'] = []
    for like in museums_liked:
        museum_info = OrderedDict()                                             # Help from: https://stackoverflow.com/questions/10844064/items-in-json-object-are-out-of-order-using-json-dumps
        museum_info['nombre'] = like.museum.name                                # Help from: https://stackoverflow.com/questions/23110383/how-to-dynamically-build-a-json-object-with-python
        museum_info['descripcion'] = like.museum.description
        museum_info['horario'] = like.museum.open_hours
        museum_info['transporte'] = like.museum.transport
        museum_info['accesibilidad'] = like.museum.accessibility
        museum_info['web'] = like.museum.url
        museum_info['direccion'] = like.museum.address
        museum_info['barrio'] = like.museum.quarter
        museum_info['distrito'] = like.museum.district
        museum_info['telefono'] = like.museum.tlf_number
        museum_info['email'] = like.museum.email
        user_data['Museos'].append([museum_info])

    json_data = json.dumps(user_data, indent=4, sort_keys=True)                 # Help from: https://stackoverflow.com/questions/12943819/how-to-prettyprint-a-json-file
    return(HttpResponse(json_data, content_type="application/json"))            # Help from: https://stackoverflow.com/questions/8583290/sending-json-using-the-django-test-client


def style(request):
    try:
        style = DDBB.Style.objects.get(user__username = request.user.username)
        textsize = style.text_size
        backgorund = style.colour
    except DDBB.Style.DoesNotExist:
        textsize = 'medium'                                                     # Default value
        backgorund = '#FFFFFF'                                                  # Default value
    try:
        template = get_template('museums/style.css')
    except NameError:
        exit('Server stopped working. Template missing')

    context = Context({'fontsize': textsize,
                       'backgorund': backgorund})
    return(HttpResponse(template.render(context), content_type='text/css'))


def about(request):
        try:
            template = get_template('museums/about.html')
        except NameError:
            exit('Server stopped working. Template missing')

        context = Context({'users': get_user_webs(),
                           'name': request.user.username,
                           'aut': request.user.is_authenticated()})
        return(HttpResponse(template.render(context)))


def not_found(request):
    try:
        template = get_template('museums/not_found.html')
    except NameError:
        exit('Server stopped working. Template missing')
    context = Context({'aut': request.user.is_authenticated(),
                       'name': request.user.username,
                       'users': get_user_webs()})
    return(HttpResponse(template.render(context)))
