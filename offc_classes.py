""" Creating all the tables for the offc_db database
Second module : To create the tables in the offc_db database,
with the right columns, primary keys, foreign keys and table engines.

"""

# Import the PyMySQL package to connect Python with MySQL.
import pymysql.cursors


class Connect:
    """ Connection to the offc_db database with my username. """

    CONNECTION = pymysql.connect(
        host="localhost",
        user="jfsubrini",
        password="jeremiehugo1",
        database="offc_db",
        charset='utf8mb4',
        autocommit=True)
    CUR = CONNECTION.cursor()


class Queries:
    """ MySQL Queries. """

    def show_category():
        """ Query that seek the names of all the categories """
        sql = "SELECT id, name FROM Category"
        Result.category(sql)

    def show_food(num_cat, num_page):
        """ Query that seek the name and brand of all the aliment of the selected category """
        sql = "SELECT name, brand FROM Food WHERE category_id =" + str(num_cat)
        sql += " LIMIT " + str(num_page * 20) + ", 20"
        Result.food(sql)

    def show_selected(select_food):
        """ Query that seek the name and nutrition_grade of the selected aliment """
        sql = "SELECT name, nutrition_grade FROM Food WHERE id =" + str(select_food)
        Result.selection(sql)

    def show_substitute(num_cat, numb_choice):
        """ Query that seek in the selected category the substitute aliment
        that has better nutrition_grade and nutrition_score than the ones of the selected aliment """
        sql = "SELECT name, brand, ingredients, nutrition_score, nutrition_grade, url"
        sql += " FROM Food WHERE category_id =" + str(numb_choice)
        sql += " AND nutrition_score < -5"   #select_food.nutrition_score
        sql += " ORDER BY nutrition_grade, nutrition_score"
        sql += " LIMIT " + str(numb_choice) + ", 1"
        Result.substitute(sql)

    def show_store():
        # """ Query that seek in the selected category the substitute aliment
        # that has better nutrition_grade and nutrition_score than the ones of the selected aliment """
        # sql = "SELECT name, brand, ingredients, nutrition_score, nutrition_grade, url"
        # sql += " FROM Food WHERE category_id =" + str(numb_choice)
        # sql += " AND nutrition_score < -5"   #select_food.nutrition_score
        # sql += " ORDER BY nutrition_grade, nutrition_score"
        # sql += " LIMIT " + str(numb_choice) + ", 1"
        Result.store(sql)

class Result:
    """ Results of the queries. """

    def category(sql):
        """ Show the result of the query looking for the categories. """
        Connect.CUR.execute(sql)
        # i = 1
        for record in Connect.CUR:
            # res = str(print("".join(str(record))))
            print(record)
            # print(i, "".join(record))
            # i += 1

    def food(sql):
        """ Show the result of the query looking for the aliments in the chosen category. """
        Connect.CUR.execute(sql)
        i = 1
        for record in Connect.CUR:
            print(i, " de la marque ".join(record))
            i += 1

    def selection(sql):
        """ Show the result of the query looking for the nutrition_grade for the selected aliment. """
        Connect.CUR.execute(sql)
        print("\nL'aliment que vous avez choisi est :")
        for record in Connect.CUR:
            print(" avec le score nutritionnel suivant : ".join(record))

    def substitute(sql):
        """ Show the result of the query looking for the substitute aliments. """
        Connect.CUR.execute(sql)
        print("\nJe vous propose de le remplacer par l'aliment avec les caractériques suivantes : ")
        for record in Connect.CUR:
            print(", ".join(record))
            # for res in record:
            #     print(res)

    def store(sql):
        """ Show the store(s) where to buy the substitute selected aliment, if any. """
        Connect.CUR.execute(sql)
