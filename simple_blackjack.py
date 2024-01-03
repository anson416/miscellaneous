# -*- coding: utf-8 -*-
# File: simple_blackjack.py

"""
### Requirements:

```text
simple_term_menu
```

### Usage:

```bash
python simple_blackjack.py [-s SEED]
```
"""

import argparse
import random
import sys
from itertools import product

from simple_term_menu import TerminalMenu

CARD_DECK = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"] * 16
PICTURE_CARDS = {"J", "Q", "K"}


def get_cards_sum(cards: list[str]) -> int:
    total, n_ace = 0, 0
    for card in cards:
        if card == "A":
            n_ace += 1
        else:
            total += 10 if card in PICTURE_CARDS else int(card)
    aces = map(sum, product((1, 11), repeat=n_ace))
    combs = tuple(filter(lambda x: x <= 21, map(lambda a: a + total, aces)))
    return max(combs) if len(combs) else 22


def main() -> None:
    ordered_deck = random.sample(CARD_DECK, len(CARD_DECK))
    player_cards, dealer_cards = [], []
    for _ in range(2):
        player_cards.append(ordered_deck.pop(0))
        dealer_cards.append(ordered_deck.pop(0))
    
    # Initial cards
    player_sum, dealer_sum = get_cards_sum(player_cards), get_cards_sum(dealer_cards)
    print(f"Your hand value is {player_sum} ({', '.join(player_cards)}).")
    print(f"Dealer has ? and {dealer_cards[1]}.")

    # Blackjack
    if player_sum == 21:
        print(f"Dealer's hand value is {dealer_sum} ({', '.join(dealer_cards)}).")
        print("Push!" if dealer_sum == 21 else "Blackjack! You won!")
        sys.exit(0)

    # Player's turn
    while player_sum < 21:
        choice = TerminalMenu(("Stand", "Hit")).show()
        if choice:
            player_cards.append(ordered_deck.pop(0))
            player_sum = get_cards_sum(player_cards)
            print(f"You hit.\nYour hand value is {player_sum} ({', '.join(player_cards)}).")
        else:
            print(f"You stood.")
            break
    else:
        if player_sum > 21:
            print("You busted!")
            sys.exit(0)

    # Dealer's turn
    print(f"Dealer's hand value is {dealer_sum} ({', '.join(dealer_cards)}).")
    while dealer_sum <= max(player_sum, 17) and dealer_sum < 21:
        dealer_cards.append(ordered_deck.pop(0))
        dealer_sum = get_cards_sum(dealer_cards)
        print(f"Dealer hit.\nDealer's hand value is {dealer_sum} ({', '.join(dealer_cards)}).")
    else:
        if player_sum == dealer_sum:
            print("Push!")
        elif dealer_sum > 21:
            print("Dealer busted! You won!")
        else:
            print("You lost!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--seed", type=int, default=None,
        help="Seed for random number generator. Defaults to None.",
    )
    args = parser.parse_args()

    random.seed(args.seed)
    main()
