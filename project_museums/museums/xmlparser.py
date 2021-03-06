#  Rodrigo Pacheco
#  Servicios y Aplicaciones Telemáticas. Universidad Rey Juan Carlos
#  r.pachecom at alumnos dot urjc dot com

#  This program parses information from XML document at
#  https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full
#  to the database created in models.py

# Documentation obtained from https://docs.python.org/2/library/xml.etree.elementtree.html
# Specially from chapter 19.7.1.6. Parsing XML with Namespaces


import xml.etree.ElementTree as ET
from urllib import request


import time


def get_location_info(location):
    address, quarter, district = '', '', ''
    try:
        address =  location.find('atributo[@nombre="CLASE-VIAL"]').text    + ' '
        address += location.find('atributo[@nombre="NOMBRE-VIA"]').text    + ', '
        address += location.find('atributo[@nombre="NUM"]').text           + '. CP:  '
        address += location.find('atributo[@nombre="CODIGO-POSTAL"]').text + ' '
        address += location.find('atributo[@nombre="LOCALIDAD"]').text
    except AttributeError:
        print('One of the filds for address could not be completed')
        pass

    try:
        quarter = location.find('atributo[@nombre="BARRIO"]').text
    except AttributeError:
        print('Quarter information could not be filled')
        pass

    try:
        district = location.find('atributo[@nombre="DISTRITO"]').text
    except AttributeError:
        print('District information could not be filled')
        pass

    return address, quarter, district


def get_contact_info(contact):
    email, telephone = '', ''
    try:
        email = contact.find('atributo[@nombre="EMAIL"]').text
        telephone = contact.find('atributo[@nombre="TELEFONO"]').text
    except AttributeError:
        print('Email or phone could not be completed for ' + email + '/' + telephone)
        return email, telephone

    return email, telephone


def parse_to_matrix(source, itsurl):
    if itsurl:
        try:
            tree = ET.parse(request.urlopen(source))
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

    matrix = []                                                             # Eahc raw will contain information corresponding to one museum
    root = tree.getroot()
    for museum in root.iter('contenido'):
        try:
            nombre = museum.find('atributos/atributo[@nombre="NOMBRE"]').text
            descripcion = museum.find('atributos/atributo[@nombre="DESCRIPCION-ENTIDAD"]').text
            horario = museum.find('atributos/atributo[@nombre="HORARIO"]').text
            transporte = museum.find('atributos/atributo[@nombre="TRANSPORTE"]').text
            accesibilidad = museum.find('atributos/atributo[@nombre="ACCESIBILIDAD"]').text
            if int(accesibilidad) == 1:
                accesibilidad = True
            else:
                accesibilidad = False
            web = museum.find('atributos/atributo[@nombre="CONTENT-URL"]').text
            location = museum.find('atributos/atributo[@nombre="LOCALIZACION"]')
            direccion, barrio, distrito = get_location_info(location)
            contact = museum.find('atributos/atributo[@nombre="DATOSCONTACTOS"]')
            email, telefono = get_contact_info(contact)
        except AttributeError:
            print('Could not parse ' + nombre)
            continue

        matrix.append([nombre, descripcion, horario, transporte, accesibilidad, web, direccion, barrio, distrito, telefono, email])

    return matrix

if __name__ == '__main__':
    source = sys.argv[1]
    parse_to_matrix(source, 0)
