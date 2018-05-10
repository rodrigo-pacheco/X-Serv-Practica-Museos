#  Rodrigo Pacheco
#  Servicios y Aplicaciones Telemáticas. Universidad Rey Juan Carlos
#  r.pachecom at alumnos dot urjc dot com

#  This program parses information from XML document at
#  https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full
#  to the database created in models.py

# Documentation obtained from https://docs.python.org/2/library/xml.etree.elementtree.html
# Specially from chapter 19.7.1.6. Parsing XML with Namespaces


import xml.etree.ElementTree as ET
import sys
from urllib import request

# After trying to run this program and botaining this exception:
# django.core.exceptions.ImproperlyConfigured: Requested setting DEFAULT_INDEX_TABLESPACE, but settings are not configured. You must either define
# the environment variable DJANGO_SETTINGS_MODULE or call settings.configure() before accessing settings.
# I found this help to solve it here: https://stackoverflow.com/questions/8047204/django-script-to-access-model-objects-without-using-manage-py-shell
# and here: https://stackoverflow.com/questions/15048963/alternative-to-the-deprecated-setup-environ-for-one-off-django-scripts

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

from models import Museum


def get_location_info(location):
    address, quarter, district = '', '', ''
    try:
        address =  location.find('atributos/atributo[@nombre="CLASE-VIAL"]').text    + ' '
        address += location.find('atributos/atributo[@nombre="NOMBRE-VIA"]').text    + ', '
        address += location.find('atributos/atributo[@nombre="NUM"]').text           + '. CP:  '
        address += location.find('atributos/atributo[@nombre="CODIGO-POSTAL"]').text + ' '
        address += location.find('atributos/atributo[@nombre="LOCALIDAD"]').text
        quarter = location.find('atributos/atributo[@nombre="BARRIO"]').text
        district = location.find('atributos/atributo[@nombre="DISTRITO"]').text
    except AttributeError:
        print('Location could not be completed for ' + address + '/' + quarter + '/' + district)
        return address, quarter, district

    return address, quarter, district


def get_contact_info(contact):
    email, telephone = '', ''
    try:
        email = contact.find('atributos/atributo[@nombre="BARRIO"]').text
        telephone = contact.find('atributos/atributo[@nombre="DISTRITO"]').text
    except AttributeError:
        print('Email or phone could not be completed for ' + email + '/' + telephone)
        return email, telephone

    return email, telephone


def parse_and_store(source, itsurl):
    if itsurl:
        try:
            tree = ET.parse(request.urlopen(sys.argv[1]))
        except ValueError:
            exit('Could not parse URL')
        except ET.ParseError:
            exit(' Could not parse. \n Does not seem to be a proper XLM')
    else:
        try:
            tree = ET.parse(str(source))
        except FileNotFoundError:
            exit('Could not parse document')
        except xml.etree.ElementTree.ParseError:
            exti(' Could not parse. \n Does not seem to be a proper XLM')


    root = tree.getroot()
    for museum in root.iter('contenido'):
        try:
            nombre = museum.find('atributos/atributo[@nombre="NOMBRE"]').text
            descripcion = museum.find('atributos/atributo[@nombre="DESCRIPCION-ENTIDAD"]').text
            horario = museum.find('atributos/atributo[@nombre="HORARIO"]').text
            transporte = museum.find('atributos/atributo[@nombre="TRANSPORTE"]').text
            accesibilidad = museum.find('atributos/atributo[@nombre="ACCESIBILIDAD"]').text
            if accesibilidad == 1:
                accesibilidad = True
            else:
                accesibilidad = False
            web = museum.find('atributos/atributo[@nombre="CONTENT-URL"]').text
            location = museum.find('atributos/atributo[@nombre="LOCALIZACION"]').text
            direccion, barrio, distrito = get_location_info(location)
            contact = museum.find('atributos/atributo[@nombre="DATOSCONTACTOS"]').text
            email, telefono = get_contact_info(contact)
        except AttributeError:
            print('Could not parse ' + nombre)
            continue

        museum = Museum(name = nombre,
                        description = descripcion,
                        open_hours = horario,
                        transport = transporte,
                        accessibility = accesibilidad,
                        url = web,
                        address = direccion,
                        quarter = barrio,
                        district = distrito,
                        tlf_number = telefono,
                        email = email)
        museum.save()

if __name__ == '__main__':
    source = sys.argv[1]
    parse_and_store(source, 0)
