#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
#################### OpenFoodFacts Converter #############################
#                                                                        #
# This program gives to the user some substitute type of aliments        #
# for a given food, with better nutrition score and the place to buy it. #
# It's also possible for the user to store substitute aliments,          #
# in order to look for it latter.                                        #
#                                                                        #
# To run this program one must run these 3 modules in order :            #
#                              p1_offc_db_creation.py                    #
#                              p2_offc_tables_creation.py                #
#                              p3_offc_insert_data.py                    #
#                                                                        #
##########################################################################

File with Open Food Facts data : off.myfile.csv
Other script : offc_classes.py

Copyright Jean-François Subrini, student DA Python at OpenClassrooms, 25/11/2017.

"""

# Import the PyMySQL package, the Python MySQL client librairy.
import pymysql.cursors

# Importation of the class file
from offc_classes import *


def main():
    """ Program wrapper """
    # Welcoming message and optional menu
    print("\nBONJOUR, BIENVENUE SUR L'OPEN FOOD FACTS CONVERTER\n")
    print('Veuillez choisir une des deux options suivantes (tapez 1 ou 2) :')
    option = input('1 - Vous souhaitez trouver un aliment de substitution.\
        \n2 - Retrouvez vos aliments substitués.\n')
    while option != '1' and option != '2':
        option = input("Vous devez taper '1' ou '2'.\n")
    
    # Option to choose a food product to find a substitute aliment.
    if option == '1':
        # Displaying all the 10 categories with the query.
        print('\nVoici les différentes catégories présentes dans notre base de données :\n'\
            '(n°, nom)\n')
        Queries.show_category()
        # Chosing the right category of your food product.
        # while 1:
        num_cat = input('\nSélectionnez la catégorie de votre aliment (entrez le n°) :\n')
        #     for num in Constant.cat_list:
        #         print(Constant.cat_list, type(Constant.cat_list))
        #         if num == num_cat:
        #             break
        # Displaying the food from this category.
        print('\nVoici les aliments présents dans cette catégorie :\n'\
            '(n°, nom, marque)\n')
        # Chosing the right food product in the selected category.
        num_page = 0
        Queries.show_food(num_cat, num_page)
        select_food = input("\nSélectionnez votre aliment (entrez le n°) "\
            "ou accedées à d'autres choix (tapez 's') :\n")
        # Displaying all the aliments by 15 items by pages.
        while select_food == 's':
            num_page += 1
            Queries.show_food(num_cat, num_page)
            select_food = input("\nSélectionnez votre aliment (entrez le n°) "\
            "ou accedées à d'autres choix (tapez 's') :\n")
        # Displaying the selected food with is name and nutrition_grade.
        Queries.show_selected(select_food)
        # Suggesting a substitute food product.
        num_choice = 0
        # Displaying all 1 substitute aliment by page.
        ok_choice = 'n'
        while ok_choice == 'n':
            num_choice += 1
            query = Queries.show_substitute(num_cat, select_food, num_choice)
            if query != "":
                ok_choice = input("\nCet aliment vous convient-il (tapez le n° correspondant) ou"\
                    " voulez-vous voir un autre choix (tapez 'n') ?\n")
                # if ok_choice == int():
                #     substitute_food = ok_choice
                # elif ok_choice != 'o' and ok_choice != 's':
                #     print("Veuillez taper 'o' ou 'n'.")
            # else:
            #     print("Il n'y a pas d'autres aliments plus sain.")
        # Showing the store(s) where to buy this substitute food product.
        substitute_food = ok_choice
        Queries.show_store(substitute_food)
        # Suggesting to save this substitute food product in the user database.
        saving_db = input("\nVoulez-vous maintenant enregistrer cet aliment"\
            " dans votre base de données ? (tapez 'o' pour oui)\n")
        if saving_db == 'o':
            Queries.save_substitute(select_food, substitute_food)
            print("\nAliment de substitution enregistré dans votre base de données.\n"\
                "\nA bientôt dans l'Open Food Facts Converter.\n")
        else:
            print("\nPas de problème. A bientôt dans l'Open Food Facts Converter.\n")

    # Option to find a substitute food product in the user database.
    elif option == '2':
        print('\nVoici les aliments de votre base de données personnnelle :\n'\
            '(n°, nom, marque, niveau nutritionnel)\n')
        # Displaying the food product(s) from the database and choising one.
        num_my_page = 0
        Queries.source_food_db(num_my_page)
        source_food = input("\nSélectionnez un aliment (entrez le n°) "\
            "ou accedées à d'autres choix (tapez 's') :\n")
        # Displaying all the aliments by 10 items by pages.
        while source_food == 's':
            num_my_page += 1
            Queries.source_food_db(num_my_page)
            source_food = input("\nSélectionnez un aliment (entrez le n°) "\
            "ou accedées à d'autres choix (tapez 's') :\n")
        # Controlling the input
        # while source_food != Constant.source_id_list:
            # source_food = input("\nSélectionnez un aliment (entrez le n°) "\
            # "ou accedées à d'autres choix (tapez 's') :\n")
        # Displaying the selected substitute food for that selected food in the user database.
        Queries.substitute_food_db(source_food)
        print("")

# To be standalone
if __name__ == "__main__":
    main()
