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
            separador = ' - '
            print(nombre, separador, descripcion, separador, horario, separador, transporte)
        except AttributeError:
            print('Could not parse ' + nombre)
            continue
        # nombre = museum.find('{nombre}nombre')
        # print(name.text)
        # for char in actor.findall('{http://characters.example.com}character'):
        #     print ' |-->', char.text

if __name__ == '__main__':
    source = sys.argv[1]
    ParseAndStore(source, 0)
