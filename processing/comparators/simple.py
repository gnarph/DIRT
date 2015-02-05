from collections import namedtuple
import itertools
import operator
import re

import processing.comparators.base_comparator as base_comparator
from models.match_singlet import MatchSinglet
import processing.comparators.match_concatenator as concatenator
from utilities.suffix_array import matcher as suffix_apps
from processing.comparators import spacer

MatchBlock = namedtuple('MatchBlock', ['a', 'b', 'size'])


class Comparator(base_comparator.BaseComparator):

    def _find_matching_blocks(self, matching_passages):
        """
        Find matchblocks from matching passages
        :param matching_passages: strings representing matching
                                  passages in both docs
        :return: list of concatenator.MatchTuples sorted by where
                 they appear in document a
        """
        blocks = set()
        for a_passage, b_passage in matching_passages:
            a_matches = re.finditer(a_passage, self.a)
            a_starts = (i.start() for i in a_matches)
            b_matches = re.finditer(b_passage, self.b)
            b_starts = (j.start() for j in b_matches)

            l_a = len(a_passage)
            l_b = len(b_passage)
            for i, j in itertools.product(a_starts, b_starts):
                new_block = concatenator.MatchTuple(i, j, i+l_a, j+l_b)
                blocks.add(new_block)
        # Concerned that sorting on a may adversely impact
        # concat on the b side
        blocks = sorted(blocks, key=operator.attrgetter('a'))
        return blocks

    def get_matching_passages(self):
        # Still need to remove/re-add spaces
        a_strip = self.a.replace(' ', '')
        b_strip = self.b.replace(' ', '')
        matching_passages = suffix_apps.acs_no_substrings(a=a_strip,
                                                          b=b_strip)
        a_passages = spacer.respace(self.a, a_strip, matching_passages)
        b_passages = spacer.respace(self.b, b_strip, matching_passages)
        passage_pairs = zip(a_passages, b_passages)
        return passage_pairs

    def compare(self):
        """
        Compare texts
        :return: list of singlet pairs
        """
        matching_passages = self.get_matching_passages()

        blocks = self._find_matching_blocks(matching_passages)
        combined_blocks = self._combine_blocks(blocks)
        filtered_blocks = self._filter_blocks(combined_blocks)
        passage_blocks = self._tuples_to_passages(filtered_blocks)

        return self._get_singlet_pairs(passage_blocks)

    def _combine_blocks(self, matching_blocks):
        """
        :param matching_blocks: list of tuples (i, j, n)
        """
        cat = concatenator.MatchConcatenator(matching_blocks, self.gap_length)
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
        """
        Get passages from concatenator blocks
        :param filtered_blocks: list of concatenator blocks
        :return: list of tuples containing the passage
                 in a and in b
        """
        passages = []
        for tup in filtered_blocks:
            a = self.a[tup.a:tup.a_end]
            b = self.b[tup.b:tup.b_end]
            # TODO: consider namedtuple for clarity
            passages.append((a, b))
        return passages

    @staticmethod
    def _get_singlet_pairs(passage_blocks):
        """
        Get the match singlet from passage pairs
        :param passage_blocks: list of passage pair tuples
        :return: list of singlet pair tuples
        """
        singlet_pairs = []
        for p_a, p_b in passage_blocks:
            s_a = MatchSinglet(passage=p_a)
            s_b = MatchSinglet(passage=p_b)
            singlet_pairs.append((s_a, s_b))
        return singlet_pairs
