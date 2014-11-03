import difflib

import processing.comparators.base_comparator as base_comparator
from models.match_singlet import MatchSinglet
from models.match import Match
from utilities.iteration import niter


CLASS_NAME = 'SimpleComparator'


def double_iter(iterable):
    return niter(iterable, 2)


class Comparator(base_comparator.BaseComparator):

    def get_singlet_pairs(self, passage_blocks):
        singlet_pairs = []
        for p_a, p_b in passage_blocks:
            s_a = MatchSinglet(file_name=self.a,
                               passage=p_a)
            s_b = MatchSinglet(file_name=self.b,
                               passage=p_b)
            singlet_pairs.append((s_a, s_b))
        return singlet_pairs

    def get_matches(self, passage_blocks):
        singlet_pairs = self.get_singlet_pairs(passage_blocks)
        matches = []
        for s_a, s_b in singlet_pairs:
            match = Match(s_a, s_b)
            matches.append(match)
        return matches

    def compare(self):
        matcher = difflib.SequenceMatcher(a=self.a,
                                          b=self.b)
        matching_blocks = matcher.get_matching_blocks()
        # Last block is a dummy
        combined_blocks = self._combine_blocks(matching_blocks[:-1])
        filtered_blocks = self._filter_blocks(combined_blocks)
        passage_blocks = self._tuples_to_passages(filtered_blocks)

        matches = self.get_matches(passage_blocks)
        return matches

    def _combine_blocks(self, matching_blocks):
        """
        :param matching_blocks: list of tuples (i, j, n)
        """
        # this just combines nearby blocks in alpha
        combined_blocks = []
        i = 0
        j = 1
        end = None
        while j < len(matching_blocks):
            first = matching_blocks[i]
            if end is None:
                end = first[0] + first[2]
            second = matching_blocks[j]
            second_start = second[0]
            if second_start - end < self.gap_length:
                # Block continues
                j += 1
            elif i != j:
                # Block terminates
                new_length = end - first[0]
                new_match = (first[0], first[1], new_length)
                print new_match
                combined_blocks.append(new_match)
                i = j
            else:
                # No change to block
                combined_blocks.append(first)
                j += 1
                i = j
            end = second_start + second[2]
        return combined_blocks

    def _filter_blocks(self, combined_blocks):
        """
        Filter match blocks based on length
        """
        return [tup for tup in combined_blocks if tup[2] > self.match_length]

    def _tuples_to_passages(self, filtered_blocks):
        passages = []
        for tup in filtered_blocks:
            a = self.a[tup[0]:tup[0]+tup[2]]
            b = self.a[tup[1]:tup[1]+tup[2]]
            passages.append((a, b))
        return passages
