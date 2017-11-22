#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
#################### OpenFoodFacts Converter ####################
#                                      							#
# Expliquer le programme en anglais  dire qu'il faut faire      #
# tourner les autres fichiers d'abord                           #
#                           		                            #
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
        # Displaying all the aliments by 20 items pages.
        while select_food == 's':
            num_page += 1
            Queries.show_food(num_cat, num_page)
            select_food = input("\nSélectionnez votre aliment (entrez le n°) "\
            "ou accedées à d'autres choix (tapez 's') :\n")
        # Displaying the selected food with is name and nutrition_grade.
        Queries.show_selected(select_food)
        # Suggesting a substitute food product.
        numb_choice = 0
        Queries.show_substitute(num_cat, numb_choice)
        # Suggesting to display another substitute food product.
        ok_choice = input("\nCet aliment vous convient-il (tapez 'o') ou"\
            " voulez-vous voir un autre choix (tapez 'n') ?\n")
        # Displaying all 1 substitute aliment by page.
        while ok_choice == 'n':
            numb_choice += 1
            print("Je vous propose alors l'aliment suivant :\n")
            Queries.show_substitute(num_cat, numb_choice)
            ok_choice = input("\nCet aliment vous convient-il (tapez 'o') ou"\
                " voulez-vous voir un autre choix (tapez 'n') ?\n")
        # Stores where to buy this substitute food product.
        print('\nTrès bien.\nJe vous indique que vous pouvez acheter '\
            'cet aliment dans le(s) magasin(s) suivant(s):\n')
        Queries.show_store()

        # # Suggesting to save this substitute food product in the user database.
        # saving_db = input("\nVoulez-vous maintenant enregistrer cet aliment"\
        # " dans votre base de données ? (tapez 'o' pour oui)\n")
        # if saving_db == 'o':
        #     print("\nAliment de substitution enregistré dans votre base de données.\
        #         \nA bientôt dans l'Open Food Facts Converter.\n")
        # else:
        #     print("\nPas de problème. A bientôt dans l'Open Food Facts Converter.\n")

    # Option to find a substitute food product in the user database.
    elif option == '2':
        pass
        # selected_food_db = input('\nVoici les aliments de votre base de données personnnelle.\
        #     \nSélectionnez un aliment (entrez le n°) :\n')
        # number_sf_db = 30
        # while selected_food_db > number_sf_db:
        #     selected_food_db = input(f'Vous devez taper un entier de 1 à {number_sf_db}.\n')
        # print("Vous avez choisi l'aliment n°{}.".format(selected_food_db))

# To be standalone
if __name__ == "__main__":
    main()


# SELECT Category.name
# FROM Category
# INNER JOIN Food
#     ON Category.id = Food.category_id
# WHERE Food.id = num_cat;

# sql = "SELECT Food.id, Food.category_id, Food.name, Food.brand"
# FROM Food
# INNER JOIN Category
#     ON Category.id = Food.category_id
# WHERE category.id = {}".format(num_cat)"

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
