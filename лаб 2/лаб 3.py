# -*- coding: utf-8 -*-
from spyre import server
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from urllib.request import urlopen


# Завантаження даних
def download():
    date_time = datetime.now()
    separated_date_time = date_time.strftime('%Y_%m_%d__%H_%M_%S')

    tuple_NNAA_to_LW = {1: 22, 2: 24, 3: 23, 4: 25, 5: 3, 6: 4, 7: 8, 8: 19, 9: 20, 10: 21, 11: 9, 12: 0, 13: 10, 14: 11, 15: 12, 16: 13, 17: 14, 18: 15, 19: 16, 20: 0, 21: 17, 22: 18, 23: 6, 24: 1, 25: 2, 26: 7, 27: 5}

    # Завантаження даних для кожного регіону
    for index_s in range(1, 28):
        url = f'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={index_s}&year1=1981&year2=2023&type=Mean'
        vhi_url = urlopen(url)

        # Зберігання отриманих даних в CSV-файл
        with open(f'dataset2/_ {separated_date_time}_vhi_id_{index_s}.csv', 'w') as out:
            dataset_s = vhi_url.read().decode('utf-8').replace('<br>', '').replace('<tt><pre>', '').replace(' ', '').split('\n')
            dataset_s.pop(-1)
            a = dataset_s.pop(0)
            a = a.split(':')[1].split(',')[0]
            out.write(f'{a}\n'+'\n'.join(dataset_s))

# Читання даних з CSV-файлів
def read_csv_file():
    tuple_NNAA_to_LW = {1: 22, 2: 24, 3: 23, 4: 25, 5: 3, 6: 4, 7: 8, 8: 19, 9: 20, 10: 21, 11: 9, 12: 0, 13: 10, 14: 11, 15: 12, 16: 13, 17: 14, 18: 15, 19: 16, 20: 0, 21: 17, 22: 18, 23: 6, 24: 1, 25: 2, 26: 7, 27: 5}
    frames = []

    # Зчитування даних з кожного CSV-файлу
    for index_f in range(1, 28):
        with open(f'dataset2/_2023_12_17__02_33_36_vhi_id_{index_f}.csv', "r") as dataset:
            df = dataset.readlines()
            df = [line.strip().split(',') for line in df]

            # Створення DataFrame з даних з кожного файлу
            df = pd.DataFrame(df[2:], columns=['year', 'Week', 'SMN',  'SMT', 'VCI', 'TCI', 'VHI', 'empty'])
            df['index_region'] = tuple_NNAA_to_LW[index_f]

            frames.append(df)

    # Об'єднання всіх DataFrame в один DataFrame result_df
    result_df = pd.concat(frames, ignore_index=True)

    return result_df

# Виклик функції для завантаження даних
download()

# Зчитування даних з CSV-файлів
df = read_csv_file()

# Створення веб-додатку
class MyApp(server.App):
    title = "Weather Data Analysis"

    inputs = [
        {
            'type': 'dropdown',
            'label': 'Select Index',
            'options': [
                {'label': 'VCI', 'value': 'VCI'},
                {'label': 'TCI', 'value': 'TCI'},
                {'label': 'VHI', 'value': 'VHI'}
            ],
            'key': 'index',
            'action_id': 'update_data'
        },
        {
            'type': 'dropdown',
            'label': 'Select Region',
            'options': [
                {'label': region, 'value': region} for region in df['index_region'].unique()
            ],
            'key': 'region',
            'action_id': 'update_data'
        },
        {
            'type': 'text',
            'label': 'Enter Months Interval',
            'value': '1,12',
            'key': 'months',
            'action_id': 'update_data'
        }
    ]

def getData(self, params):
        index = params['index']
        region = params['region']
        months = list(map(int, params['months'].split(',')))

        # Відбір даних з DataFrame df за параметрами index, region та months
        selected_data = df[(df['Index'] == index) & (df['index_region'] == region)]

        return selected_data

def getPlot(self, params):
        df_filtered = self.getData(params)

        plt.figure(figsize=(10, 6))
        plt.plot(df_filtered['year'], df_filtered['VHI'], marker='o')
        plt.title(f'{params["index"]} for Region {params["region"]}')
        plt.xlabel('Year')
        plt.ylabel('VHI')
        plt.grid(True)
        return plt

def getHTML(self, params):
        return "Hello, this is an HTML text."

# Запускаємо додаток
if __name__ == '__main__':
    app = MyApp()
    app.launch()