import pandas as pd
import os
import random as r
from main import input_check

'''
This file is intended for use by the developer, or any other authorised users
'''

def load():
    pets = pd.read_csv('pets.csv')
    return pets

def save(pets):
    pets.to_csv('pets.csv')

def main():
    flag = True
    pet_flag = True

    while flag:
        try:
            select = int(input('Would you like to add pets to the index?\n1. Yes\n2. No and Quit'))
            flag = input_check(select, 2)
        except:
            print('Invalid input')

        if select == 1:
            while pet_flag:
                pet_name = input('what is the name of this pet')

        


if __name__ == '__main__':
    main()