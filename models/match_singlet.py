import models.document_factory as document_factory


class MatchSinglet(object):
    """
    Class for representing half of a match
    """

    def __init__(self, file_name, passage, document=None):
        """
        :param file_name: name of source file
        :param passage: matching passage, non-preprocessed
        :param document: models.document.Document, optional
        """
        self.file_name = file_name
        self.passage = passage
        self._document = document

    @property
    def document(self):
        # TODO: consider searching JSON model over tei/txt,
        # probably want preprocessed doc
        if self._document is None:
            self._document = document_factory.from_file(self.file_name)
        return self._document

    def to_dict(self):
        """
        Convert to dictionary representation
        :return: dict representation of MatchSinglet
        """
        return {'file_name': self.file_name,
                'passage': self.passage,
                }

    def get_context(self, context_chars=10):
        """
        Get matching passage with some context from surrounding text
        :param context_chars: number of chars added to each side of
                              passage to make context
        :return: string of matching passage and surrounding context
        """
        body = self.document.body
        loc = body.index(self.passage)
        desired_lower = loc - context_chars
        len_passage = len(self.passage)
        desired_upper = loc + len_passage + context_chars
        lower_bound = desired_lower if desired_lower >= 0 else 0
        len_body = len(body)
        if desired_upper >= len_body:
            upper_bound = len_body
        else:
            upper_bound = desired_upper
        return body[lower_bound:upper_bound]
