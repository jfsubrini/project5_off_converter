#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Third module : To insert the data into the tables of the offc_db database,
with the data of the off_myfile.csv file (8 columns, 7289 lines, 3.6 MO),
from 10 food categories.

"""

# Import the csv module to read and write data in csv format.
import csv

# Import the PyMySQL package, the Python MySQL client library.
import pymysql.cursors

# Connection to the offc_db database with my username and autocommit option.
connection = pymysql.connect(
    host="localhost",
    user="jfsubrini",
    password="jeremiehugo1",
    database="offc_db",
    charset='utf8mb4',
    autocommit=True)
# Prepare a cursor object using cursor() method.
cur = connection.cursor()


#### Category & Food tables ####
# Opening and reading the .csv file with all the selected data from the Open Food Facts base.
f_name = "off_myfile.csv"
file = open(f_name, newline='', mode='r')
reader = csv.reader(file, delimiter='\t')
# Insertion of data in the Category and Food tables.
for col in reader:
    # Column position for the data in the off_myfile.csv file.
    url = col[0]
    name = col[1]
    brand = col[2]
    ingredients = col[4]
    nutrition_grade = col[5]
    category = col[6]
    nutrition_score = col[7]
    # SQL Queries to insert non duplicate data into the Category table.
    sql = "INSERT IGNORE INTO Category (name) VALUES (%s)"  # Syntax to avoid SQL injections
    cur.execute(sql, (category))   # Execute de SQL command
    # SQL Queries to insert data into the Food table.
    sql = "INSERT INTO Food (category_id, name, brand, ingredients, nutrition_score,"\
    "nutrition_grade, url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    sql2 = "SELECT id FROM Category WHERE name = %s" # Because Food.category_id = Category.id
    cur.execute(sql2, (category))
    result_cat = cur.fetchone()
    cur.execute(sql, (result_cat, name, brand, ingredients, nutrition_score, nutrition_grade, url))
print("\nTables Category et Food renseignées.")

#### Store table ####
# Opening and reading the off_myfile.csv from the beginning.
file.seek(0)
# Retrieving each different store name presents in the off_myfile.csv file,
# with some string formating, and creating a store_list to put in.
store_list = []
for col in reader:
    store = col[3]
    store_unit = store.strip().split(',')
    for item in store_unit:
        item = item.strip().capitalize()
        if item and item not in store_list:
            store_list.append(item)
store_list.sort()
# SQL Queries to insert the store_list into the Store table.
for label in store_list:
    sql = "INSERT INTO Store (name) VALUES (%s)"
    cur.execute(sql, (label))
print("\nTable Store renseignée.")

#### Food_Store table ####
# Opening and reading the off_myfile.csv from the beginning.
file.seek(0)
print("\nInsertion des données dans la table de composition Food_Store en cours...")
# SQL Queries to insert data into the Food_Store table.
# Using some string formating in order to separate each store name from the other.
for col in reader:
    store = col[3]
    if store != "":
        store_unit = store.strip().split(',')
        for item in store_unit:
            item = item.strip().capitalize()
            # Find the id of the Store.
            sql = "SELECT id FROM Store WHERE name = %s"
            cur.execute(sql, (item))
            id_store = cur.fetchone()
            # Find the id of the Food (with the name, brand and url altogether).
            sql = "SELECT id FROM Food WHERE name = %s and brand = %s and url = %s"
            cur.execute(sql, (col[1], col[2], col[0]))
            id_food = cur.fetchone()
            # Find for one Food.id the coresponding Store.id (from 0 to many)
            sql = "INSERT INTO Food_Store (food_id, store_id) VALUES (%s, %s)"
            cur.execute(sql, (id_food, id_store))
print("\nTable Food_Store renseignée.")

print("\nToutes les données de la base épurée de l'OPEN FOOD FACTS"\
" ont été insérées avec succès dans toutes les tables de la base de données offc_db."\
"\n\nVous pouvez maintenant lancer le programme principal p4_off_converter.py.\n")


file.close()  # Close the .csv file.
connection.close()  # Disconnect from server.
