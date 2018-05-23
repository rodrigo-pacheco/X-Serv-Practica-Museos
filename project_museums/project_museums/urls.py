#  Rodrigo Pacheco
#  Servicios y Aplicaciones Telemáticas. Universidad Rey Juan Carlos
#  r.pachecom at alumnos dot urjc dot com


"""project_museums URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'museums.views.slash'),
    url(r'^load$', 'museums.views.load_DDBB'),
    url(r'^login', 'museums.views.my_login'),
    url(r'^logout', logout, {'next_page': '/'}),                                # Help from: https://stackoverflow.com/questions/5315100/how-to-configure-where-to-redirect-after-a-log-out-in-django
    url(r'^museos$', 'museums.views.museums'),
    url(r'^museos/(\d+)', 'museums.views.museum_info'),
    url(r'^about$', 'museums.views.about'),
    url(r'.*', 'museums.views.not_found'),
]
