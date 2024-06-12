# PvC

"""
Title: PvC Full GAME
Author: V3N0M
Date: 30 May 2024
"""
import ast
import Game
import w_PVP  # Need those functions
import random
from time import sleep
import csv
import os

PLAYER_DATA_FILE = "a_Player_data.csv"
SHOP_ITEMS_FILE = "a_shop_items.csv"

# Load player data
def load_player_data(file=PLAYER_DATA_FILE):
    if not os.path.exists(file):
        print("Player data file not found. Creating a new one.")
        player_data = {'EXP': 0, 'Gold': 0, 'Inventory': init_inventory()}
        save_player_data(player_data, file)
    else:
        with open(file, 'r') as f:
            reader = csv.DictReader(f)
            data = next(reader)
            player_data = {
                'EXP': int(data['EXP']),
                'Gold': int(data['Gold']),
                'Inventory': {
                    'Weapon': ast.literal_eval(data['Weapon']) if data['Weapon'] != 'None' else None,
                    'Armour': ast.literal_eval(data['Armour']) if data['Armour'] != 'None' else None,
                    'Accessory': ast.literal_eval(data['Accessory']) if data['Accessory'] != 'None' else None
                }
            }
    return player_data

# Save player data
def save_player_data(data, file=PLAYER_DATA_FILE):
    data['EXP'] = int(data['EXP'])
    data['Gold'] = int(data['Gold'])
    with open(file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['EXP', 'Gold', 'Weapon', 'Armour', 'Accessory'])
        writer.writeheader()
        row = {
            'EXP': data['EXP'],
            'Gold': data['Gold'],
            'Weapon': repr(data['Inventory']['Weapon']) if data['Inventory']['Weapon'] else 'None',
            'Armour': repr(data['Inventory']['Armour']) if data['Inventory']['Armour'] else 'None',
            'Accessory': repr(data['Inventory']['Accessory']) if data['Inventory']['Accessory'] else 'None'
        }
        writer.writerow(row)

# Load shop items
def load_shop_items(file=SHOP_ITEMS_FILE):
    with open(file, 'r', newline='') as f:
        return list(csv.DictReader(f))

# Display shop items
def display_shop_items(items):
    categories = {'Weapon': [], 'Armour': [], 'Accessory': []}
    for index, item in enumerate(items, start=1):
        categories[item['Type']].append((index, item))
    for category, items in categories.items():
        print(f"{category}s:")
        for index, item in items:
            print(f"{index}. {item['Name']} | {item['Type']} | {item['Effect']} | Cost: {item['Cost']} Gold")
        print()
# Buy item from shop
def buy_item(shop_items, player_data):
    display_shop_items(shop_items)

    try:
        choice = int(input("Enter the index of the item you want to buy: ")) - 1
        if 0 <= choice < len(shop_items):
            item = shop_items[choice]
            item_category = item['Type']
            item['Cost'] = int(item['Cost'])
            # Ensure player data inventory has the structure
            if player_data['Inventory'][item_category] is not None:
                print(f"You already have an item in the {item_category} slot.")
                return

            if player_data['Gold'] >= item['Cost']:
                player_data['Gold'] -= item['Cost']
                player_data['Inventory'][item_category] = item
                print(f"You have bought {item['Name']} and placed it in the {item_category} slot.")
                save_player_data(player_data)
            else:
                print("You do not have enough gold to buy this item.")
        else:
            print("Invalid choice. Please select a valid item index.")
    except ValueError:
        print("Invalid input. Please enter a number.")


# Initialize inventory
def init_inventory():
    return {'Weapon': None, 'Armour': None, 'Accessory': None}

# Display inventory
def display_inventory(inventory):
    print("----- Inventory -----")
    for idx, (category, item) in enumerate(inventory.items(), 1):
        if item:
            print(f"{idx}. {category}: {item['Name']} | {item['Type']} | {item['Effect']} | Cost: {item['Cost']} | Durability: {item['Durability']}")
        else:
            print(f"{idx}. {category}: None")
    print()



