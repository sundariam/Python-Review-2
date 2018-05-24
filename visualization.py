"""построение графиков"""
import argparse
import pickle
import matplotlib.pyplot as plt
import numpy as np

PARSER = argparse.ArgumentParser()
PARSER.add_argument('--model', default='model.txt')
PARSER.add_argument('--model2', default='model2.txt')
ARGS = PARSER.parse_args()


with open(ARGS.model, "rb") as file:
    RESULT1 = pickle.load(file)

with open(ARGS.model2, "rb") as file:
    RESULT2 = pickle.load(file)

DATA_NAMES = ['средняя зарплата > 25000', 'средняя зарплата от 25000 до 35000',
              'средняя зарплата < 25000']
DATA_VALUES = RESULT1


def show_pie():
    """строит круговую диаграмму"""
    plt.title('Распределение зарплат по России')

    plt.pie(DATA_VALUES, autopct='%.1f', radius=1.1,
            explode=[0.10] + [0 for _ in range(len(DATA_NAMES) - 1)])
    plt.legend(
        bbox_to_anchor=(-0.16, 0.15, 0.25, 0.25),
        loc='lower left', labels=DATA_NAMES)
    plt.show()


def show_columns():
    """построение диаграммы"""
    regions = []
    y_column = []
    plt.title('10 регионов с самой высокой зарплатой')
    for i in RESULT2:
        regions.append(i[0])
        y_column.append(i[1])

    x_column = np.arange(len(regions))
    plt.xticks(x_column, regions)
    plt.bar(x_column, y_column, align='center', alpha=0.5)
    plt.show()

show_pie()
show_columns()
