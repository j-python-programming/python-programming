from dataclasses import dataclass
import random

@dataclass
class Card:
    suit: str
    rank: int

    def print(self):
        print("{}.{}".format(self.suit, self.rank))

cards = [
    Card("spade", 1),
    Card("spade", 2),
    Card("spade", 3)
    ]

random.shuffle(cards)
for card in cards:
    card.print()
