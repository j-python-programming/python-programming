# Python によるプログラミング：第 6 章
#  例題 6.2 カードとカードテーブル
# --------------------------
# プログラム名: 06-cards-2.py

from dataclasses import dataclass
import random

@dataclass
class Card:
    suit: str
    rank: int

    def print(self):                # カードの表示
        print("{}.{}".format(self.suit, self.rank))

class CardTable:
    def __init__(self):    # コンストラクタ
        self.deck = []
        self.hand = []

    def print_hand(self):
        for card in self.hand:
            card.print()

    def set_cards(self):     # デッキに全てのカードをセットする
        for suit in ["spade", "heart", "club", "diamond"]:
            for rank in range(13):
                self.deck.append(Card(suit, rank))
        random.shuffle(self.deck)

    def deliver(self, n):
        for x in range(n):
            card = self.deck.pop()  # カードをデッキから一枚取り出し
            self.hand.append(card)  # ハンド手札に追加する。

#main routine
table = CardTable()
table.set_cards()
table.deliver(5)
table.print_hand()
