from models.match_singlet import MatchSinglet


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

    @staticmethod
    def from_dict(d):
        a = MatchSinglet.from_dict(d['alpha'])
        b = MatchSinglet.from_dict(d['beta'])
        return Match(alpha=a,
                     beta=b)
