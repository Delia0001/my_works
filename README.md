# my_works
Репозиторий с работами
## parsing_weather
Общий ход работы     
Введём обозначения:    
• целевой сайт — сайт, который необходимо парсить в ходе работы;    
• уточняющая ссылка — маршрут(route) на ресурс целевого сайта, содержащий полный набор данных для парсинга.    

Общий ход работы следующий:    
1. Запрос к целевому сайту на получение(requests) полного(если кол-во больше 1000, то 1000) набора уточняющих ссылок. Уметь отрабатывать случай, когда список ссылок разбивается по страницам.
2. Навигация по уточняющим ссылкам и извлечение данных(bs4).
3. Обработка и сохранение данных. Данные должны сохраняться с помощью
ORM(sqlalchemy) в базу данных sqlite. В варианте представлена минимальная по
наполнению схема отношений, её можно расширять.
4. Подведение итогов.
5. Создание логов и обработка ислючений.
![image](https://github.com/Delia0001/my_works/assets/112614636/fee96af8-4133-4d12-a72e-0b613f66c181)
## КР_самолеты
Содержание работы    
1. Выберите задачу для бизнеса, которую Вы хотите решить с помощью методов машинного обучения. На основание бизнес-задачи, поставьте задачу
машинного обучения. Подберите дата-сет и оставьте ссылку на него.    
Пример:
Бизнес-задачи: Предсказание оттока клиентов в банке ВТБ.
Задача машинного обучения: Бинарная классификация
Ссылка на дата-сет: https://ods.ai/competitions/data-fusion2024-churn
2. Выполните анализ и обработку дата-сета. Этот задание включает в себя
следующие этапы работы с данными:    
- Первичный анализ данных  
- Предобработку данных  
- Разведывательный анализ данных (Exploratory Data Analysis)  
- Создание признаков (Feature Engineering)  
- Отбор признаков (Feature selection)  
- Подготовка данных (Data Preparation)  
В блокноте должны присутствовать ячейки с текстом, в которых написано
названия выполнение этапа работы с данными.  

3. Выберите несколько метрик для оценки моделей машинного обучения.
Обоснуйте свой выбор и дайте интерпретацию метрик для бизнес-задачи.  
4. Постройте 4 модели машинного обучения для решение поставленной задачи.  
5. Проведите диагностику лучшей модели из пункта 4.  
6. Сделайте подбор гиперпараметров для лучшей модели из пункта 4.  
7. Постройте ансамблевую модель машинного обучения.  
В конце блокнота сделайте вывод о проделанной работе.  
