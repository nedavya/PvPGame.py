# PVP

"""
Title: PVP secondary file
Author: V3N0M
Date: 29 May 2024
"""
import random
from time import sleep
import csv
EL_STR = "a_Element_Affinities_Strong.csv"
EL_WEAK = "a_Element_Affinities_Weak.csv"
taken_characters = []
def init_taken_characters():
    global taken_characters
    taken_characters = []

def load_element_strengths(file=EL_STR):
    strengths = {}
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            strengths[row['Element']] = [row['Strong_1'], row['Strong_2'], row['Strong_3']]
    return strengths

# Load element weaknesses from CSV file
def load_element_weaknesses(file=EL_WEAK):
    weaknesses = {}
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            weaknesses[row['Element']] = [row['Weak_1'], row['Weak_2'], row['Weak_3']]
    return weaknesses

def apply_elemental_buff(attacker, defender, strengths, weakness):
    attacker_element = attacker.get('Element')
    defender_element = defender.get('Element')
    buff_percentage = random.randint(10, 20)
    if defender_element in strengths.get(attacker_element, []):
        print(f"{attacker['Character']} has a {buff_percentage}% buff against {defender['Character']}")
        buff_percentage /= 100
        # Apply the buff to relevant stats
        attacker['Damage_1'] = str(int(int(attacker['Damage_1']) * (1 + buff_percentage)))
        attacker['Damage_2'] = str(int(int(attacker['Damage_2']) * (1 + buff_percentage)))
        attacker['Damage_Ult'] = str(int(int(attacker['Damage_Ult']) * (1 + buff_percentage)))
    elif attacker_element in weakness.get(defender_element, []):
        print(f"{defender['Character']} has a {buff_percentage}% buff against {attacker['Character']}")
def display_characters_less_detailed(characters):
    for index, character in enumerate(characters):
        try:
            print(f"Character {index + 1}: {character['Character']} | {character['HP']} HP | {character['MP']} MP")
        except KeyError as e:
            print(f"KeyError: {e} in character: {character}")

def create_bar(current, maximum, length=20, color = "white"):
    ratio = current / maximum
    filled_length = int(ratio * length)
    default = '\033[0m'
    color_code = '\033[0m' # white
    if color == 'green':
        color_code = '\033[92m'
    elif color == 'blue':
        color_code = '\033[94m'
    bar = color_code + '█' * filled_length + '_' * (length - filled_length) + default
    return bar


def print_player_status(player):
    if player.get('round_counter', 0) > 1:
        regenerate_mana_amount = regenerate_mana(player)
    else:
        regenerate_mana_amount = 0

    rounds_until_ult = player.get('rounds_until_ult', int(player['Rounds_Ult']))
    ults_available = player.get('ults_available', 0)

    # Format health and mana values without extra decimal places
    hp_formatted = "{:.0f}".format(float(player['HP']))
    mp_formatted = "{:.0f}".format(float(player['MP']))

    # Create HP and MP bars
    hp_bar = create_bar(int(player['HP']), int(player['max_HP']), color='green')
    mp_bar = create_bar(int(player['MP']), int(player['max_MP']), color='blue')

    # Print status with bars
    print(f"{'\33[0m'}-----STATUS-----")
    print(f"HP:  [{hp_bar}] {hp_formatted}/{player['max_HP']}")
    print(f"MP:  [{mp_bar}] {mp_formatted}/{player['max_MP']} (+{regenerate_mana_amount})")
    print(f"Rounds left till Ult: {rounds_until_ult} ({ults_available})")


def regenerate_mana(player):
    # Calculate mana regain amount
    regain_amount = int(player['MP_Regain'])
    # Increase player's mana by the mana regain amount
    player['MP'] = (int(player['MP']) + regain_amount)
    return regain_amount
