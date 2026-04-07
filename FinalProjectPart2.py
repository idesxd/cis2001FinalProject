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

    # player's turn to play, they can choose to either stand or hit till they are not bust
    while not player_hand.is_bust():
        player_choice = input("Enter H to hit and S to stand :").upper()
        if player_choice == "H":
            player_hand.add_card(shoe.deal_card())
            print("Player Hand :", player_hand.cards)
        elif player_choice == "S":
            print("Player chooses to stand")
            break

    if player_hand.is_bust():
        print("Player busted, Dealer Wins!")
        player_bets -= 1
        return player_hand, dealer_hand, player_choice, player_bets

    # dealer's turn to play, they must hit till they reach a value of at least 17 and then they stand
    print("Dealer Hand :", dealer_hand.cards)
    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(shoe.deal_card())
        print("Dealer Hand :", dealer_hand.cards)

    if dealer_hand.is_bust():
        print("Dealer busted, Player Wins!")
        player_bets += 1
        return player_hand, dealer_hand, player_choice, player_bets

    # if neither dealer nor player are busted, compare the card values
    if player_hand.get_value() > dealer_hand.get_value():
        print("Player Wins!")
        player_bets += 1
    elif player_hand.get_value() < dealer_hand.get_value():
        print("Dealer Wins!")
        player_bets -= 1
    else:
        print("Tie!")

    return player_hand, dealer_hand, player_choice, player_bets

















