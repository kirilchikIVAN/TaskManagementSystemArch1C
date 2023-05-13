from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .tables import *

# Создаем подключение к базе данных
engine = create_engine('sqlite:///database.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Создаем таблицы в базе данных
Base.metadata.create_all(engine)

# Создаем сессию для работы с базой данных
session = Session()

# Создаем нового пользователя
employee = Employee(name='John Doe')
session.add(employee)
session.commit()

# Выполняем запрос к базе данных
employees = session.query(Employee).all()

# Выводим результаты запроса
for employee in employees:
    print(f'ID: {employee.id}, Name: {employee.name}, Age: {employee.boss}')

# Закрываем сессию
session.close()
