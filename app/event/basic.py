import random


class Basic(object):

    def __init__(self) -> None:
        pass

    def fortunate(self):
        fortune = random.choice(['大凶', '凶', '末吉', '小吉', '中吉', '大吉', '仙草吉'])
        return fortune
