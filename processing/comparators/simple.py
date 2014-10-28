import difflib

import processing.comparators.base_comparator as base_comparator
from models.match_singlet import MatchSinglet
from models.match import Match


CLASS_NAME = 'SimpleComparator'


def double_iter(iterable):
    for i in xrange(len(iterable) - 1):
        yield iterable[i], iterable[i+1]


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
        Parameters
            matching_blocks - list of tuples (i, j, n)
        """
        # this just combines nearby blocks in alpha
        combined_blocks = []
        for block, next_block in double_iter(matching_blocks):
            alpha_end = block[0] + block[2]
            next_alpha_start = next_block[0]
            if next_alpha_start - alpha_end < self.gap_length:
                # combine
                next_alpha_end = next_alpha_start + next_block[2]
                new_length = next_alpha_end - block[0]
                new_match = (block[0], block[1], new_length)
                # TODO: lookahead to combine more blocks if applicable
                combined_blocks.append(new_match)
            else:
                combined_blocks.append(block)
        return combined_blocks

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
