

class SuperStringSet(set):

    def add(self, item):
        for contained in self:
            if item in contained:
                # Superstring already present
                return
            if contained in item:
                # New item supercedes old one
                self.remove(contained)
        super(set, self).add(item)