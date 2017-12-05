"""
All the classes and methods for the OpenFoodFacts Converter program.

"""

# Import the PyMySQL package, the Python MySQL client library.
import pymysql.cursors


class Connect:
    """ Connection to the offc_db database with my username and autocommit option.
    Prepare a cursor object using cursor() method. """

    CONNECTION = pymysql.connect(
        host="localhost",
        user="jfsubrini",
        password="jeremiehugo1",
        database="offc_db",
        charset='utf8mb4',
        autocommit=True)
    CUR = CONNECTION.cursor()


class List:
    """ Lists that will serve for input control """

    def list_id_category():
        """ Query collecting in a list all the id in the Category table """
        cat_list = []
        sql = "SELECT id FROM Category"
        Connect.CUR.execute(sql)
        for record in Connect.CUR:
            cat_list.append(record[0])
        return cat_list

    def list_id_food(real_num_cat):
        """ Query collecting in a list all the id in Food table """
        food_list = []
        sql = "SELECT id FROM Food"
        sql += " WHERE category_id =" + str(real_num_cat)
        sql += " ORDER BY name, brand"
        Connect.CUR.execute(sql)
        for record in Connect.CUR:
            food_list.append(record[0])
        return food_list

    def list_id_substitute(real_num_cat, real_select_food):
        """ Query collecting in a list all the substitute food id"""
        substitute_list = []
        sql = "SELECT id FROM Food "
        sql += " WHERE category_id =" + str(real_num_cat)
        sql += " AND nutrition_score < ("
        sql += "SELECT nutrition_score FROM Food WHERE id =" + str(real_select_food)
        sql += ") ORDER BY nutrition_grade, nutrition_score, name, brand"
        Connect.CUR.execute(sql)
        for record in Connect.CUR:
            substitute_list.append(record[0])
        return substitute_list

    def list_id_source():
        """ Query collecting in a list all the source id in the HealthyFood table """
        source_id_list = []
        sql = "SELECT DISTINCT source_id FROM HealthyFood"
        Connect.CUR.execute(sql)
        for record in Connect.CUR:
            source_id_list.append(record[0])
        return source_id_list


class Queries:
    """ MySQL Queries. """

    def show_category():
        """ Query that seeks the names of all the categories """
        sql = "SELECT name FROM Category"
        Result.category(sql)

    def show_food(real_num_cat, num_page):
        """ Query that seeks the name and brand of all the food from the selected category """
        sql = "SELECT name, brand FROM Food WHERE category_id =" + str(real_num_cat)
        sql += " ORDER BY name, brand"
        sql += " LIMIT " + str(num_page * 15) + ", 15"
        Result.food(sql, num_page)

    def show_selected(real_select_food):
        """ Query that seeks the name and nutrition grade of the selected food """
        sql = "SELECT name, nutrition_grade FROM Food WHERE id =" + str(real_select_food)
        Result.selection(sql)

    def show_substitute(real_num_cat, real_select_food, num_choice):
        """ Query that seeks in the selected category the substitute food
        (with their characteristics) that has better nutrition grade and
        nutrition score than the selected food one's """
        sql = "SELECT name, brand, ingredients, nutrition_score, nutrition_grade, url"
        sql += " FROM Food WHERE category_id =" + str(real_num_cat)
        sql += " AND nutrition_score < ("
        sql += "SELECT nutrition_score FROM Food WHERE id =" + str(real_select_food)
        sql += ") ORDER BY nutrition_grade, nutrition_score, name, brand"
        sql += " LIMIT " + str(num_choice) + ", 1"
        Result.substitute(sql)

    def show_store(substitute_food):
        """ Query that seeks the store(s)
        where one can buy the selected substitute food, if any in the OFF database. """
        sql = "SELECT s.name"
        sql += " FROM Store AS s"
        sql += " INNER JOIN Food_Store AS fs"
        sql += " ON s.id = fs.store_id"
        sql += " WHERE fs.food_id =" + str(substitute_food)
        Result.store(sql)

    def save_substitute(real_select_food, substitute_food):
        """ Query that saves the selected substitute food into the HealthyFood table. """
        sql = "INSERT INTO HealthyFood (source_id, substitute_id) VALUES (%s, %s)"
        Connect.CUR.execute(sql, (real_select_food, substitute_food))

    def source_food_db(num_my_page):
        """ Query that seeks the name, brand and nutrition grade
        of all the food present into the HealthyFood table """
        sql = "SELECT f.id, f.name, f.brand, f.nutrition_grade"
        sql += " FROM Food AS f"
        sql += " INNER JOIN HealthyFood AS h"
        sql += " ON f.id = h.source_id"
        sql += " ORDER BY name, brand, nutrition_grade"
        sql += " LIMIT " + str(num_my_page * 10) + ", 10"
        Result.source_db(sql)

    def substitute_food_db(id_source):
        """ Query that seeks for a selected food into the HealthyFood table
        the corresponding selected substitute product(s). """
        sql = "SELECT f.name, f.brand, f.nutrition_grade"
        sql += " FROM Food AS f"
        sql += " INNER JOIN HealthyFood AS h"
        sql += " ON f.id = h.substitute_id"
        sql += " WHERE h.source_id =" + str(id_source)
        Result.substitute_db(sql)


class Result:
    """ Results of the queries. """

    def category(sql):
        """ Shows the results of the query looking for the categories and gives a number
        for each one (different from the real category id), starting from 1. """
        Connect.CUR.execute(sql)
        i = 1
        for record in Connect.CUR:
            print(i, record[0])
            i += 1

    def food(sql, num_page):
        """ Shows (order by the alphabetic name and brand) the results of the query
        looking for food products and gives a number for each one (different from the real food id),
        starting from 1. """
        Connect.CUR.execute(sql)
        i = 1 + num_page * 15
        for record in Connect.CUR:
            print(i, record)
            i += 1

    def selection(sql):
        """ Shows the result of the query looking for the nutrition grade of the selected food. """
        Connect.CUR.execute(sql)
        print("\nL'aliment que vous avez choisi est :")
        for record in Connect.CUR:
            print(" avec le niveau nutritionnel suivant : ".join(record))

    def substitute(sql):
        """ Shows (order by the alphabetic nutrition grade and nutrition score) the result of
        the query looking for one substitute food, with the name, brand, ingredients,
        nutrition score and grade, and the url for that product. """
        Connect.CUR.execute(sql)
        print("\nJe vous propose de le remplacer par l'aliment suivant :\n"\
            "(nom, marque, ingredients, score nutritionnel, niveau nutritionnel, url)\n")
        for record in Connect.CUR:
            print(record)

    def store(sql):
        """ Shows the store(s) where to buy the substitute selected food,
        if any present in the OFF database. """
        Connect.CUR.execute(sql)
        print('\nTrès bien.\nVous pouvez acheter '\
            'cet aliment dans le(s) magasin(s) suivant(s) :\n')
        for record in Connect.CUR:
            print("".join(record))

    def source_db(sql):
        """ Shows (order by the alphabetic name, brand and nutrition grade) all the selected food
        present into the HealthyFood with their real food id, name, brand, and nutrition grade. """
        Connect.CUR.execute(sql)
        for record in Connect.CUR:
            print(record)

    def substitute_db(sql):
        """ Shows the selected chosen substitute food, with the name, brand and nutrition grade. """
        Connect.CUR.execute(sql)
        print("\nVous avez sélectionné cet aliment de substitution :\n"\
            "(nom, marque, niveau nutritionnel)\n")
        for record in Connect.CUR:
            print(record)
