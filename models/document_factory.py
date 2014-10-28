import codecs

import cjson

from models.document import Document
from preprocessing.tei.reader import TEIReader


def from_file(file_name):
    lowered_file_name = file_name.lower()
    if 'tei' in lowered_file_name:
        creator = from_tei
    elif 'json' in lowered_file_name:
        creator = from_json
    else:
        creator = from_txt
    return creator(file_name)


def from_txt(file_name):
    with codecs.open(file_name, encoding='UTF-8') as f:
        body = f.read()
    return Document(file_name, body)


def from_tei(file_name):
    reader = TEIReader(file_name)
    return reader.read()


def from_json(file_name):
    with codecs.open(file_name, encoding='UTF-8') as f:
        raw_json = f.read()
    data = cjson.decode(raw_json)
    return Document(file_name=data['file_name'],
                    body=data['body'],
                    metadata=data['metadata'])
