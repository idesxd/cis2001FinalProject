from FinalProjectPart2 import *
from FinalProjectPart1 import *
import pandas as pd

def play_blackjack(sim_hands = 2):
    shoe = Shoe()
    data_results = []
    table_headers = ['player_hand_org', 'dealer_hand_org', 'player_choice', 'player_hand', 'dealer_hand', 'player_bets', 'outcome']

    for hands in range(sim_hands):
        player_hand_org, dealer_hand_org, player_choice, player_hand, dealer_hand, player_bets, outcome = start_game(shoe)
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

blackjack_df = play_blackjack()
print(blackjack_df)
