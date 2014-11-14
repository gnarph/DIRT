from models.match import Match


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
        return {'matches': [match.to_dict() for match in self.matches],
                }

    @staticmethod
    def from_dict(d):
        matches = [Match.from_dict(m) for m in d['matches']]
        return MatchSet(matches)