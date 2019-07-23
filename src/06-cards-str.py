# Python によるプログラミング：第 6 章
# 例題 6.7 strの導入
# --------------------------
# プログラム名: 06-cards-str.py

from dataclasses import dataclass
import random

@dataclass
class Card:
    suit: str
    rank: int
    def __str__(self):   # __str__ によるカードの表示
        return "{} の {}".format(self.suit, self.rank)

#main routine
card = Card("spade", 1)
print("カード: {}".format(card))
