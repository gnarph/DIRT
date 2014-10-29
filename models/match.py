

class Match(object):
    """
    Class for representing matches
    """

    def __init__(self, alpha, beta):
        """
        :param alpha: MatchSinglet
        :param beta: MatchSinglet
        """
        self.alpha = alpha
        self.beta = beta

    def to_dict(self):
        """
        Convert match to dictionary representation
        """
        return {'alpha': self.alpha.to_dict(),
                'beta': self.beta.to_dict(),
                }
