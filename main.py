import time 
import pandas as pd
import json
import os
import random as r

'''
Areas - add areas that pets can be found in
Pet battles - add helmets/armour and weapon - once function is being added, create CSV called armour.csv and weapons.csv

Save file layout
name
materials
pets - pet informations - armour - weapons
'''

def data_load():
    pets = pd.read_csv('data/pets.csv')
    return pets

def save(save_file:dict, player_pets:dict):

    save_file['pets'] = player_pets

    with open("data/save_file.json", "w") as file:
        json.dump(save_file, file)
 
def save_load():
    with open("data/save_file.json") as json_file:
        json_data = json.load(json_file)

    return json_data


def chance(percent:float):
    chance_val = r.random() # Creates a random number between 0 and 1

    if chance_val <= percent: 
        return True
    else:
        return False


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def input_check(input1:int, top:int): # I noticed for input validation, this was cropping up alot, so ive writen its own funtion
    input_flag = True

    if top == 2:
        if input1 not in [1, 2]:
            print('that is not a valid input')
        else:
            input_flag = False
    else:
        if input1 not in range(1, top+1):
            print('that is not a valid input')
        else:
            input_flag = False

    return input_flag



def main_menu():
    flag = True

    player_pets = {}
    save_file = {"name":'bob'}

    while flag:
        time.sleep(2)
        clear()
        print('Welcome to Pet Adventures')
        print('Pick an action')

        try:
            choice = int(input('1. Load Save\n2. New Game\n3. Quit\n'))
            flag = input_check(choice, 3)
        except:
            print("nuh uh")

        
    match choice:
        case 1:
            save_file = save_load()
            player_pets = save_file['pets']
            while True:
                menu_select(save_file, player_pets)
        case 2:
            while True:
                menu_select(save_file, player_pets)
        case 3:
            exit()

def menu_select(save_file:dict, player_pets:dict):
    flag = True

    save_file = {'name':save_file['name']}

    while flag:
        time.sleep(2)
        clear()
        print('Pick an action')

        try:
            choice = int(input('1. Travel\n2. Manage Areas\n3. Manage Pets\n4. Save\n5. Save and Quit\n'))
            flag = input_check(choice, 6)
        except:
            print("nuh uh")

        
    match choice:
        case 1:
            pet = [None, 0, 0, None]

            while pet[3] != True:
                pet = travel(player_pets, pet[1], pet[2])

                if pet[0] != None:
                    slot = str(len(player_pets))
                    player_pets[slot] = pet[0]
                    print(player_pets)

        case 2:
            area_manage()
        case 3:
            pets_manage(player_pets)
        case 4:
            save(save_file, player_pets)
        case 5:
            save(save_file, player_pets)
            exit()




def travel(player_pets:dict, travels = 0, area = 0):
    out = False # catches if the user doesnt want to continue traveling and doesnt remove the last pet hey caught if they choose to leave after catching a last pet
    areas = ['Plains', 'Forest', 'Mountains']

    # encounter chance, if it is true, you encounter a pet
    enc = chance(0.5)

    if enc:
        pet = encounter(area, player_pets)
    else:
        print('You travel, but dont find anything')
        pet = None

    flag_input = True
    while flag_input:
        travels += 1
        time.sleep(2)
        clear()
        try:
            again = int(input('Would you like to\n1. Continue Traveling\n2. Return Home\n'))
            flag_input = input_check(again, 2)
            if again == 2:
                out = True 
            else:
                out = False
        except:
            print('nuh uh')

        if travels == 10:
            area = 1
            print(f'You are entering {areas[area]}')
        if travels == 20:
            area = 1
            print(f'You are entering {areas[area]}')

    return [pet, travels, area, out]

def encounter(area:int, player_pets:dict):
    int_input = True
    # Single function to control pet encounters

    #Loads pet data CSV
    pets = data_load()

    pets = pets.where(pets['Area'] <= area)

    pet_id = r.randint(0, len(pets)-1) # future change to area based, and use the range of area_pets

    # create area variable, with part of the CSV containing the are the pets spawn, 1 area per pet
    # Encounter func takes area variable

    # area_pets = pets.loc[area]

    pet_data = pets.loc[pet_id]
    clear()
    print(f'You encounter a {pet_data.Name}')

    while int_input:
        try:
            if len(player_pets) == 0:
                action_input = int(input('Would you like to:\n1. Catch\n2. Run'))
                int_input = input_check(action_input, 2)
            else:
                action_input = int(input('Would you like to:\n1. Catch\n2. Attack\n3. Run'))
                int_input = input_check(action_input, 3)
        except:
            print('Invalid input')

        if len(player_pets) == 0:
            match action_input:
                case 1:
                    # Catching the pet
                    catch_rate = chance(0.5)
                case 2:
                    catch_rate = False
        else:
            match action_input:
                case 1:
                    # Catching the pet
                    catch_rate = chance(0.5)
                case 2:
                    catch_rate = attack(player_pets, pet_data)
                case 3:
                    catch_rate = False

    if catch_rate:
        print('catch')
        # this Dict below is just the basic way to hold new pets
        # in the future add EXP and set it to min exp in pets.csv - add evolutions after x levels, everything is caught at its lowest level
        # 1 point per level, 3 points for evolution

        # pet is to hold the default info of the pet
        pet = {
            'id':pet_id,
            'name':pet_data['Name'],
            'level':1,
            'strength': int(pet_data['Strength']),
            'speed': int(pet_data['Speed']),
            'int': int(pet_data['Intelligence'])
        }

        # pet_out is to ensure that the output has the correct name when output
        pet_out = nickname(pet)

        return pet_out
    else:
        print('Not Catch')
        return None

