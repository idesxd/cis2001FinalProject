#Paste everything from other files
import random
import copy
import pandas as pd

CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9,
    '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11
}
def print_banner():
    print("\n==============================")
    print("     BLACKJACK SIMULATOR")
    print("         (Target: 21)")
    print("==============================")
    
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
        value = sum(CARD_VALUES[card] for card in self.cards)
        aces = self.cards.count('A')

        while value > 21 and aces > 0:
            value -= 10
            aces -= 1

        return value

    def is_bust(self):
        return self.get_value() > 21

    def __str__(self):
        return f"{self.cards} (value: {self.get_value()})"

def dealer_play(shoe, dealer_hand):
    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(shoe.deal_card())


def resolve_hand(shoe, player_hand, dealer_hand):
    if player_hand.is_bust():
        return -1, "Loss"

    dealer_play(shoe, dealer_hand)

    if dealer_hand.is_bust():
        return 1, "Win"

    if player_hand.get_value() > dealer_hand.get_value():
        return 1, "Win"
    elif player_hand.get_value() < dealer_hand.get_value():
        return -1, "Loss"
    else:
        return 0, "Draw"


def play_game(shoe, player_hand, dealer_hand, player_bets):
    result_value, outcome = resolve_hand(shoe, player_hand, dealer_hand)
    player_bets += result_value
    return player_hand, dealer_hand, player_bets, outcome


def start_game(shoe, player_choice=None):
    if len(shoe.cards) < 100:
        shoe.build_shoe()

    player_hand = Hand()
    dealer_hand = Hand()

    player_hand.add_card(shoe.deal_card())
    player_hand.add_card(shoe.deal_card())
    dealer_hand.add_card(shoe.deal_card())
    dealer_hand.add_card(shoe.deal_card())

    player_hand_org = copy.deepcopy(player_hand)
    dealer_hand_org = copy.deepcopy(dealer_hand)

    player_bets = 0

    if not player_hand.is_bust():
        if player_choice is None:
            player_choice = input("Enter H to hit or S to stand: ").upper()
        else:
            player_choice = player_choice.upper()

        if player_choice == "H":
            player_hand.add_card(shoe.deal_card())
        elif player_choice == "S":
            pass
        else:
            print("Invalid choice. Standing by default.")
            player_choice = "S"

    player_hand, dealer_hand, player_bets, outcome = play_game(
        shoe, player_hand, dealer_hand, player_bets
    )

    return (
        player_hand_org,
        dealer_hand_org,
        player_choice,
        player_hand,
        dealer_hand,
        player_bets,
        outcome
    )


def play_blackjack():
    shoe = Shoe()
    total_money = 0

    while True:
        print("\n--- New Hand ---")

        (
            player_start,
            dealer_start,
            choice,
            final_player,
            final_dealer,
            hand_result,
            outcome
        ) = start_game(shoe)

        total_money += hand_result

        print("Player starting hand:", player_start)
        print("Dealer showing:", dealer_start.cards[0])
        print("Player choice:", choice)
        print("Final player hand:", final_player)
        print("Final dealer hand:", final_dealer)
        print("Outcome:", outcome)
        print("Running total: $", total_money)

        again = input("Play again? (Y/N): ").upper()
        if again != "Y":
            break

def simulate(num_hands=100000):
    shoe = Shoe()
    results = {}

    for _ in range(num_hands):
        player = Hand()
        dealer = Hand()

        player.add_card(shoe.deal_card())
        player.add_card(shoe.deal_card())
        dealer.add_card(shoe.deal_card())
        dealer.add_card(shoe.deal_card())

        player_start = player.get_value()
        dealer_upcard = dealer.cards[0]

        action = random.choice(["HIT", "STAND"])

        if action == "HIT":
            player.add_card(shoe.deal_card())

        result_value, _ = resolve_hand(shoe, player, dealer)

        key = (player_start, dealer_upcard, action)

        if key not in results:
            results[key] = {
                "Wins": 0,
                "Losses": 0,
                "Draws": 0,
                "Net": 0
            }

        if result_value == 1:
            results[key]["Wins"] += 1
        elif result_value == -1:
            results[key]["Losses"] += 1
        else:
            results[key]["Draws"] += 1

        results[key]["Net"] += result_value

    return results


def print_table(results):
    print("\nPLAYER | DEALER | ACTION | WINS | LOSSES | DRAWS | NET")
    print("--------------------------------------------------------")

    for key in sorted(results):
        player_start, dealer_upcard, action = key
        row = results[key]

        print(
            f"{player_start:>6} | "
            f"{dealer_upcard:>6} | "
            f"{action:>6} | "
            f"{row['Wins']:>4} | "
            f"{row['Losses']:>6} | "
            f"{row['Draws']:>5} | "
            f"{row['Net']:>3}"
        )

def generate_results_table(num_hands=10):
    shoe = Shoe()
    data_results = []

    headers = [
        'player_hand_org',
        'dealer_hand_org',
        'player_choice',
        'player_hand',
        'dealer_hand',
        'player_bets',
        'outcome'
    ]

    for _ in range(num_hands):
        (
            player_hand_org,
            dealer_hand_org,
            player_choice,
            player_hand,
            dealer_hand,
            player_bets,
            outcome
        ) = start_game(shoe, random.choice(["H", "S"]))

        data_results.append([
            player_hand_org.cards,
            dealer_hand_org.cards,
            player_choice,
            player_hand.cards,
            dealer_hand.cards,
            player_bets,
            outcome
        ])

    df = pd.DataFrame(data_results, columns=headers)
    return df

if __name__ == "__main__":
    print("1 = Play game")
    print("2 = Run simulation")
    print("3 = Show pandas results table")

    choice = input("Choose: ")

    if choice == "1":
        play_blackjack()
    elif choice == "2":
        results = simulate(100000)
        print_table(results)
    elif choice == "3":
        blackjack_df = generate_results_table(10)
        print(blackjack_df)
    else:
        print("Invalid choice.")