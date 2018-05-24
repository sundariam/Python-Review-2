"""построение графиков"""
import argparse
import pickle
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--model', default='model.txt')
parser.add_argument('--model2', default='model2.txt')
args = parser.parse_args()


with open(args.model, "rb") as file:
    result1 = pickle.load(file)

with open(args.model2, "rb") as file:
    result2 = pickle.load(file)

data_names = ['средняя зарплата > 25000', 'средняя зарплата от 25000 до 35000',
              'средняя зарплата < 25000']
data_values = result1


def show_pie():
    """строит круговую диаграмму"""
    plt.title('Распределение зарплат по России')

    plt.pie(data_values, autopct='%.1f', radius=1.1,
            explode=[0.10] + [0 for _ in range(len(data_names) - 1)])
    plt.legend(
        bbox_to_anchor=(-0.16, 0.15, 0.25, 0.25),
        loc='lower left', labels=data_names)
    plt.show()


def show_columns():
    """построение диаграммы"""
    regions = []
    y_column = []
    plt.title('10 регионов с самой высокой зарплатой')
    for i in result2:
        regions.append(i[0])
        y_column.append(i[1])

    x_column = np.arange(len(regions))
    plt.xticks(x_column, regions)
    plt.bar(x_column, y_column, align='center', alpha=0.5)
    plt.show()

show_pie()
show_columns()
