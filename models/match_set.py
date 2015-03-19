from operator import attrgetter

from models.match import Match
from models.document import Document


class MatchSet(object):
    """
    Represents a set of matches between two documents
    Also contains some metadata
    """

    def __init__(self, alpha_doc, beta_doc, matches):
        self.alpha_doc = alpha_doc
        self.beta_doc = beta_doc
        self.matches = set(matches)
        self._lmatches = None

    def __eq__(self, other):
        return self.matches == other.matches

    def __len__(self):
        return len(self.matches)

    def __getitem__(self, item):
        if self._lmatches is None:
            g = attrgetter('alpha_indices')
            self._lmatches = tuple(sorted(self.matches, key=g))
        return self._lmatches[item]

    def __iter__(self):
        return iter(self.matches)

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
    def from_dict(d):
        """
        Convert dict representation to MatchSet
        :param d: dict representation of a MatchSet
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
        percentage_a = round((match_len_a/len_a) * 100, 1)
        percentage_b = round((match_len_b/len_b) * 100, 1)
        return percentage_a, percentage_b

    def get_match_count(self):
        """
        Return total number of matches
        could just use len() instead
        """
        return len(self.matches)

    def all_passages(self):
        """
        Return set of all passages
        """
        passages = set()
        for match in self.matches:
            passages.add(match.alpha_passage)
            passages.add(match.beta_passage)
        return passages

    def alpha_passages(self):
        """
        Get a list of matches in the alpha document
        """
        return [m.alpha_passage for m in self.matches]

    def beta_passages(self):
        """
        Get a list of matches in the beta document
        """
        return [m.beta_passage for m in self.matches]

    def swap_alpha_beta(self):
        """
        Swap alpha and beta
        """
        docs = self.alpha_doc, self.beta_doc
        self.beta_doc, self.alpha_doc = docs

        for match in self.matches:
            match.swap_alpha_beta()

        self._lmatches = None

    def _get_meta(self, doc):
        """
        Get metadata from a document
        """
        meta = doc.get_metadata()
        meta['match_count'] = self.get_match_count()
        meta['file_name'] = doc.file_name
        alpha_pct, beta_pct = self.get_match_percentage()
        meta['alpha_match_pct'] = alpha_pct
        meta['beta_match_pct'] = beta_pct
        return meta

    def get_alpha_metadata(self):
        """
        Passthrough to get metadata
        """
        return self._get_meta(self.alpha_doc)

    def get_beta_metadata(self):
        """
        Passthrough to get metadata
        """
        return self._get_meta(self.beta_doc)