def nickname(pet:dict):
    flag = True
    name_flag = True
    input_flag = True

    while flag:
        while input_flag:
            try:
                time.sleep(1)
                clear()
                want = int(input('Would you like to nickname this pet?\n1. Yes\n2. No\n'))
                input_flag = input_check(want, 2)
                flag = False
            except:
                print('thats not a good input')

        name_flag = True
        input_flag = True
        while name_flag:
            if want == 1:
                new_name = input('What would you like to name it?\n')
                if len(new_name) != 0:
                    while input_flag:
                        try:
                            check = int(input('Are you sure?\n1. Yes\n2. No\n')) # Doesnt work, If 2 is input, doesnt catch
                            input_flag = input_check(check, 2)
                            if check == 1:
                                flag = False
                            elif check == 2:
                                flag = True
                                name_flag = False
                        except:
                            print('thats not a valid input')
                    name_flag = False
            else:
                new_name = pet['name']
                name_flag = False

    pet['name'] = new_name
    return pet

def attack(player_pets:dict, opponent_pet:dict):
    battle_check = True

    clear()
    print('Select a Pet to battle with')
    pet = print_pets(player_pets)

    if pet == 0:
        print('You flee the battle')
    else:
        chosen_pet = player_pets[str(pet-1)]
        print(f'You select {chosen_pet["name"]}')

    #Pet attributes only needed for battles, resets after each fight
    
    clear()
    pet_health = chosen_pet['strength']
    opponent_health = opponent_pet['Strength']
    player_turn = True if chosen_pet['speed'] >= opponent_pet['Speed'] else False
    player_double = True if chosen_pet['speed'] > opponent_pet['Speed']*2 else False

    # Battle loops
    while battle_check:
        time.sleep(5)
        clear()
        if player_turn: # add chance for attacks not to land
            print(f'{chosen_pet["name"]} Attacks and deals {chosen_pet["strength"]} damage')
            opponent_health -= chosen_pet['strength']
            player_turn = False
        else: # add chance for attacks not to land
            print(f'{opponent_pet["Name"]} Attacks and deals {opponent_pet["Strength"]} damage')
            pet_health -= opponent_pet['Strength']
            print(f'{chosen_pet["name"]} has {pet_health} health remaining')
            player_turn = True


        if pet_health <= 0:
            print(f'{opponent_pet["Name"]} has won the fight')
            return False
        
        if opponent_health <= 0:
            print(f'{chosen_pet["name"]} has won the fight')
            print('You get to catch the pet without fail')
            return True


    
def area_manage():
    flag = True
    input_flag = True

    while flag:
        try:
            while input_flag:
                time.sleep(1)
                clear()
                area = int(input('What area would you like to go to?\n1. Home\n2. Plains\n3. Forest\n4. Mines\n5. Quit'))
                input_flag = input_check(area, 5)
        except:
            print('Invalid input')

        input_flag = True
        if area in range(1,5):
            areas(area)
        else:
            flag = False

def areas(choice:int):
    area = ['Home', 'Plains', 'Forest', 'Mines']
    print(area[choice-1])

def pets_manage(player_pets:dict):
    pet = -1
    pet_data = data_load()

    time.sleep(2)
    clear()

    check = {} # Check is here to catch if the player has caught any pets

    if player_pets == check:
        print('You have no pets')
        time.sleep(2)
    else:
        while pet != 0:
            pet = print_pets(player_pets)
            if pet == 0:
                print('Exiting Pet Management')
            else:
                pet_print = player_pets[str(pet-1)]
                clear()
                print(f'Name: {pet_print["name"]}\nID: {pet_print["id"]}\nPet Type: {pet_data["Name"].where(pet_data.index == pet_print["id"]).dropna()}\nStrength: {pet_print["strength"]}\nSpeed: {pet_print["speed"]}\nIntelligence: {pet_print["int"]}')
                print('''The Strength stat affects the amount of damage that a pet can take and deal
The Speed stat affects if the pet attacks first, and chance to hit. having double speed of the opponent can cause 2 attacks at one time.
The Intelligence stat is the chance for the pet to do double damage''')
                time.sleep(4)

def print_pets(player_pets:dict):
    flag = True

    while flag:

        time.sleep(2)
        clear()

        # This loop is to print all the pets the player has
        x = 0
        print('Here are your pets:')
        while x < (len(player_pets)):
            print(f'{x+1}. {player_pets[str(x)]["name"]}')
            x += 1

        try:
            pet_choose = int(input(f'To select a pet, choose any number between 1 and {x}\nTo quit select 0\n'))
            if pet_choose not in range(0, x+1):
                print('Not valid')
                pet_choose = -1
        except:
            print('Not a valid input')
        else:
            if pet_choose == 0:
                flag = False
                return pet_choose
            elif pet_choose == -1:
                print('test')
            else: 
                # possibly add the possibility to set nicknames
                # nicknames will just be name, that is set to pets default name at first
                return pet_choose

        


def main():

    while True:
        time.sleep(4)
        clear()
        main_menu()

if __name__ == '__main__':
    main()
