__author__ = 'micah'

import pickle
import json
import xml.etree.ElementTree as ET
import csv
from datetime import datetime
from pymongo import MongoClient

MONGO_URL = 'mongodb://codeguild2:pleese-keep-secret@dharma.mongohq.com:10023/qscfadm'


class PickleFileSerializer(object):
    def __init__(self):
        self.type = "pickle"

    def save(self, object_container):
        with open('saved_list.pl', 'wb') as fh:
            pickle.dump(object_container, fh)

    def open(self):
        with open('saved_list.pl', 'rb') as fh:
            retrieved_data = pickle.load(fh)
            return retrieved_data


class JSONFileSerializer(object):
    def __init__(self):
        self.type = "json"

    def sanitize_objects(self, object_container):
        for entry in object_container:
            entry.due_date = entry.due_date.isoformat()
        return object_container

    def convert_date(self, object_container):
        for entry in object_container:
            entry['due_date'] = entry['due_date'].replace('-', '/')
            entry["due_date"] = datetime.strptime(entry['due_date'], '%Y/%m/%d').date()

        return object_container

    def save(self, object_container):
        with open('saved_list.js', 'w') as fh:
            json.dump([item.serialize() for item in object_container], fh)

    def open(self):
        with open('saved_list.js') as fh:
            retrieved_data = json.load(fh)
            retrieved_data = self.convert_date(retrieved_data)
            return retrieved_data


class XMLFileSerializer(object):
    def __init__(self):
        self.type = "xml"

    def convert_to_xml(self, object_container):

        xmltree = ET.Element('TodoItems')
        for todo_dict in object_container:
            task_object = ET.SubElement(xmltree, "Item")
            for key, value in vars(todo_dict).items():
                child = ET.Element(key)
                child.text = str(value)
                task_object.append(child)

        return xmltree

    def save(self, object_container):

        xml_object = ET.ElementTree(self.convert_to_xml(object_container))
        xml_object.write('saved_list.xml')


class CSVFileSerializer(object):
    def __init__(self):
        self.type = "csv"

    def save(self, object_container):
        with open('saved_list.csv', 'w') as fh:
            object_writer = csv.DictWriter(fh, vars(object_container[0]).keys())
            object_writer.writeheader()
            for todo_dict in object_container:
                object_writer.writerow(vars(todo_dict))


class CloudStorageSerializer(object):

    def __init__(self):
        self._collectionName = 'micah_todolist'
        self.type = 'cloud'

    def _connect(self):
        self._mongo_client = MongoClient(MONGO_URL)
        self._mongo_db = self._mongo_client.qscfadm

    def save(self, todolist):
        self._connect()

        self._mongo_db[self._collectionName].remove({})

        self._mongo_db[self._collectionName].insert_many([vars(itm) for itm in todolist])

    def open(self):

        self._connect()
        return list(self._mongo_db[self._collectionName].find({}))





