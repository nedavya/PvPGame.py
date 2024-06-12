# Final Project
"""
Title: Role system w_PVP
Author: V3N0M
Date: 27 May 2024
"""
import os

import Casino

# --- NOTES --- #
# Block tactic that reduces incoming damage(random) but you cant attack that turn (for predicting ultimates)
# No healing, only offensive gameplay
# Trash talk tactic
# --- CODE --- #
import w_PVP
import x_PvC
from time import sleep
import csv
# import pygame for future
Character_Sheet = "a_Character_Sheet.csv"
SHOP_ITEMS_FILE = "a_shop_items.csv"
Elements = "a_Element_Affinities_Weak.csv"
# Inputs
def Options():
    print('''\33[0;35mPlease choose an option from the following
1. PVP
2. PvC
3. View Instructions
4. View Characters
5. Character Switch
6. Exit
''')
    try:
        Choice = input(">")
        Choice = int(Choice)
        if 0 < Choice < 7:
            return Choice
        else:
            print("Error please choose a Valid Choice")
            return Options()
    except ValueError:
        print("Error please choose a Valid Choice")
        return Options()

def Chosen(Option):
    if Option == 1:
        return PVP()
    elif Option == 2:
        return PvC()
    elif Option == 3:
        Instructions()
    elif Option == 4:
        characters()
    elif Option == 5:
        Add_Modify(Character_Sheet)
    elif Option == 6:
        print("Have a nice day")
        exit()
    else:
        return Options()

