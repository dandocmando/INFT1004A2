"""
Boring stuff
Author: Daniel Ferguson
Auth ID: 3374690
Date: Start -> 09/04/22 Upload -> 29/04/22
Task: INFT1004 Assignment 2: Spending Spree
You DO NOT need to write defs into the console, just run the entire program.
"""
import sys
import time as t
import numpy as np
import pandas as pd
import io


class MainMenu:
    def __init__(self):
        test = 0
        self.dt = 0.3  # default time for t.sleep

        # vars ported from assess1, may cull over time
        self.gc_items_lst = []  # init variables so that other defs can use them
        self.gc_cost_lst = []
        self.loop_count = 0
        self.gc_name = ""
        self.gc_max_spend = 0
        self.gc_max_items = 0
        self.username = ""

    def menu(self):
        print("Welcome to the Spending Spree Menu!\n")
        print("Options:\n 1. Define a gift card. \n 2. Go on a Spending Spree. \n 3. Display list of existing gift "
              "cards.\n 4. Display spending history. \n Q. Quit the program (Q).\n")

        choice = input("Choose 1, 2, 3, 4 or Q: ")
        if choice == '1':
            self.gift_card()  # pretty self-explanatory, launches the def gift_card
        if choice == '2':
            self.spending_spree()
        if choice == '3':
            self.gc_names()
        if choice == '4':
            self.gc_history()
        if choice.lower() == 'q':
            print("Goodbye! ")

        else:
            print("You failed to choose an option.")

    def gc_name_used(self, name):
        # This method is used to determine if the argument 'name' is already a 'GiftCardName' in the giftCards.csv file
        # if it is, then it will ask the user to replace the name with one not in the csv file.

        df = pd.read_csv('giftCards.csv')
        gc_name = name

        name_allowed = False
        while not name_allowed:  # will loop until name_allowed = True

            name_found = False  # assigns found to false each loop to reset it
            #  this is done incase user enters another gc_name that is also used
            for col in range(len(df)):  # loops through columns of df for the number of columns in df
                if df.loc[col, 'Name'] == gc_name:  # if gc_name var equals the value inside column(col) 'Name'
                    name_found = True  # if gc_name is found, set to name_found to True for the next if statement

            if name_found:  # gets user to type a new gc_name
                gc_name = input("Please enter a different gift card name: ")
            else:  # if gc_name isn't found in df column 'Name' then user is allowed to name gift card gc_name val
                name_allowed = True  # this will end while loop

        # if (df.Name == name).any():  # could be used instead of above 'for loop + if', but I though current method ^
        # showed a lower level understanding of python (instead of using a pandas function), so I left it
        return gc_name

    def gift_card(self):
        print("Hello, I am Delilah, your personal gift card management system.")
        t.sleep(self.dt)  # stops the sequence for .3, adds readability
        self.username = input("What is your name?\n")  # asks for users name for later use.
        print("Please enter the specifications of your gift card:\n")

        # all inputs are for the gift card specifications.
        gc_name = input("Gift card name:")
        gc_name = self.gc_name_used(gc_name)  # runs input_checker method with gc_name as the argument
        # input_checker is used to determine if gift card name has been used, gc_name will be reassigned if taken

        gc_max_spend = float(input("Gift card maximum spending ($100-$500): "))
        while gc_max_spend > 500 or gc_max_spend < 100:  # checks if input fits requirements, loops until it does
            gc_max_spend = float(input("Please enter a value in a range of $100-$500: "))

        gc_max_items = int(input("Maximum number of items allowed to purchase (1-5): "))
        while gc_max_items < 1 or gc_max_items > 5:
            gc_max_items = int(input("Please enter a value in a range of 1-5: "))

        print("\n")

        # prints out the previously input details
        t.sleep(self.dt)
        print("These are your gift card details:\n" + "\nGift card name: " + gc_name)
        t.sleep(self.dt)
        print("Gift card maximum spending allowed: $" + str(gc_max_spend))
        t.sleep(self.dt)
        print("Gift card maximum number of items allowed to purchase: " + str(gc_max_items) + "\n")

        df = pd.read_csv('test.csv')  # reads giftCards.csv into Dataframe df
        print(df)  # remove before handin
        print("\n")
        df.loc[len(df)] = [gc_name, gc_max_spend, gc_max_items]  # creates a new row and adds the gc details into it
        print(df)
        df.to_csv('test.csv', index=None)  # writes the Dataframe to the csv file.

        re_to_menu = input("Would you like to return to the menu (Y or N): ")
        if re_to_menu.upper() == "Y":
            self.menu()  # returns to menu

    def spending_spree(self):
        df = pd.read_csv('test.csv')  # reads giftCards.csv into Dataframe df
        # print(df)
        # print(df.loc[0, 'Name'])
        print("\nPlease choose a gift card from this list: \n")
        for col in range(len(df)):
            print(str(df.loc[col, 'Name']) + " (" + str(col + 1) + ")")
        col_ch = int(input("Choice: ")) - 1  # column choice (gc choice), used to assign vars below

        gc_card_name = df.loc[col_ch, 'Name']
        print(gc_card_name)
        gc_max_spend = df.loc[col_ch, 'SpendingLimit']  # pulls item in location 0 from column 'SpendingLimit'
        print(gc_max_spend)
        gc_max_items = df.loc[col_ch, 'MaxItems']
        print(gc_max_items)

        temp_max = 0
        # gc_max_items = self.gc_max_items  # pulls variable values from init def  # deprecated by df.loc
        # gc_max_spend = self.gc_max_spend
        gc_cost_lst = self.gc_cost_lst
        gc_items_lst = self.gc_items_lst
        loop_count = self.loop_count

        # ported from assess 1 :)

        # no str into int input exception handling has been implemented, as isn't mentioned in marking guidelines.
        # loop will repeat until loop_count is greater than gc_max_items or temp_max is higher than gc_max_spend
        while loop_count < gc_max_items and temp_max < gc_max_spend:
            cost = float(input("Purchase price: "))  # takes user input into cost variable
            temp_max = temp_max + cost  # stores the temporary total cost

            if temp_max <= gc_max_spend:  # checks if temp max is lower or equal to max spend
                gc_cost = cost  # assigns gc_cost the value of cost
                gc_cost_lst.append(gc_cost)  # appends gc_cost value into gc_cost_lst

                gc_items_desc = input("Purchase description: ")  # takes user input for item description
                gc_items_lst.append(gc_items_desc)  # appends input desc into items lst
                loop_count = loop_count + 1  # increments loop count

            else:
                t.sleep(self.dt)
                print("The gift card doesn't have enough funds to process this purchase, please try again.\n")

                # resets temp_max back to the last accepted spending amount by settings its value to gc_cost_lst
                temp_max = sum(gc_cost_lst)

            t.sleep(self.dt)
            print("\nGift card used so far: $" + str(temp_max) + " out of $" + str(gc_max_spend) + "\n")
            self.loop_count = loop_count  # loop is modified after assignment so self.loop needs to be updated

    def gc_history(self):
        print("List of gift cards: ")
        init = pd.read_csv('someNumbers.csv')

        gc_names = init['GiftCardName'].copy()  # creates a series from the 'GiftCardName' column in init
        gc_names = gc_names.drop_duplicates()  # removes duplicate names from the series
        gc_names = gc_names.to_frame()  # turns the series into a dataframe
        gc_names.reset_index(inplace=True, drop=True)  # fixes the index

        for i in range(len(gc_names.index)):  # loops for the number of gift card names in the dataframe
            print(str(gc_names.loc[i, 'GiftCardName']))  # prints each name in the dataframe

        view_choice = input("\nPlease enter the exact name of the gift card you would like to view: ")
        print("")

        init.set_index('GiftCardName', inplace=True)  # makes column 'GiftCardName' the index
        gc_indiv_purchases = init.loc[view_choice, :]  # passes rows based on index name, selected by view_choice
        gc_indiv_purchases.reset_index(inplace=True, drop=True)  # removes GiftCardName index, replaces with 0,1,2 etc

        t.sleep(self.dt)
        print("Purchase History:")
        for col in range(len(gc_indiv_purchases)):
            t.sleep(self.dt)
            print(str(col + 1) + ". $" + str(gc_indiv_purchases.loc[col, 'ItemPrice']) + ", " +
                  str(gc_indiv_purchases.loc[col, 'ItemDescription']))

    def gc_names(self):
        print("penis")


MainMenu_ob = MainMenu()  # instantiates a new object of the MainMenu Class
MainMenu_ob.menu()
