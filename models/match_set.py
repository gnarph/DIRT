from models.match import Match


class MatchSet(object):

    def __init__(self, matches):
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
        print matches
        return MatchSet(matches)

    # Temporary hack method for gui
    def get_file_names(self):
        """
        :return: file name a, file name b
        Could use document_factory to make them into documents to
        get metadata etc.
        """
        match = self.matches[0]
        a = match.alpha
        b = match.beta
        return a.file_name, b.file_name

    # Temporary hack method for gui
    def get_indices(self):
        """
        :return: list of tuple of tuple
        [(PAIR), (PAIR), ...]
        PAIR=((a_lower, a_upper), (b_lower, b_upper))
        """
        indices = []
        for match in self.matches:
            a = match.alpha
            b = match.beta
            a_indices = a.get_match_bounds(a.document.body)
            b_indices = b.get_match_bounds(b.document.body)
            i = (a_indices, b_indices)
            indices.append(i)
        return indices