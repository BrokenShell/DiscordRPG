class Bonuses:

    def __init__(self, offense=0, defense=0, balance=0):
        self.offense = offense
        self.defense = defense
        self.balance = balance

    def __add__(self, other):
        offense = self.offense + other.offense
        defense = self.defense + other.defense
        balance = self.balance + other.balance
        return Bonuses(offense, defense, balance)
