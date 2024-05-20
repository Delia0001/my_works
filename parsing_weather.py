from bs4 import BeautifulSoup
import requests
import sqlalchemy as db
from tabulate import tabulate
import os
import pandas as pd
import matplotlib.pyplot as plt
import logging

logging.basicConfig(filename='py_log.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Создаем соединение с базой данных
DB_URL = os.getenv('DB_URL', 'sqlite:///weather3.db')
engine = db.create_engine(DB_URL)
conn = engine.connect()
metadata = db.MetaData()

# Определяем таблицы
Region = db.Table('Region', metadata,
                  db.Column('id', db.Integer, primary_key=True),
                  db.Column('name', db.Text))

City = db.Table('City', metadata,
                db.Column('id', db.Integer, primary_key=True),
                db.Column('name', db.Text),
                db.Column('region_id', db.Integer, db.ForeignKey('Region.id')))

Checks = db.Table('Checks', metadata,
                  db.Column('id', db.Integer, primary_key=True),
                  db.Column('city_id', db.Integer, db.ForeignKey('City.id')),
                  db.Column('date', db.String),
                  db.Column('time', db.String))

Weather_new = db.Table('Weather_new', metadata,
                       db.Column('id', db.Integer, primary_key=True),
                       db.Column('check_id', db.Integer, db.ForeignKey('Checks.id')),
                       db.Column('date', db.String),
                       db.Column('temperature', db.Integer),
                       db.Column('wind', db.String))

metadata.create_all(engine)

# Определяем целевые сайты

site = os.getenv('site', 'https://weather.rambler.ru/world/rossiya/')
base_site = os.getenv('base_site', 'https://weather.rambler.ru')

# Парсим данные с сайта
logging.info('Sending request to the site...')
response = requests.get(site)
logging.info('Received response from the site.')
soup = BeautifulSoup(response.text, 'html.parser')

# Извлекаем данные о городах и погоде
regions = soup.find_all('a', class_='kgSF')
for region in regions[:6]:
    region_name = region.get('data-weather').split('::')[-1]
    # print(region_name)

    # Получение уточняющих ссылок
    href = region.get('href')
    # Добавление объекта в базу данных
    logging.info('Inserting region into the database...')
    region_insert = Region.insert().values(name=region_name)
    result = conn.execute(region_insert)
    logging.info('Region inserted into the database.')
    region_id = result.inserted_primary_key[0]  # Получаем ID добавленного региона
    region = base_site + href
    response = requests.get(region)
    soup = BeautifulSoup(response.text, 'html.parser')
    cities = soup.find_all('a', class_="MJZ5")

    for city in cities[:5]:
        city_name = city.get('data-weather').split('::')[-1]
        # print(city_name)
        href = city.get('href')
        # print(href)
        city = base_site + href
        response = requests.get(city)
        soup = BeautifulSoup(response.text, 'html.parser')
        week = soup.find_all('span', class_="PADa")  # даты из списка погоды на неделю
        temps = soup.find_all('span', class_="AY6t")  # температуры из списка погоды на неделю
        winds = soup.find_all('span', class_="ZX9i")  # ветренность из списка погоды на неделю
        # Сохраняем данные о городе
        logging.info('Inserting city into the database...')
        city_record = City.insert().values(name=city_name, region_id=region_id)  # Добавляем region_id
        result = conn.execute(city_record)
        logging.info('City inserted into the database.')
        city_id = result.inserted_primary_key[0]
        for day, temp, wind in zip(week, temps, winds):
            temper = temp.text.replace('-', '-')
            temper = int(temper.replace('°', ''))
            weather = Checks.insert().values(city_id=city_id, date=day.text, time='12:00')
            result = conn.execute(weather)
            check_id = result.inserted_primary_key[0]

            weather = Weather_new.insert().values(check_id=check_id, date=day.text, temperature=temper, wind=wind.text)
            conn.execute(weather)

# Отражаем таблицы из базы данных
metadata.reflect(bind=engine)

# Получаем список отраженных таблиц
tables = metadata.tables

# Выводим каждую таблицу отдельно в виде таблицы
for table_name, table in tables.items():
    print(f"Table: {table_name}")
    column_names = [column.name for column in table.c]
    data = conn.execute(table.select()).fetchall()
    print(tabulate(data, headers=column_names))
    print()

# Запрос к базе данных для получения городов и температур
logging.info('Executing query...')
query = """
SELECT City.name, Weather_new.date, Weather_new.temperature
FROM City
JOIN Checks ON City.id = Checks.city_id
JOIN Weather_new ON Checks.id = Weather_new.check_id
ORDER BY City.name, Weather_new.date
"""
df = pd.read_sql_query(query, conn)
logging.info('Query executed.')

# Построение графиков изменения температуры по дням нескольких городов
for city in df['name'].unique()[:5]:
    city_data = df[df['name'] == city]
    plt.plot(city_data['date'], city_data['temperature'])
    plt.title(city)
    plt.xlabel('Дата')
    plt.ylabel('Температура')
    plt.show()


conn.close()
logging.info('Connection to the database closed.')


from bs4 import BeautifulSoup
