class Deity:
    def __init__(self, name, domain, id=None):
        self.id = id
        self.name = name
        self.domain = domain
        self.cults = []

    def add_cult(self, cult):
        if cult not in self.cults:
            self.cults.append(cult)

    # me-lam = a sumerian word meaning a burning hot divine attire
    def melam(self):
        ret = 0
        for cult in self.cults:
            ret += cult.offerings
        return ret

    def syncretize(self, other):
        # implement later
        return
    
    def end_turn(self):
        for cult in self.cults:
            cult.end_turn()