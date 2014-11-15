from models.match import Match
from models.document import Document


class MatchSet(object):

    def __init__(self, alpha_doc, beta_doc, matches):
        self.alpha_doc = alpha_doc
        self.beta_doc = beta_doc
        self.matches = matches
        # TODO: add more data at this level,
        # move it from match singlet

    def __eq__(self, other):
        return self.matches == other.matches

    def to_dict(self):
        # Need document json name
        return {'alpha_doc': self.alpha_doc.file_name,
                'beta_doc': self.beta_doc.file_name,
                'matches': [match.to_dict() for match in self.matches],
                }

    @staticmethod
    def from_dict(d):
        matches = [Match.from_dict(m) for m in d['matches']]
        alpha = Document.from_json(d['alpha_doc'])
        beta = Document.from_json(d['beta_doc'])
        return MatchSet(alpha_doc=alpha,
                        beta_doc=beta,
                        matches=matches)