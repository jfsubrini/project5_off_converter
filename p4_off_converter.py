#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
#################### OpenFoodFacts Converter #############################
#                                                                        #
# This program gives to the user some substitute type of food            #
# for a given one, with better nutrition score and the place where       #
# to buy it, if any.                                                     #
# It helps people to substitute a healthy food for a junk one.           #
# It's also possible for the user to save this substitute food in        #
# his own database, in order to look for it latter.                      #
#                                                                        #
# To run this program the first time, one must run these 4 modules       #
# in this same order :                                                   #
#       1.  p0_clean_csv.py                (to create a clean .csv file) #
#       2.  p1_offc_db_creation.py         (to create the database)      #
#       3.  p2_offc_tables_creation.py     (to create the tables)        #
#       4.  p3_offc_insert_data.py         (to insert data into tables)  #
#                                                                        #
# Be careful not to run p3_offc_insert_data.py more than once.           #
# If so, run again p1, p2 and p3 (once this time !).                     #
#                                                                        #
# Finally, to run the main program, everytime one wants, just run :      #
#           p4_off_converter.py**                                        #
#                                                                        #
##########################################################################

File with OpenFoodFacts' clean data : off.myfile.csv
Other script : offc_classes.py

Copyright Jean-François Subrini, student DA Python at OpenClassrooms, 25/11/2017.

"""


# Importation of the class module
from offc_classes import *


def main():
    """ Program wrapper """
    # Welcoming message and optional menu.
    print("\nBONJOUR, BIENVENUE SUR L'OPENFOODFACTS CONVERTER\n")
    print('Veuillez choisir une des deux options suivantes (tapez 1 ou 2) :\n')
    option = input('1 - Vous souhaitez trouver un aliment de substitution.\
        \n2 - Retrouvez vos aliments substitués.\n')
    while option != '1' and option != '2':
        option = input("Vous devez taper '1' ou '2'.\n")

    ### Option 1 to choose a food product to find a substitute one.
    if option == '1':

        ## Displaying all the 10 categories with the query.
        print('\nVoici les 10 différentes catégories présentes dans notre base de données :\n'\
            '(n°, nom)\n')
        Queries.show_category()
        # Controlling user input and manage exception.
        while 1:
            num_cat = input('\nSélectionnez la catégorie de votre aliment '\
                '(entrez un n° de 1 à 10) :\n')
            try:
                if int(num_cat) in range(1, 11):
                    break
            except ValueError:
                pass
        # Finding the correspondance between the input n° and the category id.
        real_num_cat = List.list_id_category()[int(num_cat)-1]

        ## Displaying the food from the selected category.
        print('\nVoici les aliments présents dans cette catégorie :\n'\
            '(n°, nom, marque)\n')
        # Displaying the food products in the selected category, 15 by page, with name and brand.
        num_page = 0
        Queries.show_food(real_num_cat, num_page)
        # Chosing a food product (n° in the current page) or turning the page ('s').
        while 1:
            select_food = input("\nSélectionnez votre aliment (entrez le n°) "\
                "ou accedez à d'autres choix (tapez 's') :\n")
            num_min = 1 + 15 * num_page
            num_max = num_min + 15
            try:
                if select_food == 's':
                    num_page += 1
                    Queries.show_food(real_num_cat, num_page)
                elif int(select_food) in range(num_min, num_max):
                    break
            except ValueError:
                pass
        # Finding the correspondance between the input n° and the food id.
        real_select_food = List.list_id_food(real_num_cat)[int(select_food)-1]

        ## Displaying the selected food with its name and nutrition grade.
        Queries.show_selected(real_select_food)

        ## Suggesting a substitute food product.
        num_choice = 0
        # Displaying 1 substitute food by page, with name, brand, ingredients, nutrition_score,
        # nutrition_grade and url. Choose it ('o') or turn the page ('n').
        Queries.show_substitute(real_num_cat, real_select_food, num_choice)
        while 1:
            ok_choice = input("\nCet aliment vous convient-il (tapez 'o') ou"\
                " voulez-vous voir un autre choix (tapez 'n') ?\n")
            try:
                if ok_choice == 'n':
                    num_choice += 1
                    Queries.show_substitute(real_num_cat, real_select_food, num_choice)
                elif ok_choice == 'o':
                    # Find the substitute food real id in the substitute food id list
                    substitute_food = List.list_id_substitute(real_num_cat, real_select_food)\
                    [int(num_choice)]
                    break
            except ValueError:
                pass

        ## Showing the store(s) where to buy this substitute food product, if any.
        Queries.show_store(substitute_food)

        ## Suggesting to save this substitute food product in the HealthyFood table ('o').
        saving_db = input("\nVoulez-vous maintenant enregistrer cet aliment"\
            " dans votre base de données ? (tapez 'o' pour oui)\n")
        if saving_db == 'o':
            Queries.save_substitute(real_select_food, substitute_food)
            print("\nAliment de substitution enregistré dans votre base de données.\n"\
                "\nA bientôt dans l'OpenFoodFacts Converter.\n")
        else:
            print("\nPas de problème. A bientôt dans l'OpenFoodFacts Converter.\n")

    ### Option 2 to find a substitute food product in the HealthyFood table.
    elif option == '2':
        print('\nVoici les aliments de votre base de données personnnelle :\n'\
            '(n°id, nom, marque, niveau nutritionnel)\n')

        ## Displaying the food product(s) from the HealthyFood table, 10 by page.
        num_my_page = 0
        Queries.source_food_db(num_my_page)
        # Chosing a food product (n° in the current page) or turning the page ('s').
        broken = 1
        while broken:
            id_source = input("\nSélectionnez un aliment (entrez le n°id) "\
            "ou accedez à d'autres choix (tapez 's') :\n")
            # Checking the input
            try:
                if id_source == 's':
                    num_my_page += 1
                    Queries.source_food_db(num_my_page)
                # Checking if the input n°id is in the list that holds all the source id
                # from the HealthyFood table.
                elif id_source != 's':
                    for j in List.list_id_source():
                        if j == int(id_source):
                            broken = 0
            except ValueError:
                pass

        ## Displaying the selected substitute food for the selected food product that was
        ## present into the HealthyFood table, with the name, brand and nutrition grade.
        Queries.substitute_food_db(id_source)

        # Goodbye message.
        print("\nA bientôt dans l'OpenFoodFacts Converter.\n")

# To be standalone
if __name__ == "__main__":
    main()
