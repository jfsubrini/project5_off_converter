# OpenFoodFacts Converter

Program made by Jean-François Subrini, November 2017.



## What the project is for ?

This program was made to complete the **Project 5 of the « D.A. - PYTHON » path from OpenClassrooms**.
The purpose is to use the public data from the **OpenFoodFacts** website.
In brief, this program gives to the user some substitute type of food for a given chosen one, with better nutrition score and the place where to buy it, if any.
**It helps people to substitute a healthy food for a junk one.**


## Features of the program

* The user initiate this computer program from the command-line interface.
* The first menu ask for option 1 for finding a substitute food or option 2 for consulting the user’s substitute food database.
    1. **Option 1** :
the program first shows 10 different categories of food and ask for one to choose;
then, it shows all the food products present in the database for that category (15 by page), with its number, name and brand;
the user must choose the one he wants a substitute to be found and the program indicate its nutrition grade;
the program offers a choice of substitute food, one by one, with all its characteristics (number, name, brand, ingredients, nutritional score, nutritional grade and url to access the details on the Open Food Facts website).
the user must choose the one he wants as a substitute and the program returns where one can buy it, if any corresponding store in the database;
Finally, the user can save or not this substitute food in his own database, in order to look for it latter.
    2. **Option 2** :
The program shows the list of the present food in the user’s database (10 by page).
The user must pick one and the program shows the name, brand and nutrition grade that were selected previously by the user. If the user selected different substitute food for the same food product and saved them, the program will show all the selected substitute food.


## Where the data come from and how were they selected ?

All the data used in this program come from the « OpenFoodFacts - France » website [](https://fr.openfoodfacts.org).
This huge database was imported from [](https://fr.openfoodfacts.org/data) and the .csv file that holds all the data is : *fr.openfoodfacts.org.products.csv*
This file was 1,14 Go big the 25/11/2017, present version in this repository, with 163 columns and 380 790 food products.

The first part of this program cleans this database to create a new one, *off_myfile.csv*, smaller and more relevant for this program.

Only food sold on the **French territory** were retained, by selecting in the ‘countries_fr’ column the words ‘France’ , ’Guadeloupe’, ‘Martinique’, ’Guyane’, ’La Réunion’, ‘Polynésie française’, ‘Saint-Pierre-et-Miquelon’, ‘Nouvelle-Calédonie’, ’Union européenne’ or ‘World’.
Then, only the data from these **8 relevant columns were selected** : *url, product_name, brands, stores, ingredients_text, nutrition_grade_fr, main_category_fr, nutrition-score-fr_100g*. 
The name, brand, category and nutrition grade were compulsory data to be existing for a food product to be selected.
Finally, a choice to retain **10 categories** was made with these : 
*’Chips et frites’, ‘Confitures’, ‘Crêpes et galettes’, ‘Desserts au chocolat’, ‘Gâteaux’, ‘Pâtes à tartiner’, ‘Petit-Déjeuners’, ‘Salades composées’, ‘Sandwichs’ and ‘Tartes’*.


## How to configure and install this program ?

To setup the program for localhost, one first need to install :
python 3
pip
MySQL
PyMySQL

For the data, in this repository you can find the *fr.openfoodfacts.org.products.csv* file (25/11/2017 version) from the OpenFoodFacts website but one can update it going to : [](https://fr.openfoodfacts.org/data) and load the last *fr.openfoodfacts.org.products.csv* file version.


## How to use it or get it running ?

**To run this program the first time, one must run these 4 modules in this same order** :
        1. **p0_clean_csv.py**                      *(to create a clean .csv file)*
        2. **p1_offc_db_creation.py**           *(to create the database)*
        3. **p2_offc_tables_creation.py**     *(to create the tables)*
        4. **p3_offc_insert_data.py**            *(to insert data into tables)*

**Be careful not to run p3_offc_insert_data.py more than once**.
If so, run again p1, p2 and p3 (once this time !).

Finally, **to run the main program**, everytime one wants, just run : **p4_off_converter.py**

Enjoy it !