from collections import namedtuple
import itertools
import operator
import re

import processing.comparators.base_comparator as base_comparator
from models.match_singlet import MatchSinglet
import processing.comparators.match_concatenator as concatenator
from utilities.suffix_array import applications as suffix_apps

MatchBlock = namedtuple('MatchBlock', ['a', 'b', 'size'])


class Comparator(base_comparator.BaseComparator):

    def compare(self):
        """
        Compare texts
        :return: list of singlet pairs
        """
        # Still need to remove/re-add spaces
        matching_passages = suffix_apps.all_common_substrings(a=self.a,
                                                              b=self.b)

        blocks = set()
        for passage in matching_passages:
            a_matches = re.finditer(passage, self.a)
            a_starts = (i.start() for i in a_matches)
            b_matches = re.finditer(passage, self.b)
            b_starts = (j.start() for j in b_matches)

            l = len(passage)
            for i, j in itertools.product(a_starts, b_starts):
                new_block = MatchBlock(i, j, l)
                blocks.add(new_block)
        # Concerned that sorting on a may adversely impact
        # concat on the b side
        blocks = sorted(blocks, key=operator.attrgetter('a'))

        combined_blocks = self._combine_blocks(blocks)
        filtered_blocks = self._filter_blocks(combined_blocks)
        passage_blocks = self._tuples_to_passages(filtered_blocks)

        return self._get_singlet_pairs(passage_blocks)

    def _combine_blocks(self, matching_blocks):
        """
        :param matching_blocks: list of tuples (i, j, n)
        """
        blocks = concatenator.difflib_blocks_to_match_tuples(matching_blocks)
        cat = concatenator.MatchConcatenator(blocks, self.gap_length)
        return cat.concatenate()

    def _filter_blocks(self, combined_blocks):
        """
        Filter match blocks based on length
        """
        filtered = []
        for block in combined_blocks:
            a_len = block.a_end - block.a
            b_len = block.b_end - block.b
            if a_len >= self.match_length:
                filtered.append(block)
            elif b_len >= self.match_length:
                filtered.append(block)
        return filtered

    def _tuples_to_passages(self, filtered_blocks):
        passages = []
        for tup in filtered_blocks:
            a = self.a[tup.a:tup.a_end]
            b = self.b[tup.b:tup.b_end]
            passages.append((a, b))
        return passages

    def _get_singlet_pairs(self, passage_blocks):
        singlet_pairs = []
        for p_a, p_b in passage_blocks:
            s_a = MatchSinglet(passage=p_a)
            s_b = MatchSinglet(passage=p_b)
            singlet_pairs.append((s_a, s_b))
        return singlet_pairs
