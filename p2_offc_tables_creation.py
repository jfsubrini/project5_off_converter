#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Second module : To create the tables in the offc_db database,
with the right columns, primary keys, foreign keys and table engines.

"""

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
cur = connection.cursor()

try:
    # To create the Category table with the columns, primary key and table engine.
    sql = "CREATE TABLE Category (id MEDIUMINT UNSIGNED AUTO_INCREMENT,\
        name VARCHAR(100) UNIQUE NOT NULL,\
        PRIMARY KEY(id))\
        ENGINE = INNODB"
    cur.execute(sql)

    # To create the Food table with the columns, primary key and table engine.
    sql = "CREATE TABLE Food (id MEDIUMINT UNSIGNED AUTO_INCREMENT,\
        category_id MEDIUMINT UNSIGNED NOT NULL,\
        name VARCHAR(255) NOT NULL,\
        brand VARCHAR(170) NOT NULL,\
        ingredients TEXT,\
        nutrition_score TINYINT,\
        nutrition_grade CHAR(1) NOT NULL,\
        url VARCHAR(255) NOT NULL,\
        PRIMARY KEY(id))\
        ENGINE = INNODB"
    cur.execute(sql)

    # To create the Store table with the columns, primary key and table engine.
    sql = "CREATE TABLE Store (id MEDIUMINT UNSIGNED AUTO_INCREMENT,\
        name VARCHAR(170),\
        PRIMARY KEY(id))\
        ENGINE = INNODB"
    cur.execute(sql)

    # To create the Food_Store composition table with the columns and table engine.
    sql = "CREATE TABLE Food_Store (food_id MEDIUMINT UNSIGNED NOT NULL,\
        store_id MEDIUMINT UNSIGNED NOT NULL)\
        ENGINE = INNODB"
    cur.execute(sql)

    # To create the HealthyFood table with the columns and table engine.
    sql = "CREATE TABLE HealthyFood (source_id MEDIUMINT UNSIGNED NOT NULL,\
        substitute_id MEDIUMINT UNSIGNED NOT NULL)\
        ENGINE = INNODB"
    cur.execute(sql)

    # To create the Foreign Keys in the Food, Food_Store and HealthyFood tables.
    sql = "ALTER TABLE Food ADD CONSTRAINT fk_category_id FOREIGN KEY (category_id)\
        REFERENCES Category(id);\
        ALTER TABLE Food_Store ADD CONSTRAINT fk_food_id FOREIGN KEY (food_id)\
        REFERENCES Food(id);\
        ALTER TABLE Food_Store ADD CONSTRAINT fk_store_id FOREIGN KEY (store_id)\
        REFERENCES Store(id);\
        ALTER TABLE HealthyFood ADD CONSTRAINT fk_source_id FOREIGN KEY (source_id)\
        REFERENCES Food(id);\
        ALTER TABLE HealthyFood ADD CONSTRAINT fk_substitute_id FOREIGN KEY (substitute_id)\
        REFERENCES Food(id)"
    cur.execute(sql)
    print("\nTables de la base de données offc_db créées avec succès.\n")

except:
    print("\nLes tables de la base de données offc_db ont déjà été créées.\n")

finally:
    connection.close()
