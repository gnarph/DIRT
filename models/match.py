class Match(object):
    """
    Class for representing a single matching passage
    """

    def __init__(self, alpha_passage, alpha_indices,
                 beta_passage, beta_indices):
        """
        :param alpha_passage: string
        :param alpha_indices: tuple
        :param beta_passage: string
        :param beta_indices: tuple
        """
        self.alpha_passage = alpha_passage
        self.alpha_indices = tuple(alpha_indices)
        self.beta_passage = beta_passage
        self.beta_indices = tuple(beta_indices)

    def __eq__(self, other):
        if self.alpha_passage == other.alpha_passage:
            if self.beta_passage == other.beta_passage:
                if self.alpha_indices == other.alpha_indices:
                    return self.beta_indices == other.beta_indices
        elif self.alpha_passage == other.beta_passage:
            if self.beta_passage == other.alpha_passage:
                if self.alpha_indices == other.beta_indices:
                    return self.beta_indices == other.alpha_indices
        return False

    def __hash__(self):
        a_hash = hash(self.alpha_passage) + hash(self.alpha_indices)
        b_hash = hash(self.beta_passage) + hash(self.beta_indices)
        return hash(a_hash * b_hash)

    def to_dict(self):
        """
        Convert match to dictionary representation
        """
        return {'alpha_passage': self.alpha_passage,
                'alpha_indices': self.alpha_indices,
                'beta_passage': self.beta_passage,
                'beta_indices': self.beta_indices,
                }

    @staticmethod
    def from_dict(d):
        return Match(alpha_passage=d['alpha_passage'],
                     alpha_indices=d['alpha_indices'],
                     beta_passage=d['beta_passage'],
                     beta_indices=d['beta_indices'])

    def swap_alpha_beta(self):
        """
        Swap alpha and beta docs, as we want alpha as the focus
        """
        indices = self.alpha_indices, self.beta_indices
        self.beta_indices, self.alpha_indices = indices

        passes = self.alpha_passage, self.beta_passage
        self.beta_passage, self.alpha_passage = passes
