# Casino

"""
Title: Casino(part of PvC)
Author: V3N0M
Date: 11 June 2024
"""
import Game

PLAYER_DATA_FILE = "a_player_data.csv"

# ---- BlackJack ---- #
import random
import csv
import os
deck = []
player_hand = []
dealer_hand = []
player_points = 0
dealer_points = 0

def initialize_deck():
    """
    Initialize a deck of cards with 4 suits and 13 ranks each.
    """
    global deck
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    deck = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]


def deal_card(hand):
    """
    Deal a card from the deck and add it to the given hand.
    """
    global deck
    card = random.choice(deck)
    hand.append(card)
    deck.remove(card)

def calculate_points(hand):
    """
    Calculate the total points of a hand.
    """
    points = 0
    ace_count = 0
    for card in hand:
        rank = card['rank']
        if rank.isdigit():
            points += int(rank)
        elif rank in ['Jack', 'Queen', 'King']:
            points += 10
        elif rank == 'Ace':
            points += 11
            ace_count += 1
    while points > 21 and ace_count > 0:
        points -= 10
        ace_count -= 1
    return points

def display_hand(hand, is_dealer=False):
    """
    Display the cards in a hand along with the total points.
    """
    print("----Dealer Hand----" if is_dealer else "----Player Hand----")
    for card in hand:
        print(f"{card['rank']} of {card['suit']}")
    points = calculate_points(hand)
    print(f"Total Points: {points}")

def check_blackjack(hand):
    """
    Check if a hand has Blackjack (21 points with only 2 cards).
    """
    return len(hand) == 2 and calculate_points(hand) == 21

def player_turn():
    """
    Player's turn in the Blackjack game.
    """
    global player_hand, deck, player_points
    while True:
        display_hand(player_hand)
        player_points = calculate_points(player_hand)
        if player_points == 21:
            print("Blackjack! You win.")
            break
        elif player_points > 21:
            print(f"Bust! You lost {bet_gold} gold.")
            break
        choice = input("Do you want to [H]it or [S]tand?: ").lower()
        if choice == 'h':
            deal_card(player_hand)
        elif choice == 's':
            break

def dealer_turn():
    """
    Dealer's turn in the Blackjack game.
    """
    global dealer_hand, deck, dealer_points
    while calculate_points(dealer_hand) < 17:
        deal_card(dealer_hand)
    dealer_points = calculate_points(dealer_hand)

def check_winner():
    """
    Determine the winner of the Blackjack game.
    """
    global player_points, dealer_points
    if player_points > dealer_points:
        print("You win!")
    elif dealer_points > player_points:
        print("Dealer wins.")
    else:
        print("It's a tie.")

def load_player_data(file=PLAYER_DATA_FILE):
    """
    Load player data from a CSV file and initialize default values if necessary.
    """
    if not os.path.exists(file):
        print("Player data file not found. Creating a new one.")
        player_data = {'EXP': 0, 'Gold': 0, 'Weapon': None, 'Armour': None, 'Accessory': None}
        save_player_data(player_data, file)
    else:
        try:
            with open(file, 'r') as f:
                reader = csv.DictReader(f)
                data = next(reader)
                player_data = {
                    'EXP': int(data.get('EXP', 0)),  # Set default value if 'EXP' is missing
                    'Gold': int(data.get('Gold', 0)),  # Set default value if 'Gold' is missing
                    'Weapon': eval(data.get('Weapon', 'None')),  # Set default value if 'Weapon' is missing
                    'Armour': eval(data.get('Armour', 'None')),  # Set default value if 'Armour' is missing
                    'Accessory': eval(data.get('Accessory', 'None'))  # Set default value if 'Accessory' is missing
                }
        except (StopIteration, ValueError):
            print("Player data file is empty or corrupted.")
            player_data = {'EXP': 0, 'Gold': 0, 'Weapon': None, 'Armour': None, 'Accessory': None}
            save_player_data(player_data, file)

    return player_data

# Save player data
def save_player_data(data, file=PLAYER_DATA_FILE):
    """
    Save player data to a CSV file.
    """
    # Convert gold to integer
    data['Gold'] = int(data['Gold'])

    # Check if all required keys are present
    required_keys = ['EXP', 'Gold', 'Weapon', 'Armour', 'Accessory']
    if all(key in data for key in required_keys):
        with open(file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=required_keys)
            writer.writeheader()
            writer.writerow({
                'EXP': data['EXP'],
                'Gold': data['Gold'],
                'Weapon': repr(data['Weapon']),
                'Armour': repr(data['Armour']),
                'Accessory': repr(data['Accessory'])
            })
    else:
        print("Error: Missing required keys in player data. Saving aborted.")

def play_blackjack():
    """
    Play a round of Blackjack.
    """
    global deck, player_hand, dealer_hand, player_points, dealer_points
    player_data = load_player_data(PLAYER_DATA_FILE)
    if player_data['EXP'] < 50:
        print("You do not have enough EXP to play Blackjack.")
        return
    if player_data['Gold'] <= 50:
        print("You do not have enough Gold to play Blackjack. At least 50 gold is required")
        return
    initialize_deck()
    player_hand = []
    dealer_hand = []
    deal_card(player_hand)
    deal_card(player_hand)
    deal_card(dealer_hand)
    deal_card(dealer_hand)
    print("----BLACKJACK----")
    global bet_gold
    bet_gold = int(input("Enter the amount of gold you want to bet: "))
    if bet_gold > player_data['Gold']:
        print("Insufficient gold.")
        return
    elif bet_gold < 50:
        print("please enter more than 50 gold as a bet!")
        return

    player_data['EXP'] -= 50  # Deduct EXP cost for playing
    player_data['Gold'] -= bet_gold  # Deduct gold for the bet
    save_player_data(player_data)

    if check_blackjack(player_hand):
        display_hand(player_hand)
        print(f"Blackjack! You win {3*bet_gold} gold.")
        player_data['Gold'] += bet_gold * 3  # Double the bet for Blackjack win
        save_player_data(player_data)
        return  # Player won immediately
    else:
        display_hand(dealer_hand, is_dealer=True)
        player_turn()
        if player_points <= 21:
            dealer_turn()
            display_hand(dealer_hand, is_dealer=True)
            check_winner()
            if player_points > dealer_points:
                player_data['Gold'] += bet_gold * 2  # Double the bet for winning
                save_player_data(player_data)
            elif player_points < dealer_points:
                print(f"You lost {bet_gold} gold. Loser.")
                save_player_data(player_data)
            else:
                print("It's a tie. (The house always wins)")
        else:
            save_player_data(player_data, PLAYER_DATA_FILE)
    return Game.PvC()