def Add_Modify(file):
    try:
        print("[A]dd | [M]odify | [D]elete")
        action = input(">").lower()
        if action == 'a':
            character_data = {}
            character_data['Character'] = input("Enter character name: ")
            elements = read_elements(Elements)
            print(" | ".join(elements))
            character_data['Element'] = input("Enter character element: ")
            character_data['HP'] = int(input("Enter character HP: "))
            character_data['MP'] = int(input("Enter character MP: "))
            character_data['Spell_1'] = input("Enter character Spell 1: ")
            character_data['Spell_2'] = input("Enter character Spell 2: ")
            character_data['Ultimate(Domain_Expansion)'] = input("Enter character Ultimate: ")
            character_data['Damage_1'] = int(input("Enter character Damage 1: "))
            character_data['Damage_2'] = int(input("Enter character Damage 2: "))
            character_data['Damage_Ult'] = int(input("Enter character Damage Ultimate: "))
            character_data['MP_1'] = int(input("Enter character MP for Spell 1: "))
            character_data['MP_2'] = int(input("Enter character MP for Spell 2: "))
            character_data['Rounds_Ult'] = int(input("Enter character Rounds for Ultimate: "))
            character_data['MP_Regain'] = int(input("Enter character MP Regain: "))

            with open(file, mode='a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=character_data.keys())
                if f.tell() == 0:
                    writer.writeheader()
                writer.writerow(character_data)
            print("Character added successfully.")
        elif action == 'm':
            with open(file, mode='r', newline='') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                for index, row in enumerate(rows, start=1):
                    print(f"{index}. {row['Character']}")
                index = int(input("Enter the index of the character you want to modify: ")) - 1

            character_data = rows[index]
            print("Enter new values (leave blank to keep existing values):")
            for key, value in character_data.items():
                if key == 'Element':
                    elements = read_elements(Elements)
                    print(" | ".join(elements))
                new_value = input(f"{key} [{value}]: ").strip()
                if new_value:
                    character_data[key] = new_value


            with open(file, mode='w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            print("Character modified successfully.")
        elif action == 'd':
            with open(file, mode='r', newline='') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                for index, row in enumerate(rows, start=1):
                    print(f"{index}. {row['Character']}")
                index = int(input("Enter the index of the character you want to delete: ")) - 1
            if 0 <= index < len(rows):
                deleted_character = rows.pop(index)
                print(f"Deleted character: {deleted_character['Character']}")
            else:
                print("Invalid index. No character deleted.")
            with open(file, mode='w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
                writer.writeheader()
                writer.writerows(rows)

            print("Character deleted successfully.")
        else:
            print("Invalid choice.")
    except Exception as e:
        return None


def PVP():
    strenghts = w_PVP.load_element_strengths(w_PVP.EL_STR)
    weakness = w_PVP.load_element_weaknesses(w_PVP.EL_WEAK)
    w_PVP.init_taken_characters()
    characters = load_characters(Character_Sheet)
    w_PVP.display_characters_less_detailed(characters)
    player1 = w_PVP.select_character(characters, 1)
    player1['max_HP'] = player1.get('HP')
    player1['max_MP'] = player1.get('MP')
    player2 = w_PVP.select_character(characters, 2)
    player2['max_HP'] = player2.get('HP')
    player2['max_MP'] = player2.get('MP')
    round_counter = 0
    while int(player1['HP']) > 0 and int(player2['HP']) > 0:
        round_counter += 1

        print(f"\n--- Round {round_counter} ---")
        sleep(0.3)

        print(f"Player 1: {player1['Character']}'s turn")
        print()
        sleep(0.1)
        w_PVP.apply_elemental_buff(player1, player2, strenghts, weakness)
        w_PVP.print_player_status(player1)
        action_success = False
        while not action_success:
            action = w_PVP.choose_action(player1)
            action_success = w_PVP.execute_action(action, player1, player2, round_counter)


        if int(player2['HP']) <= 0:
            print(f"\n{player2['Character']} is defeated! Player 1 wins!")
            break
        if int(player1['HP']) <= 0:
            print(f"\n{player1['Character']} is defeated! Player 2 wins!")
            break

        print(f"\nPlayer 2: {player2['Character']}'s turn")
        print()
        sleep(0.1)
        w_PVP.print_player_status(player2)
        action_success = False
        w_PVP.apply_elemental_buff(player2, player1, strenghts, weakness)
        while not action_success:
            action = w_PVP.choose_action(player2)
            action_success = w_PVP.execute_action(action, player2, player1, round_counter)

        for player in [player1, player2]:
            player['round_counter'] += 1
            player['rounds_until_ult'] -= 1
            if player['rounds_until_ult'] <= 0:
                player['ults_available'] += 1
                player['rounds_until_ult'] = int(player['Rounds_Ult'])
        if int(player1['HP']) <= 0:
            print(f"\n{player1['Character']} is defeated! Player 2 wins!")
            break
        if int(player2['HP']) <= 0:
            print(f"\n{player2['Character']} is defeated! Player 1 wins!")
            break


def PvC():

    player_data = x_PvC.load_player_data()
    inventory = player_data.get('Inventory', x_PvC.init_inventory())
    shop_items = x_PvC.load_shop_items()

    while True:
        print("PvC Campaign Mode")
        print(f"EXP: {player_data['EXP']} | Gold: {int(float(player_data['Gold']))}")
        print("1. Battle")
        print("2. Shop")
        print("3. View Inventory")
        print("4. Sell Item")
        print("5. Blackjack(50 EXP)")
        print("6. Save and Exit")

        try:
            choice = int(input("> "))
            if choice == 1:
                x_PvC.battle(player_data, inventory)
            elif choice == 2:
                x_PvC.buy_item(shop_items, player_data)
                x_PvC.display_inventory(inventory)
            elif choice == 3:
                x_PvC.display_inventory(inventory)
            elif choice == 4:
                x_PvC.remove_item(inventory, player_data)
                x_PvC.save_player_data(player_data)
            elif choice == 5:
                Casino.play_blackjack()
            elif choice == 6:
                break
            else:
                print("Invalid choice.")
        except ValueError:
            print("Invalid input.")


def characters():
    print("Here are all the characters in this game")
    char = load_characters(Character_Sheet)
    w_PVP.display_characters_info(char)

# Processing

def read_elements(file):
    elements = []
    with open(file, mode='r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            elements.append(row['Element'])
    return elements

def load_characters(File):
    character_data = []
    with open(File, 'r', newline='') as reading:
        reader = csv.DictReader(reading)
        for i in reader:
            character_data.append(i)
    return character_data

# Outputs
def Intro() -> None:
    print(rf'''{'\033[1m'}{'\033[0;34m'} __      __       .__                                
    /  \    /  \ ____ |  |   ____  ____   _____   ____   
    \   \/\/   _/ __ \|  | _/ ___\/  _ \ /     \_/ __ \  
     \        /\  ___/|  |_\  \__(  <_> |  Y Y  \  ___/  
      \__/\  /  \___  |____/\___  \____/|__|_|  /\___  > 
           \/       \/          \/            \/     \/{'\033[0m'}''')
    print(f"{'\033[1m'}{'\033[0;31m'}Please make sure to check out the instructions!{'\033[0m'}")
def Instructions():
    print(rf'''{'\033[1m'}{'\033[0;31m'}______________   _____________ 
\______   \   \ /   \______   \
 |     ___/\   Y   / |     ___/
 |    |     \     /  |    |    
 |____|      \___/   |____|{'\033[0m'}  

{'\033[0;35m'}")The PVP mode involves in fighting between a player side by side.
You both may choose characters, although they may not be duplicates.
You each have a domain expansion and 2 spells with corresponding damages.
Elementals and their random boosts to damage also play part as an extra boost to damage.{'\033[0m'}

{'\033[0;31m'}Here are all the Elements and their Strenghts:                               
Fire: Hero|Martial|Air
Earth: Water|Sigma|Ranged
Water: Dark|Fire|Ranged
Air: Martial|Water|Earth
Dark: Hero|Ranged|Special
Martial: Hero|Earth|Special
Hero: Dark|Special|Earth
Special: Sigma|Martial|Air
Ranged: Martial|Air|Earth
Sigma: Ranged|Fire|Martial{'\033[0m'}

{'\033[0;34m'}Here are all the Elements and their Weaknesses:
Hero: Fire|Martial|Dark
Martial: Fire|Air|Ranged
Air: Fire|Ranged|Special
Earth: Martial|Hero|Air
Water: Earth|Air|Martial
Dark: Earth|Water|Hero
Ranged: Earth|Water|Special
Special: Water|Hero|Martial
Fire: Water|Dark|Sigma
Sigma: Dark|Special|Martial{'\033[0m'}

{'\033[0;35m'}")You choose from a variety of characters: [An example of their components]:
Character|Element|HP|MP|Spell_1|Spell_2|Ultimate(Domain_Expansion)|Damage_1|Damage_2|Damage_Ult|MP_1|MP_2|Rounds_Ult|MP_Regain

You then have a MP and HP bar|status menu: showcasing the rounds until you can use an ultimate[Ultimates are stackable]

Next: There is an option to dodge: [Partial Dodge|Reflection|Complete Dodge|Fail to Dodge|]
There is also a final option with a 15% chance to instantly win[trash talk] | 85% chance to instant loss is the penalty.{'\033[0m'}")

______________   ____________  
\______   \   \ /   \_   ___ \ 
 |     ___/\   Y   //    \  \/ 
 |    |     \     / \     \____
 |____|      \___/   \______  /
                            \/ 
{'\033[4m'}MODE 1: BATTLE{'\033[0m'}
{'\033[0;35m'}")This mode functions similarily to PVP: 
You are facing off alone against a random AI with the aim to defeat you.
You can choose the AI's character or it will randomly choose(there is a 80% reward penalty if you choose the AI)
There are 6 difficulties:
1: EASY MODE (0.8)
2: MEDIUM MODE (1.5)
3: HARD MODE (2.0)
4: VERY HARD MODE (3.0)
5: IMPOSSIBLE MODE (5.0)
6: ASIAN MODE (10.0)

Each one increases the reward by its difficulty. 
The default reward is:[50 gold x AI difficulty x randint(1,4) + 100 EXP x AI difficulty x randint(1,4)]{'\033[0m'}
{'\033[4m'}MODE 2: SHOP{'\033[0m'}
{'\033[0;35m'}The shop functions through 3 categories(only 1 item per category)
There are 3 categories:[Weapon|Accessory|Armour]
The armour grants health as a shield which increases the max hp of the player
The accessory: can also do the same as an armour or a weapon or even do a unique function of MP[its 1-time use]
The effects dont stack
The weapon: increases damage all around
It costs a different amount of Gold for each item in the shop{'\033[0m'}
{'\033[4m'}MODE 3: Inventory{'\033[0m'}
{'\033[0;35m'}This functions to view the different categories and the weapons within them
It allows the user to check his inventory but its nothing special{'\033[0m'}
{'\033[4m'}MODE 4: Sell{'\033[0m'}
{'\033[4m'}Allows the user to sell items from the inventory{'\033[0m'}
{'\033[4m'}MODE 5: BlackJack{'\033[0m'}
{'\033[0;35m'}The user can use his EXP(50 per game) to play in the {'\033[0;31m'}CASINO{'\033[0;35m'}
The user can gamble with his gold and play this 'mini-game' to earn some gold
The gold and EXP currency is synced between the games{'\033[0m'}
{'\033[4m'}MODE 6: Exit{'\033[0m'}
{'\033[0;31m'}The user Exits the PVC section{'\033[0m'}
{'\033[1;35m'}_________ .__                                __                      
\_   ___ \|  |__ _____ ____________    _____/  |_  ___________ ______
/    \  \/|  |  \\__  \\_  __ \__  \ _/ ___\   ___/ __ \_  __ /  ___/
\     \___|   Y  \/ __ \|  | \// __ \\  \___|  | \  ___/|  | \\___ \ 
 \______  |___|  (____  |__|  (____  /\___  |__|  \___  |__| /____  >
        \/     \/     \/           \/     \/          \/          \/{'\033[0m'}
{'\033[0;35m'}Allows the Ussr to view all the characters within the game
Also allows the user to add/modify or delete characters through inputs.
Overall: Characters can be viewed and had fun around through the functions.{'\033[0m'}
{'\33[0;30m'}______________  __.______________
\_   _____\   \/  |   \__    ___/
 |    __)_ \     /|   | |    |   
 |        \/     \|   | |    |   
/_______  /___/\  |___| |____|   
        \/      \_/ 
EXITS THE PROGRAM{'\033[0m'}          
''')


# Main
if __name__ == '__main__':
    Intro()
    sleep(0.1)
    Characters = load_characters(Character_Sheet)
    while True:
        Option = Options()
        Chosen(Option)
        os.system('clear')



