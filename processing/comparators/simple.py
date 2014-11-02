import difflib

import processing.comparators.base_comparator as base_comparator
from models.match_singlet import MatchSinglet
from models.match import Match
from utilities.iteration import niter


CLASS_NAME = 'SimpleComparator'


def double_iter(iterable):
    return niter(iterable, 2)


class Comparator(base_comparator.BaseComparator):
    def compare(self):
        matcher = difflib.SequenceMatcher(a=self.file_name_a, b=self.file_name_a)
        matching_blocks = matcher.get_matching_blocks()
        combined_blocks = self._combine_blocks(matching_blocks)
        filtered_blocks = self._filter_blocks(combined_blocks)
        passage_blocks = self._tuples_to_passages(filtered_blocks)

        singlet_pairs = []
        for p_a, p_b in passage_blocks:
            s_a = MatchSinglet(file_name=self.file_name_a,
                               passage=p_a)
            s_b = MatchSinglet(file_name=self.file_name_b,
                               passage=p_b)
            singlet_pairs.append((s_a, s_b))
        matches = []
        for s_a, s_b in singlet_pairs:
            match = Match(s_a, s_b)
            matches.append(match)
        return matches

    def _combine_blocks(self, matching_blocks):
        """
        :param matching_blocks: list of tuples (i, j, n)
        """
        # this just combines nearby blocks in alpha
        combined_blocks = []
        i = 0
        j = 1
        while j < len(matching_blocks):
            first = matching_blocks[i]
            first_end = first[0] + first[2]
            second = matching_blocks[j]
            second_start = second[0]
            if second_start - first_end < self.gap_length:
                # Block continues
                j += 1
            elif i != j:
                # Block terminates
                new_length = end - second_start
                new_match = (first[0], first[1], new_length)
                combined_blocks.append(new_match)
                i = j
            else:
                # No change to block
                combined_blocks.append(first)
                j += 1
                i = j
            end = second_start + second[2]

    def _filter_blocks(self, combined_blocks):
        """
        Filter match blocks based on length
        """
        return [tup for tup in combined_blocks if tup[2] > self.match_length]

    def _tuples_to_passages(self, filtered_blocks):
        passages = []
        for tup in filtered_blocks:
            a = self.file_name_a[tup[0]:tup[0]+tup[2]]
            b = self.file_name_a[tup[1]:tup[1]+tup[2]]
            passages.append((a, b))
        return passages