def execute_action_AI(action, attacker, defender, round_counter):
    if action == 1:
        return w_PVP.use_spell(attacker, defender, 'Spell_1', 'Damage_1', 'MP_1')  # makes the Ai always able to use a spell
    elif action == 2:
        return w_PVP.use_spell(attacker, defender, 'Spell_2', 'Damage_2', 'MP_2')
    elif action == 3 and round_counter >= int(attacker['Rounds_Ult']):
        attacker['ults_available'] -= 1
        attacker['rounds_until_ult'] = int(attacker['Rounds_Ult'])
        return w_PVP.use_ultimate(attacker, defender)
    elif action == 4:
        attacker['dodge'] = True
        print(f"{attacker['Character']} is preparing to dodge the next attack.")
        return True
    elif action == 3 and round_counter < int(attacker['Rounds_Ult']):
        return w_PVP.use_spell(attacker, defender, 'Spell_1', 'Damage_1', 'MP_1')
    elif action == 5:
        trash_talk = random.randint(1,5)
        if trash_talk == [1 or 2]:
            w_PVP.trash_talk(attacker,defender)
        elif trash_talk ==[3 or 4 or 5]:
            random_spell = random.randint(1, 2)
            if random_spell == 1:
                return w_PVP.use_spell(attacker, defender, 'Spell_1', 'Damage_1', 'MP_1')
            elif random_spell == 2:
                return w_PVP.use_spell(attacker, defender, 'Spell_2', 'Damage_2', 'MP_2')



# Equip item
def equip_item(inventory, item):
    category = item['Type']
    if category in inventory:
        if inventory[category]:
            print(f"You already have {inventory[category]['Name']} equipped as {category}. Replace it? (y/n)")
            if input("> ").strip().lower() == 'y':
                inventory[category] = item
                print(f"{item['Name']} equipped as {category}.")
            else:
                print(f"{item['Name']} not equipped.")
        else:
            inventory[category] = item
            print(f"{item['Name']} equipped as {category}.")
    else:
        print("Invalid item type.")

# Function to check if inventory is empty
def is_inventory_empty(inventory):
    # Check if all items in the inventory are None
    return all(item is None for item in inventory.values())

# Remove item
def remove_item(inventory, player_data):
    if not inventory or all(item is None for item in inventory.values()):
        print("Inventory is empty.")
        return

    # Display the inventory
    display_inventory(inventory)

    categories = list(inventory.keys())
    print("Select the category of the item you want to sell (50% back):")
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category}")

    try:
        category_choice = int(input("> ")) - 1
        if 0 <= category_choice < len(categories):
            category = categories[category_choice]
            item = inventory.get(category)
            if item:
                name = item.get('Name', 'None')
                cost = item.get('Cost', '0')

                print(f"Removed {name} from {category}.")
                price = int(cost) / 2
                player_data['Gold'] += price
                inventory[category] = None
                print(f"You received {round(price, 0)} gold back.")
            else:
                print(f"No items in {category}.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")

# Select AI opponent difficulty
def ai_opponent_difficulty():
    difficulties = [
        "Easy (Stats * 1.0)",
        "Medium (Stats * 1.5)",
        "Hard (Stats * 2.0)",
        "Very Hard (Stats * 3.0)",
        "Impossible (Stats * 5.0)",
        "Asian (Stats * 10.0)"
    ]
    print("Select AI Difficulty:")
    for i, difficulty in enumerate(difficulties, 1):
        print(f"{i}. {difficulty}")

    try:
        choice = int(input("> "))
        if 1 <= choice <= 6:
            title = difficulties[choice - 1].split(' (')[0].strip()
            return choice, title
        else:
            return ai_opponent_difficulty()
    except ValueError:
        return ai_opponent_difficulty()

