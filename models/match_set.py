from models.match import Match


class MatchSet(object):

    def __init__(self, matches):
        self.matches = matches

    def to_dict(self):
        return {'matches': [match.to_dict() for match in self.matches],
                }

    @staticmethod
    def from_dict(d):
        matches = [Match.from_dict(m) for m in d['matches']]
        return MatchSet(matches)