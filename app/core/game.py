class Game:
    def __init__(self):
        self.entities = []
        self.deities = []

    def add_entity(self, entity):
        self.entities.append(entity)
        print(f"Entity {entity.name} added to the game.")

    def add_deity(self, deity):
        self.deities.append(deity)
        print(f"Deity {deity.name} added to the game.")

    def end_turn(self):
        for entity in self.entities:
            entity.end_turn()
        for deity in self.deities:
            deity.end_turn()

    def status(self):
        print("game status:")
        for entity in self.entities:
            print(f" - {entity.name}: {entity.wealth} resources, {entity.army} army")
        print(f"deities: {", ".join(deity.name for deity in self.deities)}")
        for deity in self.deities:
            for cult in deity.cults:
                print(f" - {deity.name} favors {cult.entity.name} with {cult.favor()}")
        print("---")
