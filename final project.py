#part 1 - Blackjack classes - use a shoe of 6 decks of cards, and shuffle the shoe if the card count gets < 100 reshuffle
import random
CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9,
    '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

class Shoe:
    def __init__(self, num_decks=6):
        self.num_decks = num_decks
        self.build_shoe()

    def build_shoe(self):
        ranks = list(CARD_VALUES.keys())
        self.cards = ranks * 4 * self.num_decks
        random.shuffle(self.cards)

    def deal_card(self):
        if len(self.cards) < 100:
            print("Reshuffling shoe...")
            self.build_shoe()
        return self.cards.pop()


class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value = sum(CARD_VALUES[c] for c in self.cards)
        aces = self.cards.count('A')

        #CITATION, UMGPT: How do I adjust for aces
        while value > 21 and aces:
            value -= 10
            aces -= 1

        return value

    def is_bust(self):
        return self.get_value() > 21


#part 2 - Blackjack game using classes and user input - assume every hand is worth $1, tracking win/loss amount
#part 3 - Build a results table to show what strategy loses the least money - for each starting hand value for the player and the dealer, either hit or stand and track the result - just do a single hit or stand and then track win/lose/draw
#simulate 100,000 hands, track our starting hand value and then randomly pick hit or stand, and track win/loss/draw result
#at the end, display a table showing the results of hitting and standing for each starting value