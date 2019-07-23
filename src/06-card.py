from dataclasses import dataclass

@dataclass
class Card:
    suit: str
    rank: int

    def print(self):
        print("{} の {}".format(self.suit, self.rank))

card = Card("heart", 10)
card.print()
