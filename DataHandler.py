import json
import dicttoxml
from xml.dom.minidom import parseString
from abc import ABC, abstractmethod 


class DataHandler(ABC):
    @abstractmethod
    def write(self, data, filename):
        pass


class JSONHandler(DataHandler):
    def write(self, data, filename):
        with open(filename, 'w') as f:
           f.write(json.dumps(data, indent=4))


class XMLHandler(DataHandler):
    def write(self, data, filename):
        xml = dicttoxml.dicttoxml(data, custom_root='rooms', attr_type=False)
        pretty_xml = parseString(xml).toprettyxml()
        with open (filename,'w' ) as f:
            f.write(pretty_xml)

    