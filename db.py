import re
import sqlite3


'''

    Класс для работы с бд

'''

class DbBot:
    # название таблиц при проверки на наличия 
    # их в базе, если нет то создаем
    table_name = [
        'sqlitedb_users',
        'sqlitedb_test',
        'sqlitedb_quest',
        'sqlitedb_answer'
    ]
    # модели для работы с базу через объекты

    # соединение к бд 
    sqlite_connection = None
    # создаем подключение в бд
    def __init__(self):
        # проверка было ли до этого подключение
        # дыбы не плодить много соединений 
        if self.sqlite_connection != None:
            return
        try:
            self.sqlite_connection = sqlite3.connect('sqlite_python.db')
            cursor = self.sqlite_connection.cursor()
            print("База данных создана и успешно подключена к SQLite")
            sqlite_select_query = "select sqlite_version();"
            cursor.execute(sqlite_select_query)
            record = cursor.fetchall()
            print("Версия базы данных SQLite: ", record)
            cursor.close()
        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)

    
    def __del__(self):
        self.sqlite_connection.close()