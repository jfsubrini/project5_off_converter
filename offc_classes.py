""" Creating all the tables for the offc_db database
Second module : To create the tables in the offc_db database,
with the right columns, primary keys, foreign keys and table engines.

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


class Constant:
    """ Query that collect in a list all the id in Category """
    cat_dict = {}
    sql = "SELECT id FROM Category"
    Connect.CUR.execute(sql)
    i = 1
    for record in Connect.CUR:
        cat_dict[i] = record
        i += 1

    """ Query that collect in a list all the source_id in HealthyFood """
    source_id_list = []
    sql = "SELECT DISTINCT source_id FROM HealthyFood"
    Connect.CUR.execute(sql)
    for record in Connect.CUR:
        source_id_list.append(record)


class Queries:
    """ MySQL Queries. """

    def show_category():
        """ Query that seek the names of all the categories """
        sql = "SELECT id, name FROM Category"
        Result.category(sql)

    def show_food(num_cat, num_page):
        """ Query that seek the name and brand of all the food of the selected category """
        sql = "SELECT id, name, brand FROM Food WHERE category_id =" + str(num_cat)
        sql += " ORDER BY name, brand"
        sql += " LIMIT " + str(num_page * 15) + ", 15"
        Result.food(sql)

    def show_selected(select_food):
        """ Query that seek the name and nutrition_grade of the selected food """
        sql = "SELECT name, nutrition_grade FROM Food WHERE id =" + str(select_food)
        Result.selection(sql)

    def show_substitute(num_cat, select_food, num_choice):
        """ Query that seek in the selected category the substitute food
        that has better nutrition_grade and nutrition_score
        than the ones of the selected food """
        sql = "SELECT id, name, brand, ingredients, nutrition_score, nutrition_grade, url"
        sql += " FROM Food WHERE category_id =" + str(num_cat)
        sql += " AND nutrition_score < ("
        sql += "SELECT nutrition_score FROM Food WHERE id =" + str(select_food)
        sql += ") ORDER BY nutrition_grade, nutrition_score"
        sql += " LIMIT " + str(num_choice) + ", 1"
        Result.substitute(sql)

    def show_store(substitute_food):
        """ Query that seek the store(s) where one can buy the selected substitute food. """
        sql = "SELECT s.name"
        sql += " FROM Store AS s"
        sql += " INNER JOIN Food_Store AS fs"
        sql += " ON s.id = fs.store_id"
        sql += " WHERE fs.food_id =" + str(substitute_food)
        Result.store(sql)

    def save_substitute(select_food, substitute_food):
        """ Query that save the selected substitute food in the user database. """
        sql = "INSERT INTO HealthyFood (source_id, substitute_id) VALUES (%s, %s)"
        Connect.CUR.execute(sql, (select_food, substitute_food))

    def source_food_db(num_my_page):
        """ Query that seek the id, name, brand and nutrition_grade
        of all the food in the user database """
        sql = "SELECT f.id, f.name, f.brand, f.nutrition_grade"
        sql += " FROM Food AS f"
        sql += " INNER JOIN HealthyFood AS h"
        sql += " ON f.id = h.source_id"
        sql += " ORDER BY name, brand, nutrition_grade"
        sql += " LIMIT " + str(num_my_page * 10) + ", 10"
        Result.source_db(sql)

    def substitute_food_db(source_food):
        """ Query that seek in the selected substitute food
        for the selected one in the user database. """
        sql = "SELECT f.name, f.brand, f.nutrition_grade"
        sql += " FROM Food AS f"
        sql += " INNER JOIN HealthyFood AS h"
        sql += " ON f.id = h.substitute_id"
        sql += " WHERE h.source_id =" + str(source_food)
        Result.substitute_db(sql)


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
        """ Show the result of the query looking for the food in the chosen category. """
        Connect.CUR.execute(sql)
        for record in Connect.CUR:
            print(record)

    def selection(sql):
        """ Show the result of the query looking for the nutrition_grade
        for the selected food. """
        Connect.CUR.execute(sql)
        print("\nL'aliment que vous avez choisi est :")
        for record in Connect.CUR:
            print(" avec le niveau nutritionnel suivant : ".join(record))

    def substitute(sql):
        """ Show the result of the query looking for the substitute food. """
        Connect.CUR.execute(sql)
        print("\nJe vous propose de le remplacer par l'aliment suivant :\n"\
            "(n°, name, marque, ingredients, score nutritionnel, niveau nutritionnel, url)\n")
        for record in Connect.CUR:
            print(record)

    def store(sql):
        """ Show the store(s) where to buy the substitute selected food, if any. """
        Connect.CUR.execute(sql)
        print('\nTrès bien.\nVous pouvez acheter '\
            'cet aliment dans le(s) magasin(s) suivant(s):\n')
        for record in Connect.CUR:
            print("".join(record))
            # if record == "":
            #     print("Il n'y a pas de magasin renseigné dans la base.")

    def source_db(sql):
        """ Show all the selected food present in the user database. """
        Connect.CUR.execute(sql)
        for record in Connect.CUR:
            print(record)

    def substitute_db(sql):
        """ Show the selected substitute food in the user database. """
        Connect.CUR.execute(sql)
        print("\nVous avez sélectionné cet aliment de substitution :\n"\
            "(nom, marque, niveau nutritionnel)\n")
        for record in Connect.CUR:
            print(record)