# Modify stats based on difficulty
def modify_stats(character, difficulty):
    multipliers = {1: 1.0, 2: 1.5, 3: 2.0, 4: 3.0, 5: 5.0, 6: 10.0}
    multiplier = multipliers.get(difficulty, 1.0)
    modified_character = character.copy()
    modified_character['max_HP'] = int(character['HP'])
    modified_character['max_MP'] = int(character['MP'])
    stats_to_modify = ['HP', 'MP', 'Damage_1', 'Damage_2', 'Damage_Ult']
    if multiplier != 1:
        for stat in stats_to_modify:
            if stat in character:
                modified_character[stat] = int(character[stat]) * multiplier
            print(f"Modified {stat} from {int(character[stat])} to {int(character[stat]) * multiplier}")
        return modified_character
    else:
        for stat in stats_to_modify:
            if stat in character:
                modified_character[stat] = int(character[stat]) * multiplier
        return modified_character
def choose_character(characters, taken_characters, player_type):
    while True:
        print(f"\n{player_type}, choose your character:")
        for idx, char in enumerate(characters):
            if char['Character'] not in taken_characters:
                print(f"{idx + 1}. {char['Character']}")
        try:
            choice = int(input("> ")) - 1
            if 0 <= choice < len(characters):
                chosen_char = characters[choice]
                if chosen_char['Character'] in taken_characters:
                    print("Character already taken, choose another.")
                else:
                    taken_characters.append(chosen_char['Character'])
                    return chosen_char
            else:
                print("Error: Invalid choice try again.")
        except ValueError:
            print("Invalid input")


def apply_inventory_effects(character, item):
    if 'Equipped_Items' not in character:
        character['Equipped_Items'] = set()

    category = item['Type']

    if category in character['Equipped_Items']:
        print(f"{item['Name']} is already in use.")
        return

    for effect in item['Effect'].split(','):
        try:
            stat, value = effect.split()
            if '%' in value:
                value = float(value.strip('%')) / 100
            else:
                value = int(value)

            if stat == 'ATK':
                print(f"Old ATK: Damage_1 = {character['Damage_1']}, Damage_2 = {character['Damage_2']}, Damage_Ult = {character['Damage_Ult']}")
                character['Damage_1'] = str(int(float(character['Damage_1']) * (1 + value)))
                character['Damage_2'] = str(int(float(character['Damage_2']) * (1 + value)))
                character['Damage_Ult'] = str(int(float(character['Damage_Ult']) * (1 + value)))
                print(f"Applied ATK effect: Damage_1 = {character['Damage_1']}, Damage_2 = {character['Damage_2']}, Damage_Ult = {character['Damage_Ult']}")
            elif stat == 'SHIELD':
                print(f"Old Shield: HP = {character['HP']}")
                character['HP'] = str(int(float(character['HP']) * (1 + value)))
                print(f"Applied SHIELD effect: HP = {character['HP']}")
            elif stat == 'HP':
                print(f"Old HP = {character['HP']}")
                character['HP'] = str(int(float(character['HP']) + value))
                print(f"Applied HP effect: HP = {character['HP']}")
            elif stat == 'MP':
                print(f"Old MP = {character['MP']}")
                character['MP'] = str(int(float(character['MP']) + value))
                print(f"Applied MP effect: MP = {character['MP']}")
            else:
                print(f"Unknown stat effect: {stat}")
        except ValueError as e:
            print(f"Error processing effect '{effect}': {e}")

    character['Equipped_Items'].add(category)

    # Reduce durability
    durability = int(item['Durability'])
    if durability > 1:
        # Calculate chance to break based on durability
        chance_to_break = 100 / durability
        if random.randint(1, 100) <= chance_to_break:
            print(f"{item['Name']} broke!")
            # Remove the item from the inventory
            return None
        else:
            item['Durability'] = str(durability - 1)
            print(f"Durability reduced to {item['Durability']}")
    elif durability == 1:
        print(f"{item['Name']} is one-time use and broke!")
        # Remove the item from the inventory
        return None
    else:
        print(f"{item['Name']} is already broken!")
    return item


