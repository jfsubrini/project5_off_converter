#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module that clean the fr.openfoodfacts.org.products.csv file from Open Food Facts
insert the data in the tables of the offc_db database with the data of the off_myfile.csv
(8 columns, 63091 items ????????????????, 24.2 MO) file.

"""

# Import the csv module to read and write data in csv format. 
import csv
import os


# Delete the previous off_myfile.csv file.
try:
    os.remove("off_myfile2.csv")
    print("\nAncien fichier off_myfile.csv supprimé.")
finally:
    print("\nCréation du nouveau fichier off_myfile.csv en cours...\n")

# Opening and reading the .csv file from the Open Food Facts base.
f_source = "fr.openfoodfacts.org.products.csv"
file = open(f_source, newline='', mode='r')
reader = csv.reader(file, delimiter='\t')

# Creating and writing on the off_myfile.csv, 
# to put all the selected and useful data from the Open Food Facts .csv file.
f_name_new = "off_myfile2.csv"
file_new = open(f_name_new, newline='', mode='w')
writer = csv.writer(file_new, delimiter='\t')

# Insertion of the selected column with its data in the off_myfile.csv file.
for col in reader:
# Selected column position from the Open Food Facts .csv file.
    name = col[7]
    if name:
        brand = col[12]
        if brand:
            countries_list = ['France', 'Guadeloupe', 'Martinique', 'Guyane', 'La Réunion',\
             'Polynésie française', 'Saint-Pierre-et-Miquelon', 'Nouvelle-Calédonie',\
             'Union européenne', 'World']
            for cou in countries_list:
                countries = col[33]
                if cou == countries:
                    nutrition_grade = col[53]
                    if nutrition_grade:
                        categories_list = ['Chips et frites', 'Confitures', 'Crêpes et galettes',\
                        'Desserts au chocolat', 'Gâteaux', 'Pâtes à tartiner', 'Petit-déjeuners',\
                        'Salades composées', 'Sandwichs', 'Tartes']
                        for cat in categories_list:
                            category = col[60]
                            if cat == category:
                                url = col[1]
                                store = col[30]
                                ingredients = col[34]
                                nutrition_score = col[159]
                                writer.writerow([url, name, brand, store, countries, ingredients,\
                                    nutrition_grade, category, nutrition_score])
# Régler le problème des cases vides.

print("Le fichier off_myfile.csv a été créé.")

file.close()  # Close the .csv file.
