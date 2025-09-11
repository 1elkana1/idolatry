import random
from .cults import Cult

class Entity():
    def __init__(self, name, patron=None, army=0, wealth=100, id=None):
        self.id = id
        self.name = name
        self.cults = []
        self.army = army
        self.wealth = wealth
        self.recruit_army(10)
        if patron:
            self.establish_cult_to(patron)

    def patron(self):
        patron_cult = max(self.cults, key=lambda c: c.offerings, default=None)
        return patron_cult.deity if patron_cult else None
    
    def establish_cult_to(self, deity, initial_offering=0):
        cult = Cult(deity, self, initial_offering)
        self.add_cult(cult)
        return cult
    
    def add_cult(self, cult):
        if cult not in self.cults:
            self.cults.append(cult)

    def offer_to(self, deity, amount):
        if self.wealth < amount:
            print(f"{self.name} lacks wealth to offer to {deity.name}!")
            return False
        cult = next((c for c in self.cults if c.deity == deity), None)
        if not cult:
            cult = self.establish_cult_to(deity)
        cult.make_offering(amount)
        self.wealth -= amount
        return True

    def recruit_army(self, n):
        if self.wealth >= n:
            self.wealth -= n
            self.army += n
            print(f"{self.name} recruits {n} soldiers. (army size: {self.army}, remaining wealth: {self.wealth})")
            return True
        print(f"{self.name} lacks wealth to recruit {n} soldiers!")
        return False

    def attack(self, defender):
        print(f"{self.name} attacks {defender.name}!")
        attacker_power = self.battle_power()
        defender_power = defender.battle_power()
        print(f"Power: {self.name}={attacker_power} vs {defender.name}={defender_power}")
        total = attacker_power + defender_power
        chance = random.randint(1, total)
        if chance <= attacker_power:
            print(f"{self.name} wins the battle!")
            defender.army = max(0, defender.army - 10)
        else:
            print(f"{defender.name} defends successfully!")
            self.army = max(0, self.army - 10)

    def battle_power(self):
        army_power = self.army
        blessing_bonus = 0
        for cult in self.cults:
            deity_bonus = cult.favor()
            print(f"{cult.deity.name} blesses {self.name} with {deity_bonus} battle power")
            blessing_bonus += deity_bonus
        return army_power + blessing_bonus

    def end_turn(self):
        self.wealth += 5
