import pandas as pd
import random
import copy

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9,
    '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

class Shoe:
    def __init__(self, num_decks=6):
        self.cards = None
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


def start_game(shoe, option):
    if len(shoe.cards) < 100:
        shoe.build_shoe()
    player_hand = Hand()
    dealer_hand = Hand()

    # 1. Initial dealing of two cards each for the dealer and player
    player_hand.add_card(shoe.deal_card())
    player_hand.add_card(shoe.deal_card())
    dealer_hand.add_card(shoe.deal_card())
    dealer_hand.add_card(shoe.deal_card())
    player_hand_org = copy.deepcopy(player_hand)
    dealer_hand_org = copy.deepcopy(dealer_hand)

    # both of the player's cards and first of the dealer's cards is made visible
    #print("Player Hand :", player_hand.cards)
    #print("Dealer Hand :", dealer_hand.cards[0])

    player_choice = ""
    player_bets = 0

    # player's turn to play, they can choose to either stand or hit once
    if not player_hand.is_bust():
        if option == "player":
            print("Player Hand :", player_hand.cards)
            print("Dealer's First Card :", dealer_hand.cards[0])
            player_choice = input("Enter H to hit and S to stand :").upper()
        elif option == "sim":
            player_choice = random.choice(['H', 'S'])

        if player_choice == "H":
            player_hand.add_card(shoe.deal_card())
        elif player_choice == "S":
            pass

    player_hand, dealer_hand, player_bets, outcome = play_game(shoe, player_hand, dealer_hand, player_bets)
    if option == "player":
        print("Player Outcome :", outcome)
    elif option == "sim":
        pass

    return player_hand_org, dealer_hand_org, player_choice, player_hand, dealer_hand, player_bets, outcome


def play_game(shoe, player_hand, dealer_hand, player_bets):

    if player_hand.is_bust():
        #print("Player busted, Dealer Wins!")
        player_bets -= 1
        outcome = "Loss"
        return player_hand, dealer_hand, player_bets, outcome

    # dealer's turn to play, they must hit till they reach a value of at least 17 and then they stand
    #print("Dealer Hand :", dealer_hand.cards)
    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(shoe.deal_card())
        #print("Dealer Hand :", dealer_hand.cards)

    if dealer_hand.is_bust():
        #print("Dealer busted, Player Wins!")
        player_bets += 1
        outcome = "Win"
        return player_hand, dealer_hand, player_bets, outcome

    # if neither dealer nor player are busted, compare the card values
    if player_hand.get_value() > dealer_hand.get_value():
        #print("Player Wins!")
        player_bets += 1
        outcome = "Win"
    elif player_hand.get_value() < dealer_hand.get_value():
        #print("Dealer Wins!")
        player_bets -= 1
        outcome = "Loss"
    else:
        #print("Draw!")
        outcome = "Draw"

    return player_hand, dealer_hand, player_bets, outcome


def sim_blackjack(sim_hands, option = "sim", shoe = None):
    if shoe is None:
        shoe = Shoe()
    data_results = []
    table_headers = ['player_hand_org', 'dealer_hand_org', 'player_choice', 'player_hand', 'dealer_hand', 'player_bets', 'outcome']

    for hands in range(sim_hands):
        player_hand_org, dealer_hand_org, player_choice, player_hand, dealer_hand, player_bets, outcome = start_game(shoe, option)
        data_results.append([
            player_hand_org.cards,
            dealer_hand_org.cards,
            player_choice,
            player_hand.cards,
            dealer_hand.cards,
            player_bets,
            outcome
        ])

    results_table = pd.DataFrame(data_results, columns = table_headers)

    return results_table


if __name__ == "__main__":
    class_shoe = Shoe()

    while True:  # This loop allows the game to ask again after each turn
        print("\n--- Blackjack Menu ---")
        print("1 = Play game (1 Round)")
        print("2 = Run simulation (5 Rounds)")
        print("Q = Quit")

        choice = input("Choose: ").strip().upper()

        if choice == "1":
            # Changed sim_hands to 1 so it plays exactly one turn then returns here
            blackjack_df = sim_blackjack(1, "player", class_shoe)
            print("\n--- Round Results ---")
            print(blackjack_df)

        elif choice == "2":
            blackjack_df = sim_blackjack(100000, "sim", class_shoe)
            print("\n--- Simulation Results ---")
            print(blackjack_df)

        elif choice == "Q":
            print("Thanks for playing!")
            break  # Now this break is inside a loop, so it works perfectly

        else:
            print("Invalid choice. Please try again.")