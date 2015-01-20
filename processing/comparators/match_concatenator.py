from collections import namedtuple


MatchTuple = namedtuple(typename='MatchTuple',
                        field_names=['a', 'b', 'a_end', 'b_end'])


class DoneMainBlocks(BaseException):
    pass


def difflib_blocks_to_match_tuples(blocks):
    tuples = []
    for tup in blocks:
        mt = MatchTuple(a=tup.a,
                        b=tup.b,
                        a_end=tup.a+tup.size,
                        b_end=tup.b+tup.size)
        tuples.append(mt)
    return tuples


def passage_to_match_tuple(a, b, a_psg, b_psg):
    a_start = a.index(a_psg)
    b_start = b.index(b_psg)
    a_end = a_start + len(a_psg)
    b_end = b_start + len(b_psg)
    mt = MatchTuple(a=a_start,
                    b=b_start,
                    a_end=a_end,
                    b_end=b_end)
    return mt


def passages_to_match_tuples(a, b, passage_pairs):
    tups = []
    for a_psg, b_psg in passage_pairs:
        tup = passage_to_match_tuple(a=a,
                                     b=b,
                                     a_psg=a_psg,
                                     b_psg=b_psg)
        tups.append(tup)
    return tups


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

    def move_cursors_to_end(self, second):
        self.a_cursor = second.a_end
        self.b_cursor = second.b_end

    def _process_main(self):
        """
        Process the blocks (except the last)
        :return: leftmost block not combined,
                 rightmost block combining,
                 should we continue using process main
        """
        first = self.match_list[self.i]
        second = self.match_list[self.j]
        if not self.can_combine(first, second):
            if first.a_end == self.a_cursor:
                self.combined.append(first)
                self.i = self.j
            elif self.is_valid_block(first):
                # terminate
                self.combine_and_select_block(first)
                self.i = self.j
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
            return []
        if self.match_count <= 1:
            return self.match_list
        cont = True
        first = self.match_list[self.i]
        second = self.match_list[self.j]
        while cont and self.match_count > 2:
            first, second, cont = self._process_main()

        self._process_last(first, second)
        return self.combined

    def is_valid_block(self, first):
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
        mismatch_ab = (first.a_end < second.a
                       and second.b_end < first.b)
        mismatch_ba = (second.a_end < first.a
                       and first.b_end < second.b)
        out_of_order = mismatch_ab or mismatch_ba
        return not out_of_order and self.jump_gap(second)

    def jump_gap(self, last):
        """
        Check if we can jump from the cursors to a match
        :param last: match to attempt a jump to
        :return: if we can jump to the next match
        """
        a_gap = last.a - self.a_cursor
        b_gap = last.b - self.b_cursor
        return (a_gap <= self.gap_length and
                b_gap <= self.gap_length)
