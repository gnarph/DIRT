class MatchHalf(object):
    """
    Class for representing half of a match,
    and for getting information about them
    """

    def __init__(self, passage):
        """
        :param passage: matching passage, non-preprocessed
        """
        self.passage = passage

    def __eq__(self, other):
        return self.passage == other.passage

    def get_match_bounds(self, body):
        """
        Get the lower and upper indices that bound the match
        :param body: text body the indices should reference
        :return: lower index, upper index
        """
        start = body.index(self.passage)
        end = start + len(self.passage)
        return start, end
