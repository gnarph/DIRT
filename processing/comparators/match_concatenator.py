from collections import namedtuple


MatchTuple = namedtuple('MatchTuple', ['a', 'b', 'a_end', 'b_end'])


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

    def move_cursors_to_end(self, second):
        self.a_cursor = second.a_end
        self.b_cursor = second.b_end

    def concatenate(self):
        combined = []
        while self.j < len(self.match_list):
            first = self.match_list[self.i]
            second = self.match_list[self.j]
            a_gap = second.a - self.a_cursor
            b_gap = second.b - self.b_cursor
            if not self.jump_gap(a_gap, b_gap):
                if first.a_end == self.a_cursor:
                    combined.append(first)
                    self.i = self.j
                elif self.is_valid_block(first):
                    # terminate
                    block = self.get_block(first)
                    combined.append(block)
                    self.i = self.j
            self.j += 1
            self.move_cursors_to_end(second)
        # terminate last block
        self.move_cursors_to_end(second)
        block = self.get_block(first)
        combined.append(block)
        return combined

    def is_valid_block(self, first):
        return (self.a_cursor > first.a and
                self.b_cursor > first.b)

    def get_block(self, first):
        return MatchTuple(a=first.a,
                          b=first.b,
                          a_end=self.a_cursor,
                          b_end=self.b_cursor)

    def jump_gap(self, a_gap, b_gap):
        return (a_gap <= self.gap_length and
                b_gap <= self.gap_length)
