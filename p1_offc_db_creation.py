#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
First module : To create the OpenFoodFacts Convertor Database

"""

# Import the PyMySQL package, the Python MySQL client library.
import pymysql.cursors


# Connection to the offc_db database.
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="jeremiehugo1")
# Prepare a cursor object using cursor() method.
cur = connection.cursor()


# Creating the offc_db database after droping the previous one if exists.
sql = "DROP DATABASE IF EXISTS offc_db; CREATE DATABASE offc_db CHARACTER SET 'utf8'"
cur.execute(sql)
# Granting all privileges of that database to my username.
sql = "GRANT ALL PRIVILEGES ON offc_db.* TO 'jfsubrini'@'localhost'"
cur.execute(sql)
print("\nBase de données offc_db créée avec succès.\n")

connection.commit()
connection.close()
