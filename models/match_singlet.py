from models.document import Document


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
        if self._document is None:
            self._document = Document.from_file(self.file_name)
        return self._document

    def to_dict(self):
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
        upper_bound = desired_upper
        if desired_upper < len_passage:
            upper_bound = len_passage - 1
        return body[lower_bound:upper_bound]
