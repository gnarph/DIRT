from collections import namedtuple
import difflib

import processing.comparators.base_comparator as base_comparator
from models.match_singlet import MatchSinglet
import processing.comparators.match_concatenator as concatenator

MatchBlock = namedtuple('MatchBlock', ['a', 'b', 'size'])


class Comparator(base_comparator.BaseComparator):

    def _get_matching_blocks_ab(self):
        """
        Get matching blocks going from a
        """
        matcher = difflib.SequenceMatcher(isjunk=lambda x: x in ' \n\t',
                                          a=self.a,
                                          b=self.b)
        matching_blocks = matcher.get_matching_blocks()
        return matching_blocks

    def _get_matching_blocks_ba(self):
        """
        Get matching blocks going from b
        """
        matcher2 = difflib.SequenceMatcher(isjunk=lambda x: x in ' \n\t',
                                           a=self.b,
                                           b=self.a)
        inv_matching_blocks = matcher2.get_matching_blocks()
        matching_blocks2 = []
        # Need to swap around to match format based on a
        for block in inv_matching_blocks:
            b = MatchBlock(a=block.b,
                           b=block.a,
                           size=block.size)
            matching_blocks2.append(b)

        return matching_blocks2

    def compare(self):
        """
        Compare texts
        :return: list of singlet pairs
        """

        # matching_blocks = self._get_matching_blocks_ab()
        # matching_blocks2 = self._get_matching_blocks_ba()
        #
        # # Last block is a dummy
        # combined_blocks = self._combine_blocks(matching_blocks[:-1])
        # filtered_blocks = self._filter_blocks(combined_blocks)
        #
        # combined_blocks2 = self._combine_blocks(matching_blocks2[:-1])
        # filtered_blocks2 = self._filter_blocks(combined_blocks2)
        #
        # passage_blocks = self._tuples_to_passages(filtered_blocks)
        # passage_blocks2 = self._tuples_to_passages(filtered_blocks2)
        #
        # for pb in passage_blocks2:
        #     if pb not in passage_blocks:
        #         passage_blocks.append(pb)
        passage_blocks = self.hack_lcs(self.a, self.b)

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

    def hack_lcs(self, a, b):
        import pyximport; pyximport.install()
        from utilities.lcs import matched_passages
        passages = list(matched_passages(a, b))
        tups = [(p, p) for p in passages]
        return tups

