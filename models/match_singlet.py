class MatchSinglet(object):
    """
    Class for representing half of a match,
    and for getting information about them
    """
    # TODO: rename class

    def __init__(self, passage):
        """
        :param passage: matching passage, non-preprocessed
        """
        self.passage = passage

    def __eq__(self, other):
        return self.passage == other.passage

    def to_dict(self):
        """
        Convert to dictionary representation
        :return: dict representation of MatchSinglet
        """
        return {'passage': self.passage,
                }

    @staticmethod
    def from_dict(d):
        return MatchSinglet(d['passage'])

    def get_match_bounds(self, body):
        """
        Get the lower and upper indices that bound the match
        :param body: text body the indices should reference
        :return: lower index, upper index
        """
        start = body.index(self.passage)
        end = start + len(self.passage)
        return start, end

    def get_context(self, body, context_chars=10):
        """
        Get matching passage with some context from surrounding text
        :param body: text body to get the match from,
                     must contain self.passage
        :param context_chars: number of chars added to each side of
                              passage to make context
        :return: string of matching passage and surrounding context
        """
        # TODO: test when self.passage not in body?
        loc, top = self.get_match_bounds(body)
        desired_lower = loc - context_chars
        desired_upper = top + context_chars
        lower_bound = desired_lower if desired_lower >= 0 else 0
        len_body = len(body)
        if desired_upper >= len_body:
            upper_bound = len_body
        else:
            upper_bound = desired_upper
        context = body[lower_bound:upper_bound]
        return context
