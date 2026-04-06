from FinalProjectPart1 import *

def play_game():
    shoe = Shoe()
    player_hand = Hand()
    dealer_hand = Hand()

    # 1. Initial dealing of two cards each for the dealer and player
    player_hand.add_card(shoe.deal_card())
    player_hand.add_card(shoe.deal_card())
    dealer_hand.add_card(shoe.deal_card())
    dealer_hand.add_card(shoe.deal_card())

    # both of the player's cards and first of the dealer's cards is made visible
    print("Player Hand :", player_hand.cards)
    print("Dealer Hand :", dealer_hand.cards[0])

    player_choice = ""
    player_bets = 0

    return player_hand, dealer_hand, player_choice, player_bets

