def display_characters_info(characters):
    # Display a numbered list of characters
    print("Characters List:")
    for index in range(0, len(characters), 3):
        if index + 2 < len(characters):
            print(f"{index + 1}. {characters[index]['Character']}  |  {index + 2}. {characters[index + 1]['Character']}  |  {index + 3}. {characters[index + 2]['Character']}")
        elif index + 1 < len(characters):
            print(f"{index + 1}. {characters[index]['Character']}  |  {index + 2}. {characters[index + 1]['Character']}")
        else:
            print(f"{index + 1}. {characters[index]['Character']}")
        sleep(0.08)
    print(f"{len(characters) + 1}. All")
    print()

    # Get user input to select a character
    try:
        choice = int(input(f"Enter the index of the character you want to view:"))
        if choice < 1 or choice > len(characters) + 1:
            raise ValueError
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    # Check if user wants to view all characters
    if choice == len(characters)+1:
        selected_indices = range(len(characters))
    else:
        selected_indices = [int(choice) - 1]  # because it starts at 0
    for index in selected_indices:
        character = characters[index]
        max_hp = int(character['HP'])
        max_Mp = int(character['MP'])
        health_bar = create_bar(max_hp, max_hp, color='green')
        Mana_bar = create_bar(max_Mp, max_Mp, color='blue')

    # Display information for selected characters

    for index in selected_indices:
        character = characters[index]
        print(f"\033[0mCharacter {index + 1}: {character['Character']}")
        print(f"Class: {character['Element']}")
        print(f"HP: |{health_bar}| [{character['HP']}]")
        print(f"Mana:|{Mana_bar}| [{character['MP']}] | {character['MP_Regain']} GAIN")
        print("Spells:")
        print(f"{character['Spell_1']} | {character['Damage_1']} ATK | {character['MP_1']} MP")
        print(f"{character['Spell_2']} | {character['Damage_2']} ATK | {character['MP_2']} MP")
        print(
            f"Domain Expansion: {character['Ultimate(Domain_Expansion)']} | {character['Damage_Ult']} ATK | {character['Rounds_Ult']} ROUND\033[0;35m")
        print()  # Add an empty line for better readability
        sleep(0.5)

    if choice != len(characters)+1:
        try:
            redo = input("Would You like to view another character(Y):").upper()
            redo = str(redo)
            if redo == "Y":
                return display_characters_info(characters)
            else:
                return None
        except ValueError:
            return None


def select_character(characters, player_num):
    while True:
        try:
            choice = int(input(f"Player {player_num}: select your character by index: "))
            choice -= 1
            if 0 <= choice < len(characters):
                selected_character = characters[choice]
                if selected_character['Character'] not in taken_characters:
                    taken_characters.append(selected_character['Character'])
                    selected_character['dodge'] = False  # Initialize dodge status
                    selected_character['rounds_until_ult'] = int(selected_character['Rounds_Ult'])
                    selected_character['ults_available'] = 0
                    selected_character['round_counter'] = 0
                    print(f"Player {player_num} has selected {selected_character['Character']}!")
                    return selected_character
                else:
                    print("Error: This character has already been chosen by Player 1. Please choose another character.")
            else:
                print("Error: please choose a valid character index.")
        except ValueError:
            print("Error: please enter a number.")

def choose_action(character):
    print("Choose an action:")
    print(f"1. {character['Spell_1']} | {character['Damage_1']} ATK | {character['MP_1']} MP")
    print(f"2. {character['Spell_2']} | {character['Damage_2']} ATK | {character['MP_2']} MP")
    print(f"3. Domain Expansion: {character['Ultimate(Domain_Expansion)']} | {character['Damage_Ult']} ATK | {character['Rounds_Ult']} ROUND")
    print("4. Dodge")
    print("5. Trash Talk")
    while True:
        try:
            action = int(input("> "))
            if 1 <= action <= 5:
                return action
            else:
                print("Error: please choose a valid action.")
        except ValueError:
            print("Error: please enter a number.")