def use_item(character, inventory, used_categories):
    display_inventory(inventory)
    try:
        item_index = int(input("Enter the index of the item you want to use: ")) - 1

        if 0 <= item_index < len(inventory):
            category, item = list(inventory.items())[item_index]
            if item:
                if category in used_categories:
                    print(f"{item['Name']} is already in use.")
                else:
                    updated_item = apply_inventory_effects(character, item)
                    if updated_item is None:
                        print(f"{item['Name']} has broken!")
                        inventory[category] = None
                    else:
                        inventory[category] = updated_item
                    used_categories.add(category)
                    return item
            else:
                print(f"No item in the {category} category.")
        else:
            print("Invalid item index.")
    except ValueError:
        print("Invalid input.")


# Battle function
def battle(player_data, inventory):
    w_PVP.init_taken_characters()
    strenghts = w_PVP.load_element_strengths(w_PVP.EL_STR)
    weakness = w_PVP.load_element_weaknesses(w_PVP.EL_WEAK)
    characters = Game.load_characters("a_Character_Sheet.csv")
    w_PVP.display_characters_less_detailed(characters)
    player_character = w_PVP.select_character(characters, 'Human')
    ai_difficulty, ai_title = ai_opponent_difficulty()
    reward = ai_difficulty * random.randint(3,20)
    used_categories = set()
    if input("Choose AI or Not?(Y)").strip().upper() == 'Y':
        ai_character = w_PVP.select_character(characters, "AI")
        reward = reward / 5
    else:
        ai_character = random.choice(characters)
        print(f"AI has chosen {ai_character['Character']}")

    def initialize_character(character):
        character['dodge'] = False
        character['rounds_until_ult'] = int(character.get('Rounds_Ult', 0))
        character['ults_available'] = 0
        character['round_counter'] = 0
        character['max_HP'] = character['HP']
        character['max_MP'] = character['MP']

    initialize_character(player_character)
    initialize_character(ai_character)

    ai_character = modify_stats(ai_character, ai_difficulty)
    ai_character['MP_1'] = 1
    print(f"You have chosen Mode {ai_difficulty}: {ai_title} Mode")
    for _ in range(10):  # underscore just means there is nothing like an "i"
        if input(f"{'\033[04m'}{'\033[0;31m'}Do you want to use an item({'\033[0;32m'}y): {'\033[0m'}").strip().lower() != 'y':
            break
        use_item(player_character, inventory, used_categories)

    round_counter = 0
    while int(player_character['HP']) > 0 and int(ai_character['HP']) > 0:
        round_counter += 1

        print(f"\n--- Round {round_counter} ---")
        sleep(0.3)

        print(f"Player: {player_character['Character']}'s turn")
        sleep(0.1)
        w_PVP.print_player_status(player_character)
        w_PVP.apply_elemental_buff(player_character, ai_character, strenghts, weakness)

        action_success = False
        while not action_success:
            action = w_PVP.choose_action(player_character)
            action_success = w_PVP.execute_action(action, player_character, ai_character, round_counter)

        if int(ai_character['HP']) <= 0:
            print(f"\n{ai_character['Character']} is defeated! You win!")
            player_data['EXP'] += 100 * reward
            player_data['Gold'] += 50 * reward
            print(f"You gained {50 * reward} gold and {100 * reward} EXP")
            break

        print(f"\nAI: {ai_character['Character']}'s turn")
        sleep(0.1)
        w_PVP.print_player_status(ai_character)
        ai_action = random.randint(3, 3)
        w_PVP.apply_elemental_buff(ai_character, player_character, strenghts, weakness)
        execute_action_AI(ai_action, ai_character, player_character, round_counter)

        if int(player_character['HP']) <= 0:
            print(f"\n{player_character['Character']} is defeated! You lose!")
            player_data['Gold'] = max(0, player_data['Gold'] - 10 * (1 / reward))
            print(f"You lost {int(10 * (1 / reward))} gold. Loser")
            break

        for player in [player_character, ai_character]:
            player['round_counter'] += 1
            player['rounds_until_ult'] -= 1
            if player['rounds_until_ult'] <= 0:
                player['ults_available'] += 1
                player['rounds_until_ult'] = int(player.get('Rounds_Ult', 0))
    save_player_data(player_data, PLAYER_DATA_FILE)
