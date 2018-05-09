#  Rodrigo Pacheco
#  Servicios y Aplicaciones Telemáticas. Universidad Rey Juan Carlos
#  r.pachecom at alumnos dot urjc dot com

#  This program parses information from XML document at
#  https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full
#  to the database created in models.py


import xml.etree.ElementTree as ET
import sys
from urllib import request


def ParseAndStore(source, itsurl):
    if itsurl:
        try:
            xmlFile = request.urlopen(sys.argv[1])
        except:
            print('Could not parse URL')
    else:
        try:
            xmlfile = open(str(source), 'r')
        except FileNotFoundError:
            print('Could not parse document')

    

if __name__ == '__main__':
    source = sys.argv[1]
    ParseAndStore(source, True)
