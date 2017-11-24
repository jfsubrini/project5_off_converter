#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
#################### OpenFoodFacts Converter ####################
#                                                               #
# Expliquer le programme en anglais  dire qu'il faut faire      #
# tourner les autres fichiers d'abord                           #
#                                                               #
#################################################################

Python's Scripts
Files : off.myfile.csv

Copyright Jean-François Subrini, student DA Python at OpenClassrooms, 14/10/2017.

"""

# Import the PyMySQL package to connect Python with MySQL.
import pymysql.cursors

# Importation of the class file
from offc_classes import *


def main():
    """ Program wrapper """
    # Welcoming message
    print("\nBONJOUR, BIENVENUE SUR L'OPEN FOOD FACTS CONVERTER\n")
    # Optional menu
    print('Veuillez choisir une des deux options suivantes (tapez 1 ou 2) :')
    option = input('1 - Vous souhaitez remplacer un aliment.\
        \n2 - Retrouvez vos aliments substitués.\n')
    while option != '1' and option != '2':
        option = input("Vous devez taper '1' ou '2'.\n")
    # Option to choose a food product.
    if option == '1':
        # Displaying all the 10 categories with the query.
        print('\nVoici les différentes catégories présentes dans notre base de données :\n')
        Queries.show_category()
        # Chosing the right category of your food product.
        num_cat = input('\nSélectionnez la catégorie de votre aliment (entrez le n°) :\n')
        # while num_cat != '1' or num_cat != '1057' or num_cat != '1949' or num_cat != '2135'\
        #  or num_cat != '2444' or num_cat != '3813' or num_cat != '4166' or num_cat != '5843'\
        #   or num_cat != '6215' or num_cat != '6963':
        #     num_cat = input('Vous devez taper un des numéros de catégories ci-dessus.\n')
        print('Vous avez choisi la catégorie n°{}.\n'.format(num_cat))
        # Displaying the food from this category.
        print('\nVoici les aliments présents dans cette catégorie :\n')
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
            print("\nAliment de substitution enregistré dans votre base de données.\
                \nA bientôt dans l'Open Food Facts Converter.\n")
        else:
            print("\nPas de problème. A bientôt dans l'Open Food Facts Converter.\n")

    # Option to find a substitute food product in the user database.
    elif option == '2':
        print('\nVoici les aliments de votre base de données personnnelle :')
        # Chosing the food product in the database.
        num_my_page = 0
        Queries.source_food_db(num_my_page)
        source_food = input("\nSélectionnez un aliment (entrez le n°) "\
            "ou accedées à d'autres choix (tapez 's') :\n")
        # Displaying all the aliments by 10 items by pages.
        while source_food == 's':
            num_my_page += 1
            Queries.source_food_db(num_my_page)
            source_food = input("\nSélectionnez votre aliment (entrez le n°) "\
            "ou accedées à d'autres choix (tapez 's') :\n")
        # Displaying the selected substitute food for that selected food in the user database.
        Queries.substitute_food_db(source_food)
    print('\nMerci pour votre visite et à très bientôt...\n')

# To be standalone
if __name__ == "__main__":
    main()

# Nombre de produits par catégorie :
# SELECT COUNT(sur la PK) AS num_products
# FROM Food
# WHERE category_id = num_cat
# GROUP BY id;

# Nombre de produits pour les différents grade :
# SELECT nutrition_grade COUNT(*) AS num_nutri_grade
# FROM Food
# WHERE category_id = num_cat
# GROUP BY nutrition_grade;
