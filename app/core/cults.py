class Cult():
    def __init__(self, deity, entity, id=None):
        self.id = id
        self.deity = deity
        self.entity = entity
        self.offerings = 0
        self.deity.add_cult(self)

    def make_offering(self, amount):
        self.offerings += amount

    def favor(self):
        return self.offerings

    def end_turn(self):
        # deity consumes offerings
        self.offerings -= 5

    def __eq__(self, other):
        return self.deity == other.deity and self.entity == other.entity