def use_spell(attacker, defender, spell_key, damage_key, mp_key):
    if 'dodge' not in defender:
        defender['dodge'] = False  # Initialize dodge status if not present
    if int(attacker['MP']) >= int(attacker[mp_key]):
        damage = int(attacker[damage_key])
        if defender['dodge']:
            print(f"{defender['Character']} attempted to dodge the attack!")
            dodge(attacker, defender, damage)
            defender['dodge'] = False
        else:
            defender['HP'] = str(max(0, int(defender['HP']) - damage))
            print(f"{attacker['Character']} used {attacker[spell_key]} causing {damage} damage to {defender['Character']}.")
        attacker['MP'] = str(int(attacker['MP']) - int(attacker[mp_key]))
        return True
    else:
        print("Not enough MP!")
        return False

def use_ultimate(attacker, defender):
    damage = int(attacker['Damage_Ult'])
    if defender['dodge']:
        print(f"{defender['Character']} attempted to dodge the attack!")
        dodge(attacker, defender, damage)
        defender['dodge'] = False
    else:
        defender['HP'] = str(max(0, int(defender['HP']) - damage))
        print(f"{attacker['Character']} used DOMAIN EXPANSION:{attacker['Ultimate(Domain_Expansion)']} dealing {damage} damage to {defender['Character']}.")
    return True

def dodge(attacker, defender, damage):
    '''
    Dodge mechanic using percentages
    :param attacker:  the player who currently is in turn
    :param defender:  the player who is not currently playing
    :param damage:  damage amount
    :return:
    '''
    chance = random.randint(1, 100)  # 1-100% chances
    if 1 <= chance <= 5: # 5% chance to reflect
        # Reflect damage
        defender['HP'] = str(max(0, int(defender['HP']) - damage))
        print(f"{defender['Character']} reflected the attack! {attacker['Character']} took {damage} damage.")
    elif 6 <= chance <= 25:
        # Fully dodge
        print(f"{defender['Character']} fully dodged the attack!")
    elif 26 <= chance <= 75:
        # Partially dodge
        partial_dodge = random.randint(30, 70) / 100.0  # 30-70% chance of damage being blocked
        actual_damage = int(damage * (1 - partial_dodge))
        defender['HP'] = str(max(0, int(defender['HP']) - actual_damage))
        print(f"{defender['Character']} partially dodged the attack! Took {actual_damage} damage instead of {damage}.")
    else:
        # Fail to dodge
        defender['HP'] = str(max(0, int(defender['HP']) - damage))
        print(f"{defender['Character']} failed to dodge and took {damage} damage.")
    return True

def trash_talk(attacker, defender):
    chance = random.randint(1, 100)
    if 0 <= chance <= 15:
        defender['HP'] = '0'
        print(f"{attacker['Character']} caused EMOTIONAL DAMAGE and {defender['Character']}! cried himself to death")
    else:
        attacker['HP'] = '0'
        print(f"{attacker['Character']} got cooked by {defender['Character']}! As a result he has been banished to the shadow realm")
    return True

def execute_action(action, attacker, defender, round_counter):
    if action == 1:
        return use_spell(attacker, defender, 'Spell_1', 'Damage_1', 'MP_1')
    elif action == 2:
        return use_spell(attacker, defender, 'Spell_2', 'Damage_2', 'MP_2')
    elif action == 3:
        if attacker['ults_available'] > 0:
            attacker['ults_available'] -= 1
            attacker['rounds_until_ult'] = int(attacker['Rounds_Ult'])
            return use_ultimate(attacker, defender)
        else:
            print("Ultimate Unavailable")
            print(f"Ultimate available in {attacker['rounds_until_ult']} rounds!")
            return False
    elif action == 4:
        attacker['dodge'] = True
        print(f"{attacker['Character']} is preparing to dodge the next attack.")
        return True
    elif action == 5:
        return trash_talk(attacker, defender)
