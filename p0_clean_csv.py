#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module that clean the fr.openfoodfacts.org.products.csv file from OpenFoodFacts,
creating the off_myfile.csv file with 8 columns and 7289 food products (3.6 MO).

"""

# Import the csv module to read and write data in csv format
# and the os module to delete the .csv file at the start.
import csv
import os


# Delete the previous off_myfile.csv file if any.
try:
    os.remove("off_myfile.csv")
    print("\nAncien fichier off_myfile.csv supprimé.")
    print("\nCréation du nouveau fichier off_myfile.csv en cours...\n")
except:
    print("\nCréation du fichier off_myfile.csv en cours...\n")

# Opening and reading the .csv file from the Open Food Facts base.
f_source = "fr.openfoodfacts.org.products.csv"
file = open(f_source, newline='', mode='r')
reader = csv.reader(file, delimiter='\t')

# Creating and writing on the off_myfile.csv file,
f_name_new = "off_myfile.csv"
file_new = open(f_name_new, newline='', mode='w')
writer = csv.writer(file_new, delimiter='\t')

# Inserting the selected column with its chosen data from the Open Food Facts .csv file
# into the off_myfile.csv file.
for col in reader:
    # Selected columns from the Open Food Facts .csv file (with its position).
    name = col[7]
    # If the column "product_name" is not empty.
    if name:
        brand = col[12]
        # If the column "brands" is not empty.
        if brand:
            countries_list = ['France', 'Guadeloupe', 'Martinique', 'Guyane', 'La Réunion',\
             'Polynésie française', 'Saint-Pierre-et-Miquelon', 'Nouvelle-Calédonie',\
             'Union européenne', 'World']
            for cou in countries_list:
                try:
                    countries = col[33]
                    # If the column "countries_fr" contains at least
                    # one of the country listed in the countries_list.
                    if cou == countries:
                        nutrition_grade = col[53]
                        # If the column "nutrition_grade_fr" is not empty.
                        if nutrition_grade:
                            categories_list = ['Chips et frites', 'Confitures',\
                            'Crêpes et galettes', 'Desserts au chocolat', 'Gâteaux',\
                            'Pâtes à tartiner', 'Petit-déjeuners', 'Salades composées',\
                            'Sandwichs', 'Tartes']
                            for cat in categories_list:
                                category = col[60]
                                # If the column "main_category_fr" contains at least
                                # one of the category listed in the categories_list.
                                if cat == category:
                                    url = col[1]           # column 'url'
                                    store = col[30]        # column 'stores'
                                    ingredients = col[34]  # column ingredients_text
                                    nutrition_score = col[159]   # column 'nutrition-score-fr_100g'
                                    # Then the line is selected for the off_myfile.csv file
                                    # and fill the url, name, brand, store, ingredients,
                                    # nutrition_grade, category and nutrition_score columns.
                                    writer.writerow([url, name, brand, store, ingredients,\
                                        nutrition_grade, category, nutrition_score])
                except IndexError:
                    pass

print("Le fichier off_myfile.csv a été créé.\n")
file.close()  # Close the .csv file.
