from models.match import Match
from models.document import Document
from utilities import file_ops


class MatchSet(object):
    """
    Represents a set of matches between two documents
    Also contains some metadata
    """

    def __init__(self, alpha_doc, beta_doc, matches):
        self.alpha_doc = alpha_doc
        self.beta_doc = beta_doc
        self.matches = matches

    def __eq__(self, other):
        return self.matches == other.matches

    def to_dict(self):
        """
        Covert MatchSet to dictionary representation
        :return: dict representation of MatchSet
        """
        # Need document json name
        return {'alpha_doc': self.alpha_doc.file_name,
                'beta_doc': self.beta_doc.file_name,
                'matches': [match.to_dict() for match in self.matches],
                }

    @staticmethod
    def from_json(filename):
        json = file_ops.read_json_utf8(filename)
        return MatchSet.from_dict(json)

    @staticmethod
    def from_dict(d):
        """
        Convert dict representation to MatchSet
        :param d: dict representaton of a MatchSet
        :return: MatchSet
        """
        matches = [Match.from_dict(m) for m in d['matches']]
        alpha = Document.from_json(d['alpha_doc'])
        beta = Document.from_json(d['beta_doc'])
        return MatchSet(alpha_doc=alpha,
                        beta_doc=beta,
                        matches=matches)

    def get_file_names(self):
        """
        :return: file name a, file name b
        Could use document_factory to make them into documents to
        get metadata etc.
        """
        alpha_name = self.alpha_doc.file_name
        beta_name = self.beta_doc.file_name
        return alpha_name, beta_name

    def get_indices(self):
        """
        :return: list of tuple of tuple
        [(PAIR), (PAIR), ...]
        PAIR=((a_lower, a_upper), (b_lower, b_upper))
        """
        # TODO: consider a class instead of the odd data structure
        indices = []
        for match in self.matches:
            index_pair = match.alpha_indices, match.beta_indices
            indices.append(index_pair)
        return indices

    def get_match_percentage(self):
        """
        Return what percentage of each document is a match with
        the other, roughly
        :return: a's similarity, b's similarity
        """
        match_len_a = 0.0
        match_len_b = 0.0
        len_a = len(self.alpha_doc.pre_body)
        len_b = len(self.beta_doc.pre_body)
        for match in self.matches:
            a = match.alpha_indices[1] - match.alpha_indices[0]
            match_len_a += a
            b = match.beta_indices[1] - match.beta_indices[0]
            match_len_b += b
        percentage_a = (match_len_a/len_a) * 100
        percentage_b = (match_len_b/len_b) * 100
        return percentage_a, percentage_b

    def all_passages(self):
        """
        Return set of all passages
        """
        passages = set()
        for match in self.matches:
            passages.add(match.alpha_passage)
            passages.add(match.beta_passage)
        return passages


