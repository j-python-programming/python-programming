# Pythonによるプログラミング：第 6 章
#  例題 6.2 カードとカードテーブル
# --------------------------
# プログラム名: 06-cards.py
# 本文、P147 リスト6.8, リスト6.9, リスト6.10

from dataclasses import dataclass
import random

@dataclass
class Card:
    suit: str
    rank: int

    def print(self):                # カードの表示
        print("{}.{}".format(self.suit, self.rank))

class CardTable:
    def __init__(self): # カードテーブルの初期化
        self.deck = []
        self.hand = []

def set_cards(deck): # デッキに全てのカードをセットする
    for suit in ["spade", "heart", "club", "diamond"]:
        for rank in range(13):
            deck.append(Card(suit, rank))
    random.shuffle(deck)

table = CardTable()
set_cards(table.deck)
for x in range(5):
    card = table.deck.pop()  # カードをデッキから一枚取り出し
    table.hand.append(card)  # ハンド手札に追加する。

for card in table.hand:      # 手札の全てのカードを取り出し、
    card.print()             # カードを表示する。
