from dataclasses import dataclass

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

for card in cards:
    card.print()
