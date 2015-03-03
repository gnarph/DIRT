from collections import namedtuple
import itertools
import operator
import re

import processing.comparators.base_comparator as base_comparator
from models.match_singlet import MatchHalf
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
        for passage in matching_passages:
            a_matches = re.finditer(passage, self.a_strip)
            a_starts = (i.start() for i in a_matches)
            b_matches = re.finditer(passage, self.b_strip)
            b_starts = (j.start() for j in b_matches)

            l = len(passage)
            for i, j in itertools.product(a_starts, b_starts):
                new_block = concatenator.MatchTuple(i, j, i+l, j+l)
                blocks.add(new_block)
        # Concerned that sorting on a may adversely impact
        # concat on the b side
        blocks = sorted(blocks, key=operator.attrgetter('a'))
        return blocks

    def get_matching_passages(self):
        """
        Get common passages between document
        :return: set of common passages
        """
        matching_passages = suffix_apps.acs_no_substrings(a=self.a_strip,
                                                          b=self.b_strip)
        return matching_passages

    def compare(self):
        """
        Compare texts
        :return: list of singlet pairs
        """
        matching_passages = self.get_matching_passages()

        blocks = self._find_matching_blocks(matching_passages)

        # Concatenate blocks by gap length
        combined_blocks = self._combine_blocks(blocks)

        # Filter blocks by length
        filtered_blocks = self._filter_blocks(combined_blocks)

        # Get actual blocks
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
        a_spaces = spacer.get_space_locations(self.a)
        b_spaces = spacer.get_space_locations(self.b)
        passages = []
        for tup in filtered_blocks:
            a = self.a_strip[tup.a:tup.a_end]
            b = self.b_strip[tup.b:tup.b_end]

            a_passage = spacer.add_spaces(a_spaces, tup.a, a)
            b_passage = spacer.add_spaces(b_spaces, tup.b, b)
            passage_tup = (a_passage, b_passage)
            passages.append(passage_tup)
        return passages

    @staticmethod
    def _pass_gen(strip_body, blocks):
        for b in blocks:
            yield strip_body[b.tup]

    @staticmethod
    def _get_singlet_pairs(passage_blocks):
        """
        Get the match singlet from passage pairs
        :param passage_blocks: list of passage pair tuples
        :return: list of singlet pair tuples
        """
        singlet_pairs = []
        for p_a, p_b in passage_blocks:
            s_a = MatchHalf(passage=p_a)
            s_b = MatchHalf(passage=p_b)
            singlet_pairs.append((s_a, s_b))
        return singlet_pairs
