"""создание и работа с таблицей базы данных"""
import sqlite3 as lite
import argparse
import pickle

PARSER = argparse.ArgumentParser()
PARSER.add_argument('--salaries', default='salaries.txt')
PARSER.add_argument('--model', default='model.txt')
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


create_table()
fill_in()

with open(ARGS.model, "wb") as new_file:
    pickle.dump(get_result(), new_file)
