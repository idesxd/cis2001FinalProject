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
        dealer_upcard = dealer.cards[0]   # string like 'K', '7', etc.

        action = random.choice(["HIT", "STAND"])

        if action == "HIT":
            player.add_card(shoe.deal_card())

        outcome_value, outcome_name = resolve_simulated_hand(shoe, player, dealer)

        key = (player_start, dealer_upcard, action)

        if key not in results:
            results[key] = {
                "Wins": 0,
                "Losses": 0,
                "Draws": 0,
                "Net": 0
            }

        if outcome_value == 1:
            results[key]["Wins"] += 1
        elif outcome_value == -1:
            results[key]["Losses"] += 1
        else:
            results[key]["Draws"] += 1

        results[key]["Net"] += outcome_value

    return results


def resolve_simulated_hand(shoe, player_hand, dealer_hand):
    if player_hand.is_bust():
        return -1, "Loss"

    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(shoe.deal_card())

    if dealer_hand.is_bust():
        return 1, "Win"

    if player_hand.get_value() > dealer_hand.get_value():
        return 1, "Win"
    elif player_hand.get_value() < dealer_hand.get_value():
        return -1, "Loss"
    else:
        return 0, "Draw"


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
