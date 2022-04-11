"""
Boring stuff
Author: Daniel Ferguson
Auth ID: 3374690
Date: Start -> 10/04/22 Completion -> 12/04/22
Task: INFT1004 Assignment 2: Spending Spree
I have ported large parts of this program from assessment 1
I have Integrated Pandas Dataframes into them for csv manipulation
You DO NOT need to write defs into the console, just run the entire program.
"""
import os
import sys
import time as t
import numpy as np
import pandas as pd
import io
from getpass import getuser


class MainMenu:
    def __init__(self):
        self.dt = 0.3  # default time for t.sleep

        # vars ported from assess1, may cull over time
        self.gc_items_lst = []  # init variables so that other defs can use them
        self.gc_cost_lst = []
        self.loop_count = 0
        self.gc_name = ""
        self.gc_max_spend = 0
        self.gc_max_items = 0
        self.username = ""
        self.name_assigned = False

    def menu(self):
        print("Welcome to the Spending Spree Menu!\n")
        t.sleep(self.dt)

        if not self.name_assigned:  # if not implemented so user only enters name once
            print("Hello " + str(getuser()) + "!")  # :)
            self.username = str(getuser())
            self.name_assigned = True

        print('')
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

    def input_checker(self, input_to_be_checked, csv, column_name):
        # This method is used to determine if the argument 'input_to_be_checked' is already a 'col_name' (column)
        # in the 'csv' file. If it is, then the user will be asked to replace the name with one not in
        # the 'csv' file.

        df = pd.read_csv(csv)  # reads the csv file from the argument csv

        in_chk = input_to_be_checked  # reduce local var names for ease of use
        col_name = column_name

        name_allowed = False
        while not name_allowed:  # will loop until name_allowed = True

            name_found = False  # assigns found to false each loop to reset it
            #  this is done incase user enters another in_chk that is also used
            for col in range(len(df)):  # loops through columns of df for the number of columns in df
                if df.loc[col, col_name] == in_chk:  # if in_chk var equals the value inside the column passed in
                    # 'col_name'
                    name_found = True  # if in_chk is found, set to name_found to True for the next if statement

            if name_found:  # gets user to type a new in_chk
                in_chk = input("Please enter a different gift card name: ")
            else:  # if in_chk isn't found in df column 'Name' then user is allowed to name gift card in_chk val
                name_allowed = True  # this will end while loop

        return in_chk

    def gift_card(self):
        print("Hello, I am Delilah, your personal gift card management system.")
        t.sleep(self.dt)  # stops the sequence for .3, adds readability
        print("Please enter the specifications of your gift card.\n")

        # all inputs are for the gift card specifications.
        gc_name = input("Gift card name:")
        gc_name = self.input_checker(gc_name, 'giftCards.csv', 'GiftCardName')  # runs input_checker method
        # input_checker is used to determine if gift card name has been used, gc_name will be reassigned if it has

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

        df = pd.read_csv('giftCards.csv')  # reads giftCards.csv into Dataframe df
        print(df)  # remove before handin
        print("\n")
        df.loc[len(df)] = [gc_name, gc_max_spend, gc_max_items]  # creates a new row and adds the gc details into it
        print(df)
        df.to_csv('giftCards.csv', index=None)  # writes the Dataframe to the csv file.

        print('')
        re_to_menu = input("Would you like to return to the menu (Y or N): ")
        if re_to_menu.upper() == "Y":
            self.menu()  # returns to menu
        else:
            sys.exit()

    def spending_spree(self):

        df = pd.read_csv('giftCards.csv')  # reads giftCards.csv into Dataframe df

        # print(df)
        # print(df.loc[0, 'Name'])
        print("\nPlease choose a gift card from this list: \n")
        for col in range(len(df)):
            t.sleep(self.dt)
            if col == 0:
                print(str(col + 1) + ". " + str(df.loc[col, 'GiftCardName']) + " (Default)")
            else:
                print(str(col + 1) + ". " + str(df.loc[col, 'GiftCardName']))

        col_ch = int(input("Please enter which card you would like to use (1, 2, 3 etc): ")) - 1
        print('')
        # column choice (gc choice), used to assign vars below

        gc_card_name = df.loc[col_ch, 'GiftCardName']  # pulls item specified by col_ch from column 'SpendingLimit'
        gc_max_spend = df.loc[col_ch, 'SpendingLimit']  # assigns to local vars so ported program can be used
        gc_max_items = df.loc[col_ch, 'MaxItems']

        print("You have chosen:\n Gift Card : " + str(gc_card_name) + "\n Spending Limit: $" + str(gc_max_spend) +
              "\n Item Limit: " + str(gc_max_items))
        print('')

        t.sleep(self.dt)
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

        # ported def loop from assess 1.
        # nests Cost and Items into sublists so that Cost var can be manipulated using sorted function
        # use prints on the below lists after manipulation to gain greater understanding of what is happening :)
        gc_list_nested = [list(x) for x in zip(gc_cost_lst, gc_items_lst)]
        # uses nested list to sort nested items based on cost, because desc is nested it follows cost movement
        gc_list_sorted = sorted(gc_list_nested, key=lambda l: l[0], reverse=True)

        # creates a dataframe out of the sorted list, adds columns
        export_df = pd.DataFrame(gc_list_sorted, columns=['ItemPrice', 'ItemDescription'])
        export_df['GiftCardName'] = gc_card_name  # creates a new column with the name of the gift card used
        export_df = export_df.loc[:, ['GiftCardName', 'ItemDescription', 'ItemPrice']]  # rearranges the columns

        combined_df = pd.concat([pd.read_csv('spendingHistory.csv'), export_df])
        pd.DataFrame(combined_df).to_csv('spendingHistory.csv', index=False)

        print("Gift card expended, your purchases are listed below, they are ordered from most to least expensive.\n")
        for x in range(loop_count):  # prints the list of transactions ordered highest cost to lowest :)
            print("Cost: $" + str(gc_list_sorted[x][0]) + ", item description: " + str(gc_list_sorted[x][1]))
            t.sleep(self.dt)  # exceeds requirement to print most expensive item.

        gc_num_item_purchased = len(gc_list_sorted)  # counts number of nested list items for average computation
        gc_average_cost = sum(gc_cost_lst) / gc_num_item_purchased  # average cost with sum of lst / num of purchases

        t.sleep(self.dt)
        print("\nGift card used: " + str(gc_card_name) + ", spending limit: $" + str(gc_max_spend))
        t.sleep(self.dt)
        print("The number of items purchased was: " + str(gc_num_item_purchased))
        t.sleep(self.dt)
        print("The average cost was: $" + str(round(gc_average_cost, 2)) + "\n")  # rounds avg cost -> 2 dec places
        t.sleep(self.dt)

        re_to_menu = input("Would you like to return to the menu (Y or N): ")
        if re_to_menu.upper() == "Y":
            self.menu()  # returns to menu

        else:
            sys.exit()

    def gc_history(self):
        print("List of gift cards: ")
        init = pd.read_csv('spendingHistory.csv')

        gc_names = init['GiftCardName'].copy()  # creates a series from the 'GiftCardName' column in init
        gc_names = gc_names.drop_duplicates()  # removes duplicate names from the series
        gc_names = gc_names.to_frame()  # turns the series into a dataframe
        gc_names.reset_index(inplace=True, drop=True)  # fixes the index, when duplicates are removed index breaks

        for i in range(len(gc_names.index)):  # loops for the number of gift card names in the dataframe
            print(str(i+1)+". "+str(gc_names.loc[i, 'GiftCardName']))  # prints each name in the dataframe

        temp_choice = int(input("\nPlease enter the number of the gift card you would like to view: "))
        # takes user input as 1,2,3 etc
        print("")
        gc_indiv_ch = gc_names.loc[(temp_choice-1), 'GiftCardName']
        # converts 1,2,3 into the actual GiftCardName required for steps below

        init.set_index('GiftCardName', inplace=True)  # makes column 'GiftCardName' the index
        gc_indiv_purchases = init.loc[gc_indiv_ch, :]  # passes rows based on index name, selected by gc_indiv_ch
        gc_indiv_purchases.reset_index(inplace=True, drop=True)  # removes GiftCardName index, replaces with 0,1,2 etc

        t.sleep(self.dt)
        print("Purchase History of "+gc_indiv_ch+": ")
        for col in range(len(gc_indiv_purchases)):
            t.sleep(self.dt)
            print(str(col + 1) + ". $" + str(gc_indiv_purchases.loc[col, 'ItemPrice']) + ", " +
                  str(gc_indiv_purchases.loc[col, 'ItemDescription']))

        re_to_menu = input("Would you like to return to the menu (Y or N): ")
        if re_to_menu.upper() == "Y":
            self.menu()  # returns to menu

        else:
            sys.exit()

    def gc_names(self):
        print("List of gift cards: ")
        init = pd.read_csv('giftCards.csv')

        gc_names = init['GiftCardName'].copy()  # creates a series from the 'GiftCardName' column in init
        gc_names = gc_names.drop_duplicates()  # removes duplicate names from the series
        gc_names = gc_names.to_frame()  # turns the series into a dataframe
        gc_names.reset_index(inplace=True, drop=True)  # fixes the index, when duplicates are removed index breaks

        for i in range(len(gc_names.index)):  # loops for the number of gift card names in the dataframe
            print(str(gc_names.loc[i, 'GiftCardName']))  # prints each name in the dataframe

        re_to_menu = input("Would you like to return to the menu (Y or N): ")
        if re_to_menu.upper() == "Y":
            self.menu()  # returns to menu
        else:
            sys.exit()

    def create_initial_csv(self):
        # this def will be launched on the first run of this program on a new computer.
        # it creates the two csv files needed and fills them with the data required by the program
        # creates giftCards.csv
        gift_cards = pd.DataFrame(columns=['GiftCardName', 'SpendingLimit', 'MaxItems'])
        # creates dataframe and adds specified columns
        gift_cards.loc[0, 'GiftCardName'] = 'Victory-day gift card'  # adds specified data into dataframe
        gift_cards.loc[0, 'SpendingLimit'] = 200
        gift_cards.loc[0, 'MaxItems'] = 4

        pd.DataFrame(gift_cards).to_csv('giftCards.csv', index=False)  # exports dataframe to csv

        # creates spendingHistory.csv
        spending_history = pd.DataFrame(columns=['GiftCardName', 'ItemDescription', 'ItemPrice'])
        pd.DataFrame(spending_history).to_csv('spendingHistory.csv', index=False)
        print("Initialisation complete: csv files created and setup.")

        with open("pr_lch.bak", 'w') as file_edit:  # creates a file that tells the program if it has been run before
            file_edit.write("1")
            os.system("attrib +h pr_lch.bak")

        self.menu()

    def on_launch(self):
        if os.path.exists("pr_lch.bak"):  # checks if file exists
            os.system("attrib -h pr_lch.bak")  # unhides file
            with open("pr_lch.bak", 'r') as launched_before:
                if launched_before.readline() == '1':  # checks if it has a '1' in it
                    os.system("attrib +h pr_lch.bak")  # rehides file (stops tampering)
                    self.menu()  # starts menu
                else:
                    self.create_initial_csv()  # runs initial startup
        else:
            self.create_initial_csv()


MainMenu_ob = MainMenu()  # instantiates a new object of the MainMenu Class
MainMenu_ob.on_launch()
