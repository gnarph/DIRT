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
                else:
                    # terminate
                    # don't want first and second, only want first up to cursor
                    block = self.get_block(first, second)
                    combined.append(block)
                    self.j += 1
                    self.i = self.j
            self.j += 1
            self.a_cursor = second.a_end
            self.b_cursor = second.b_end
            # update end of current comb cursor
        # terminate last block
        block = self.get_block(first, second)
        combined.append(block)
        return combined

    @staticmethod
    def get_block(first, second):
        return MatchTuple(a=first.a,
                          b=first.b,
                          a_end=second.a_end,
                          b_end=second.b_end)

    def jump_gap(self, a_gap, b_gap):
        return (a_gap <= self.gap_length and
                b_gap <= self.gap_length)
