from app.core.game import Game
from app.core.deities import Deity
from app.core.entities import Entity


if __name__ == "__main__":
    ishkur = Deity("Ishkur", "Storm")
    adad = Deity("Adad", "Storm")
    shuruppak = Entity("Shuruppak", ishkur)
    amurru = Entity("Amurru", adad)

    game = Game()
    game.add_entity(shuruppak)
    game.add_entity(amurru)
    game.add_deity(ishkur)
    game.add_deity(adad)
    print("---")

    amurru.offer_to(adad, 20)
    shuruppak.offer_to(ishkur, 50)

    game.end_turn()
    game.status()

    shuruppak.attack(amurru)
