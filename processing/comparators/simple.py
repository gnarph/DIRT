from collections import namedtuple
import difflib

import processing.comparators.base_comparator as base_comparator
from models.match_singlet import MatchSinglet
from models.match import Match
from utilities.iteration import niter
import processing.comparators.match_concatenator as concatenator


def double_iter(iterable):
    return niter(iterable, 2)


class Comparator(base_comparator.BaseComparator):

    def compare(self):
        """
        Compare texts
        :return: list of Matches
        """
        matcher = difflib.SequenceMatcher(isjunk=lambda x: x in ' \n\t',
                                          a=self.a,
                                          b=self.b)
        matching_blocks = matcher.get_matching_blocks()
        # Last block is a dummy
        combined_blocks = self._combine_blocks(matching_blocks[:-1])
        filtered_blocks = self._filter_blocks(combined_blocks)
        passage_blocks = self._tuples_to_passages(filtered_blocks)

        matches = self._get_matches(passage_blocks)
        return matches

    def _combine_blocks(self, matching_blocks):
        """
        :param matching_blocks: list of tuples (i, j, n)
        """
        blocks = concatenator.difflib_blocks_to_match_tuples(matching_blocks)
        cat = concatenator.MatchConcatenator(blocks, self.gap_length)
        return cat.concatenate()

        # this just combines nearby blocks in alpha
        combined_blocks = []
        i = 0
        j = 1
        end = None
        g2 = 0
        while j < len(matching_blocks):
            first = matching_blocks[i]
            if end is None:
                end = first.a + first.size
            second = matching_blocks[j]
            gap = second.a - end
            if gap < self.gap_length:
                # Block continues
                # why 2?
                g2 += gap + 2
            else:
                # Block terminates
                self._terminate_block(combined_blocks, end, first, g2)
                i = j
            j += 1
            end = second.a + second.size
        self._terminate_block(combined_blocks, end, first, g2)
        return combined_blocks

    def _terminate_block(self, combined_blocks, end, first, g2):
        new_length = end - first.a
        new_match = self.MatchTuple(a=first.a,
                                    b=first.b,
                                    len_a=new_length,
                                    len_b=new_length + g2)
        combined_blocks.append(new_match)

    def _filter_blocks(self, combined_blocks):
        """
        Filter match blocks based on length
        """
        return [tup for tup in combined_blocks if tup[2] > self.match_length]

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
            s_a = MatchSinglet(file_name=self.name_a,
                               passage=p_a)
            s_b = MatchSinglet(file_name=self.name_b,
                               passage=p_b)
            singlet_pairs.append((s_a, s_b))
        return singlet_pairs

    def _get_matches(self, passage_blocks):
        singlet_pairs = self._get_singlet_pairs(passage_blocks)
        matches = []
        for s_a, s_b in singlet_pairs:
            match = Match(s_a, s_b)
            matches.append(match)
        return matches
