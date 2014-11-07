from collections import namedtuple


MatchTuple = namedtuple('MatchTuple', ['a', 'b', 'a_end', 'b_end'])


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


class MatchConcatenator(object):

    def __init__(self, match_list, gap_length):
        self.match_list = match_list
        self.i = 0
        self.j = 1
        self.g2 = 0
        self.gap_length = gap_length
        first = self.match_list[self.i]
        self.a_cursor = first.a_end
        self.b_cursor = first.b_end
        self.combined = []
        self.match_count = len(self.match_list)

    def move_cursors_to_end(self, second):
        self.a_cursor = second.a_end
        self.b_cursor = second.b_end

    def _process_main(self):
        first = self.match_list[self.i]
        second = self.match_list[self.j]
        if not self.jump_gap(second):
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
        block = self.get_block(first)
        self.combined.append(block)

    def _process_last(self, first, second):
        last = second
        if not self.jump_gap(last):
            if first.a_end == self.a_cursor:
                # no combining
                self.combined.append(first)
                self.combined.append(second)
            else:
                # terminate
                self.combine_and_select_block(first)
                self.combined.append(last)
        else:
            # combine and terminate
            self.move_cursors_to_end(last)
            self.combine_and_select_block(first)

    def concatenate(self):
        cont = True
        while cont:
            first, second, cont = self._process_main()

        self._process_last(first, second)
        return self.combined

    def is_valid_block(self, first):
        return (self.a_cursor > first.a and
                self.b_cursor > first.b)

    def get_block(self, first):
        return MatchTuple(a=first.a,
                          b=first.b,
                          a_end=self.a_cursor,
                          b_end=self.b_cursor)

    def jump_gap(self, last):
        a_gap = last.a - self.a_cursor
        b_gap = last.b - self.b_cursor
        return (a_gap <= self.gap_length and
                b_gap <= self.gap_length)
