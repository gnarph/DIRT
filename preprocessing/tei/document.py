from lxml import etree

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


class TEIDocument(object):
    """
    Class used to represent a TEI encoded xml file
    """

    query_template = '//{namespace}{tag}'
    no_tag_error_template = 'Could not find <{tag}>'

    def __init__(self, file_name):
        """
        :param file_name: file name
        """
        self.file_name = file_name
        self.namespace = ''
        self.tree = None

    def _setup_parse_tree(self):
        """
        Parse the file, set self.tree and self.namespace
        """
        parser = etree.XMLParser(remove_blank_text=True)
        self.tree = etree.parse(self.file_name, parser=parser)
        root = self.tree.getroot()
        root_tag = root.tag
        ns_index = root_tag.rfind('}') + 1
        self.namespace = root_tag[:ns_index]

    def _get_body(self):
        """
        Get document body
        :return: body of the tei document (no tags)
        """
        raw_body = self._get_element_text(TAG_BODY)
        stripped_body = ' '.join(raw_body.split())
        return stripped_body

    def get_data(self):
        """
        Get document body and metadata
        :return: dictionary of data
        """
        self._setup_parse_tree()

        stripped_body = self._get_body()
        # TODO: consider making this it's own class
        return {'title': self._get_element_text(TAG_TITLE),
                'edition': self._get_element_text(TAG_EDITION_STATEMENT),
                'date': self._get_element_text(TAG_DATE),
                'availability': self._get_element_text(TAG_LICENSE),
                'body': stripped_body,
                }

    def _get_element_text(self, tag):
        """
        Get text from element in document
        :param tag: name of tag
        :return: text within tag
        """
        element = self._get_element(tag)
        if element is not None:
            return element.xpath('string()')
        else:
            # TODO: log a warning instead
            return self.no_tag_error_template.format(tag=tag)

    def _get_element(self, tag):
        """
        Get a single element from the xml document
        :param tag: tag of the element in the document
        :return: element node
        """
        query = self._get_tag_query(tag)
        return self.tree.find(query)

    def _get_tag_query(self, tag):
        """
        Get xpath query for tag
        """
        return self.query_template.format(namespace=self.namespace,
                                          tag=tag)
