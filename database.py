"""создание и работа с таблицей базы данных"""
import sqlite3 as lite
import argparse
import pickle

PARSER = argparse.ArgumentParser()
PARSER.add_argument('--salaries', default='salaries.txt')
PARSER.add_argument('--model', default='model.txt')
PARSER.add_argument('--model2', default='model2.txt')
ARGS = PARSER.parse_args()

CON = lite.connect('test.db')


def create_table():
    """создание таблицы с зарплатами по регионам"""
    with CON:
        cursor = CON.cursor()
        cursor.execute("DROP TABLE IF EXISTS regions")
        cursor.execute("""CREATE TABLE regions(Id INTEGER PRIMARY KEY,
                                            name VARCHAR(30),
                                            salary INTEGER)""")


def fill_in():
    """внесение данных в таблицу"""
    with CON:
        cursor = CON.cursor()
        with open(ARGS.salaries) as file:
            for line in file:
                line = line.split('  ')
                cursor.execute("""INSERT INTO regions(name,salary)
                               VALUES (?, ?)""",
                               (line[0], int(line[1])))


def get_result():
    """Делим регионы на 3 группы по сумме зарплаты"""
    with CON:
        cursor = CON.cursor()
        cursor.execute("""SELECT COUNT(salary)
                        FROM regions
                        WHERE salary > 30000""")
        count_max = cursor.fetchone()
        cursor.execute("""SELECT COUNT(salary)
                        FROM regions
                        WHERE salary > 25000
                        AND salary < 30000""")
        count_avg = cursor.fetchone()
        cursor.execute("""SELECT COUNT(salary)
                        FROM regions
                        WHERE salary < 25000""")
        count_min = cursor.fetchone()
        result = []
        result.append(count_max)
        result.append(count_avg)
        result.append(count_min)

    return result


def top_10():
    """10 регионов с самой высокой зарплатой"""
    with CON:
        cursor = CON.cursor()
        data = []
        cursor.execute("""SELECT name, salary
                           FROM regions
                           WHERE salary > 50000""")
        i = 0
        while i < 10:
            data.append(cursor.fetchone())
            i += 1
    return data


create_table()
fill_in()

with open(ARGS.model, "wb") as new_file:
    pickle.dump(get_result(), new_file)

with open(ARGS.model2, "wb") as new_file:
    pickle.dump(top_10(), new_file)
