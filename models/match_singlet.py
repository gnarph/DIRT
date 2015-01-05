from models.document import Document
from utilities import fuzzer


class MatchSinglet(object):
    """
    Class for representing half of a match,
    and for getting information about them
    """
    # TODO: rename class

    def __init__(self, file_name, passage, document=None):
        """
        :param file_name: name of source file
        :param passage: matching passage, non-preprocessed
        :param document: models.document.Document, optional
        """
        self.file_name = file_name
        self.passage = passage
        self._document = document

    def __eq__(self, other):
        if self.file_name != other.file_name:
            return False
        return self.passage == other.passage

    @property
    def document(self):
        """
        Plain input document... need to get context from it
        :return:
        """
        if self._document is None:
            return Document.from_json(self.file_name)
        return self._document

    def to_dict(self):
        """
        Convert to dictionary representation
        :return: dict representation of MatchSinglet
        """
        return {'file_name': self.file_name,
                'passage': self.passage,
                }

    @staticmethod
    def from_dict(d):
        return MatchSinglet(d['file_name'],
                            d['passage'])

    def get_match_bounds(self, body):
        """
        Get the lower and upper indices that bound the match
        :param body: text body the indices should reference
        :return: lower index, upper index
        """
        start = body.index(self.passage)
        end = start + len(self.passage)
        return start, end

    def get_context(self, from_doc=None, context_chars=10):
        """
        Get matching passage with some context from surrounding text
        :param from_doc: document the context should come from
        :param context_chars: number of chars added to each side of
                              passage to make context
        :return: string of matching passage and surrounding context
        """
        if from_doc is None:
            from_doc = self.document
        loc, top = self.get_match_bounds(from_doc.body)
        desired_lower = loc - context_chars
        desired_upper = top + context_chars
        lower_bound = desired_lower if desired_lower >= 0 else 0
        len_body = len(from_doc.body)
        if desired_upper >= len_body:
            upper_bound = len_body
        else:
            upper_bound = desired_upper
        context = from_doc.body[lower_bound:upper_bound]
        return context
