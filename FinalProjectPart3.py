def dealer_play(shoe, dealer_hand):

    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(shoe.deal_card())


def resolve_hand(shoe, player_hand, dealer_hand):

    if player_hand.is_bust():
        return -1

    dealer_play(shoe, dealer_hand)

    if dealer_hand.is_bust():
        return 1

    if player_hand.get_value() > dealer_hand.get_value():
        return 1

    elif player_hand.get_value() < dealer_hand.get_value():
        return -1

    else:
        return 0


def simulate(num_hands=100000):

    shoe = Shoe()

    results = {}

    for _ in range(num_hands):

        player = Hand()
        dealer = Hand()

        player.add_card(shoe.deal_card())
        dealer.add_card(shoe.deal_card())

        player.add_card(shoe.deal_card())
        dealer.add_card(shoe.deal_card())

        player_start = player.get_value()

        dealer_upcard = dealer.cards[0].value

        action = random.choice(["HIT", "STAND"])

        if action == "HIT":
            player.add_card(shoe.deal_card())

        result = resolve_hand(shoe, player, dealer)

        key = (player_start, dealer_upcard, action)

        if key not in results:
            results[key] = 0

        results[key] += result

    return results


def print_table(results):

    print("\nPLAYER | DEALER | ACTION | NET RESULT")
    print("--------------------------------------")

    for key in sorted(results):

        p, d, a = key

        print(p, d, a, results[key])


if __name__ == "__main__":

    print("1 = Play game")
    print("2 = Run simulation")

    choice = input("Choose: ")

    if choice == "1":
        play_blackjack()

    else:

        results = simulate(100000)

        print_table(results)