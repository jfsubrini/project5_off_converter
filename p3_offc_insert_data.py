#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Third module : To insert the data in the tables of the offc_db database
from the off_myfile.csv (8 columns, 63091 items ????????????????, 24.2 MO) file.

"""

# Import Python's module
import csv

# Import the PyMySQL package to connect Python with MySQL.
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

# Opening and reading the .csv file with all the selected data from the Open Food Facts base.
f_name = "off_myfile4.csv"
file = open(f_name, newline='', mode='r')
reader = csv.reader(file, delimiter='\t')

# Insertion of the data in the Category and Food tables.
for col in reader:
    # Column position for the data in the off_myfile.csv file.
    url = col[0]
    name = col[1]
    brand = col[2]
    #store = col[3]
    ingredients = col[4]
    nutrition_grade = col[5]
    category = col[6]
    nutrition_score = col[7]
    # SQL Queries to insert non duplicate data in the Category table.
    sql = "INSERT IGNORE INTO Category (name) VALUES (%s)"  # Syntax to avoid SQL injections
    cur.execute(sql, (category))   # Execute de SQL command
    # SQL Queries to insert data in the Food table.
    sql = "INSERT INTO Food (category_id, name, brand, ingredients, nutrition_score,"\
    "nutrition_grade, url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    sql2 = "SELECT id FROM Category WHERE name = %s"
    cur.execute(sql2, (category))
    result_cat = cur.fetchone()
    cur.execute(sql, (result_cat, name, brand, ingredients, nutrition_score, nutrition_grade, url))
print("\nTables Category et Food renseignées.")

# Opening and reading the .csv file with all the selected data from the Open Food Facts base.
f_name = "off_myfile4.csv"
file = open(f_name, newline='', mode='r')
reader = csv.reader(file, delimiter='\t')
# Retrieving each different store name present in the off_myfile.csv file.
store_list = []
for col in reader:
    store = col[3]
    store_unit = store.strip().split(',')
    for item in store_unit:
        item = item.strip().capitalize()
        if item and item not in store_list:
            store_list.append(item)
store_list.sort()
# SQL Queries to insert the store_list in the Store table.
for label in store_list:
    sql = "INSERT INTO Store (name) VALUES (%s)"
    cur.execute(sql, (label))
print("\nTable Store renseignée."\
    "\n\nInsertion des données dans la table de composition Food_Store en cours...")

# Opening and reading the .csv file with all the selected data from the Open Food Facts base.
f_name = "off_myfile4.csv"
file = open(f_name, newline='', mode='r')
reader = csv.reader(file, delimiter='\t')
# SQL Queries to insert data in the Food_Store table.
for col in reader:
    store = col[3]
    if store != "":
        store_unit = store.strip().split(',')
        for item in store_unit:
            item = item.strip().capitalize()
            sql = "SELECT id FROM Store WHERE name = %s"
            cur.execute(sql, (item))
            id_store = cur.fetchone()
            sql = "SELECT id FROM Food WHERE name = %s and brand = %s"
            cur.execute(sql, (col[1], col[2]))
            id_food = cur.fetchone()
            sql = "INSERT INTO Food_Store (food_id, store_id) VALUES (%s, %s)"
            cur.execute(sql, (id_food, id_store))
print("\nTable Food_Store renseignée.")
print("\nToutes les données de la base épurée de l'OPEN FOOD FACTS"\
" ont été insérées avec succès dans toutes les tables de la base de données offc_db."\
"\nVous pouvez maintenant lancer le programme principal p4_off_converter.py.\n")

file.close()  # Close the .csv file.

connection.close()  # Disconnect from server
