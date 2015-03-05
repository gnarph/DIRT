from collections import namedtuple


MatchTuple = namedtuple(typename='MatchTuple',
                        field_names=['a', 'b', 'a_end', 'b_end'])


class MatchConcatenator(object):
    """
    Class for combining match blocks based on their locations
    and sizes, covered by gap_length
    """

    def __init__(self, match_list, gap_length):
        """
        :param match_list: list of MatchTuples
        :param gap_length: max length of gap to jump
        """
        self.match_list = match_list
        self.i = 0
        self.j = 1
        self.g2 = 0
        self.gap_length = gap_length
        self.match_count = len(self.match_list)
        if self.match_count:
            first = self.match_list[self.i]
            self.a_cursor = first.a_end
            self.b_cursor = first.b_end
            self.combined = []

    def move_cursors_to_end(self, target_block):
        """
        Move cursors to end of target block
        :param target_block: block to move cursors to end of
        """
        self.a_cursor = target_block.a_end
        self.b_cursor = target_block.b_end

    def _process_main(self):
        """
        Process the blocks (except the last)
        :return: leftmost block not combined,
                 rightmost block combining,
                 should we continue using process main
        """
        # Cursors to blocks which may be combined
        first = self.match_list[self.i]
        second = self.match_list[self.j]
        if not self.can_combine(first, second):
            if first.a_end == self.a_cursor:
                # Couldn't combine, just add first
                # to the combined list
                self.combined.append(first)
                # Advance cursor
                self.i = self.j
            elif self.is_valid_block(first):
                # Can't combine any more, so combine
                # those that have just been past
                self.combine_and_select_block(first)
                self.i = self.j
        # Advance second cursor
        self.j += 1
        cont = self.j < self.match_count
        if cont:
            self.move_cursors_to_end(second)
        return first, second, cont

    def combine_and_select_block(self, first):
        """
        Combine block and add it to combined list
        :param first: block at which to start the combination
        """
        block = self.combine_block(first)
        self.combined.append(block)

    def _process_last(self, first, second):
        """
        Processes the last match block
        :param first:
        :param second:
        """
        if not self.can_combine(first, second):
            # no combining
            self.combined.append(first)
            self.combined.append(second)
        else:
            # combine and terminate
            self.move_cursors_to_end(second)
            self.combine_and_select_block(first)

    def concatenate(self):
        """
        Concatenate match blocks depending on gap_length
        :return: list of concatenated blocks
        """
        if not self.match_count:
            # No concatenating if there are no matches
            return []
        if self.match_count <= 1:
            # Can't combine a single match
            return self.match_list
        # Setup for iterating through
        cont = True
        first = self.match_list[self.i]
        second = self.match_list[self.j]
        while cont and self.match_count > 2:
            first, second, cont = self._process_main()

        # Last block is a special case
        self._process_last(first, second)
        return self.combined

    def is_valid_block(self, first):
        """
        Check that a concatenated block is avlid
        :param first: earlier blocks
        :return: boolean
        """
        return (self.a_cursor > first.a and
                self.b_cursor > first.b)

    def combine_block(self, first):
        """
        Combine from first block to cursors
        :param first: position to start combining
        :return: combined block
        """
        return MatchTuple(a=first.a,
                          b=first.b,
                          a_end=self.a_cursor,
                          b_end=self.b_cursor)

    def can_combine(self, first, second):
        """
        Check if two blocks can be combined
        :param first: first block in list
        :param second: second block in list
        :return: boolean indicating if blocks can be combined
        """
        # Need to check out of order issues as
        # blocks are sorted by where they start in a
        mismatch_ab = (first.a_end <= second.a
                       and second.b_end <= first.b)
        mismatch_ba = (second.a_end <= first.a
                       and first.b_end <= second.b)
        out_of_order = mismatch_ab or mismatch_ba
        return not out_of_order and self.jump_gap(second)

    def jump_gap(self, last):
        """
        Check if we can jump from the cursors to a match
        cannot jump if the matches are out of order
        :param last: match to attempt a jump to
        :return: if we can jump to the next match
        """
        a_gap = last.a - self.a_cursor
        b_gap = last.b - self.b_cursor
        return (a_gap <= self.gap_length and
                b_gap <= self.gap_length)
