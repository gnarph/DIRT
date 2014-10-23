from lxml import etree

import tei_document

TAG_HEADER = 'teiHeader'
TAG_FILE_DESC = 'fileDesc'
TAG_TITLE_STATEMENT = 'titleStmt'
TAG_TITLE = 'title'
TAG_PRINCIPAL = 'principal'
TAG_EDITION_STATEMENT = 'editionStmt'
TAG_PUB_STATEMENT = 'publicationStmt'
TAG_DATE = 'date'
TAG_DISTRIBUTOR = 'distributor'
TAG_LICENSE = 'availability'
TAG_TEXT = 'text'
TAG_FRONT = 'front'
TAG_BODY = 'body'


class TEIReader(object):

    query_template = '//{namespace}tag'

    def __init__(self, file_name):
        self.file_name = file_name

    def parse(self):
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(self.file_name, parser=parser)
        root = tree.getroot()
        root_tag = root.tag
        ns_index = root_tag.rfind('}') + 1
        namespace = root_tag[:ns_index]

        doc = tei_document.TEIDocument(tree, namespace)

        header = etree.find(TAG_HEADER)
        file_desc = header.find(TAG_FILE_DESC)
        title = file_desc.find(TAG_TITLE)
        principal = file_desc.find(TAG_PRINCIPAL)
        edition = file_desc.find(TAG_EDITION_STATEMENT)
        publication = file_desc.find(TAG_PUB_STATEMENT)
        date = publication.find(TAG_DATE)
        availability = file_desc.find(TAG_LICENSE)
        text = doc.find(TAG_TEXT)
        front = text.find(TAG_FRONT)
        body = text.find(TAG_BODY)

