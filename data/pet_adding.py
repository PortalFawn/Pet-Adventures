import pandas as pd
import os
import random as r
import time

'''
This file is intended for use by the developer, or any other authorised users
'''

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

def load():
    pets = pd.read_csv('data/pets.csv')
    return pets

def save(pets:pd.DataFrame):
    print('Saving to CSV...')
    pets.to_csv('data/pets.csv', mode='a', header=False)

def main():
    flag = True
    pet_flag = True
    input_flag = True
    pets_added = 0

    while flag:
        try:
            clear()
            select = int(input('Would you like to add pets to the index?\n1. Yes\n2. No and Quit\n'))
            flag = input_check(select, 2)
        except:
            print('Invalid input')

        if select == 1:
            while pet_flag:
                clear()
                print('It is advised that for base level pets that the numbers add to 15')
                while input_flag:
                    pet_name = input('What is the name of this pet?\n')
                    if len(pet_name) == 0:
                        print('there is no input') 
                    else: 
                        input_flag = False

                input_flag = True
                while input_flag:
                    try:
                        pet_str = int(input('What is the Strength of this pet?\n'))
                        input_flag = False
                    except:
                        print('invalid input')

                input_flag = True
                while input_flag:
                    try:
                        pet_int = int(input('What is the Intelligence of this pet?\n'))
                        input_flag = False
                    except:
                        print('invalid input')

                input_flag = True
                while input_flag:
                    try:
                        pet_spd = int(input('What is the Speed of this pet?\n'))
                        input_flag = False
                    except:
                        print('invalid input')
                
                if pets_added == 0:
                    # Issue Adding new pet to Original list - End of night Commit
                    new_pet = pd.DataFrame([pet_name, pet_str, pet_spd, pet_int])
                    pets_added += 1

                    new_pet = new_pet.T

                    print(new_pet)
                else:
                    newer_pet = pd.DataFrame([pet_name, pet_str, pet_spd, pet_int])

                    new_pet = pd.concat([new_pet, newer_pet.T])
                    print(new_pet)

                input_flag = True
                while input_flag:
                    try:
                        cont = int(input('Would you like to add another pet?\n1. Yes\n2. No\n'))
                        input_flag = input_check(cont, 2)
                    except:
                        print('invalid input')

                input_flag = True
                if cont == 2:
                    pet_flag, flag = False, False 
                else:
                    pet_flag = True

    print(new_pet)
    save(new_pet)
    print('Program Closing')
        


if __name__ == '__main__':
    main()