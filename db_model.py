from db import *


class CustromCtrl:
    """
        Родительский контроллер
    """
    def __init__(self):
        pass


    def add(self):
        pass


    def update(self):
        pass

    
    def remove(self):
        pass


class CustomModel():
    """
        Родительская модель
    """
    # protected название таблицы
    _table_name = ''

    # список моделей
    __table_model = []

    # данные из бд
    _data = None
    

    def __init__(self):
        self.db = DbBot()


    def check_model(self):
        self.__table_model = [
            UserModel(),
            TestModel(),
            QuestModel(),
            AnswerModel()
        ]
        for _model in self.__table_model:
            _model.print_name()
            if _model.check_has_table() is None:
                _model.create_table()


    def create_table(self):
        pass


    def get(self, id):
        pass

    def print_name(self):
        print(self._table_name)


    def data(self):
        return self._data


    def check_has_table(self):
        """
            Проверка на наличие таблиц в бд
        """
        cursor = self.db.sqlite_connection.cursor()
        # sqlite_master - таблица созданая sqlite для информации по всем таблицам
        sqlite_select_query = '''SELECT name FROM sqlite_master WHERE type='table' AND name='{}';'''.format(self._table_name)
        cursor.execute(sqlite_select_query)
        total_rows = cursor.fetchone()
        cursor.close()
        return total_rows


    def remove_table(self):
        '''
            Удаляем тублицу
        '''
        cursor = self.db.sqlite_connection.cursor()
        sql = '''
            DROP TABLE {}
        '''.format(self._table_name)
        cursor.execute(sql)
        self.db.sqlite_connection.commit()
        cursor.close()


    def dict_factory(self, cursor, row):
        """
            Перенос данных из картежа в словарь
            название столбца -> зачение поля
        """
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d


class UserModel(CustomModel):
    """
        Модель для работы пользователя
    """

    _table_name = 'sqlitedb_users'


    def get(self, user_id):
        '''
            Получаем запись пользователя в бд

            id - id пользователя в telegram
        '''
        # перевод tuple в dict
        self.db.sqlite_connection.row_factory = self.dict_factory
        cursor = self.db.sqlite_connection.cursor()
        sqlite_select_query = '''
            SELECT * FROM sqlitedb_users WHERE id='{}' 
        '''.format(user_id)
        cursor.execute(sqlite_select_query)
        self._data = cursor.fetchone()
        cursor.close()
        return self._data

    '''
    
        Создаем таблицу пользователя с полями
    
    '''
    def create_table(self):
        sqlite_create_table_query = '''
        CREATE TABLE {} (
            id INT PRIMARY KEY,
            tab VARCHAT(255) NULL,
            depatment VARCHAT(255) NULL,
            phone VARCHAR(12) NULL,
            name VARCHAR(255) NULL,
            last_name VARCHAR(255) NULL,
            sure_name VARCHAR(255) NULL,
            admin INTEGER DEFAULT 0 NOT NULL,
            test1 VARCHAR(255) NULL,
            menu VARCHAR(255) NULL,
            test_id INT NULL,
            quest_id INT NULL
            )'''.format(self._table_name)
        cursor = self.db.sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        cursor.execute(sqlite_create_table_query)
        self.db.sqlite_connection.commit()
        print("Таблица SQLite создана")
        cursor.close()


    def add(self, id):
        '''
            Создаем пользователя в бд

            id - id пользователя в telegram
        '''
        # если уже такой есть
        # то не создаем
        if(self.get(id)):
            return
        sqlite_create_table_query = '''
        INSERT INTO sqlitedb_users 
            (id) 
        VALUES 
            ('{}')
        '''.format(id)
        print(sqlite_create_table_query)
        cursor = self.db.sqlite_connection.cursor()
        cursor.execute(sqlite_create_table_query)
        self.db.sqlite_connection.commit()
        cursor.close()
        return id



    def update(self, update):
        '''
            Обновляем пользователя

            update - обновленая запись из таблица пользователей
        '''
        # останавливаемся если нет такого пользователя
        if(not self.get(update['id'])):
            return
        '''
            Выписаваем в отдельное место 
            id пользовтеля
            что бы удалить из словаря
        '''
        user_id = update['id']
        del update['id']
        '''
            Выписаваем в отдельное место 
            id пользовтеля
            что бы удалить из словаря
        '''


        '''
            Формируем строку update для
            таблице пользователя по словарю
        '''
        _update = ''
        for key_col in update.keys():
            if _update != '':
                _update += ', '
            _update += '''
            {} = '{}' 
            '''.format(key_col, update[key_col]) 
        '''
            Формируем строку update для
            таблице пользователя по словарю
        '''


        sqlite_create_table_query = '''
            UPDATE sqlitedb_users 
            SET {}
            WHERE id = '{}' 
        '''.format(_update,user_id)
        cursor = self.db.sqlite_connection.cursor()
        cursor.execute(sqlite_create_table_query)
        self.db.sqlite_connection.commit()
        cursor.close()
        update['id'] = user_id


    def get_count_users(self):
        '''
            Количество пользователей в бд
        '''
        # перевод tuple в dict
        self.db.sqlite_connection.row_factory = self.dict_factory
        cursor = self.db.sqlite_connection.cursor()
        sqlite_select_query = '''
            SELECT COUNT(*) c FROM sqlitedb_users
        '''
        cursor.execute(sqlite_select_query)
        c = cursor.fetchone()
        cursor.close()
        return c['c']

    
    def get_users(self):
        '''
            Получаем всех пользователей
        '''
        # перевод tuple в dict
        self.db.sqlite_connection.row_factory = self.dict_factory
        cursor = self.db.sqlite_connection.cursor()
        sqlite_select_query = '''
            SELECT * FROM sqlitedb_users
        '''
        cursor.execute(sqlite_select_query)
        data = cursor.fetchall()
        cursor.close()
        return data

class TestModel(CustomModel):
    """
        Модель для теста
    """

    _table_name = 'sqlitedb_test'
    last_id = -1


    def get(self, test_id):
        super().__init__()
        self.db.sqlite_connection.row_factory = self.dict_factory
        cursor = self.db.sqlite_connection.cursor()
        sqlite_select_query = '''
            SELECT * FROM sqlitedb_test 
            WHERE id = '{}' 
        '''.format(test_id)
        cursor.execute(sqlite_select_query)
        self._data = cursor.fetchone()
        cursor.close()


    def add(self, name):
        """
            Добавляем тест
        """
        if self.get_test_name(name):
            return False
        sqlite_create_table_query = '''
        INSERT INTO sqlitedb_test 
            (name) 
        VALUES 
            ('{}')'''.format(name)  
        cursor = self.db.sqlite_connection.cursor()
        cursor.execute(sqlite_create_table_query)
        self.db.sqlite_connection.commit()
        cursor.close()
        self.last_id = cursor.lastrowid
        self._data = {
            'id':cursor.lastrowid
        }
        return True


    def get_test_name(self, name):
        """
            Вернуть тест по названию
        """
        self.db.sqlite_connection.row_factory = self.dict_factory
        cursor = self.db.sqlite_connection.cursor()
        sqlite_select_query = '''SELECT * FROM sqlitedb_test 
            WHERE name = '{}' '''.format(name)
        cursor.execute(sqlite_select_query)
        total_rows = cursor.fetchone()
        self._data = total_rows
        cursor.close()
        if total_rows is None:
            return False
        return total_rows

    
    def create_table(self):
        """
            Создаем таблицу для тестов
        """
        sqlite_create_table_query = '''
        CREATE TABLE {} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL
        )'''.format(self._table_name)
        cursor = self.db.sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        cursor.execute(sqlite_create_table_query)
        self.db.sqlite_connection.commit()
        print("Таблица SQLite создана")
        cursor.close()
    

    def get_quest(self):
        """
            Вернуть вопросы по id 
        """
        self.db.sqlite_connection.row_factory = self.dict_factory
        cursor = self.db.sqlite_connection.cursor()
        sqlite_select_query = '''SELECT * FROM sqlitedb_quest
            WHERE id = '{}' '''.format(self._data['id'])
        cursor.execute(sqlite_select_query)
        self.quest = cursor.fetchall()
        cursor.close()
        return self.quests

    def get_quests(self):
        """
            Вернуть вопросы в этом тесте 
        """
        self.db.sqlite_connection.row_factory = self.dict_factory
        cursor = self.db.sqlite_connection.cursor()
        sqlite_select_query = '''SELECT * FROM sqlitedb_quest
            WHERE test_id = '{}' '''.format(self._data['id'])
        cursor.execute(sqlite_select_query)
        self.quests = cursor.fetchall()
        cursor.close()
        return self.quests

    
    def get_tests(self):
        """
            Вернем все тесты
        """
        self.db.sqlite_connection.row_factory = self.dict_factory
        cursor = self.db.sqlite_connection.cursor()
        sqlite_select_query = '''SELECT * FROM sqlitedb_test'''
        cursor.execute(sqlite_select_query)
        self.tests = cursor.fetchall()
        cursor.close()
        return self.tests

    
    # def get_user_has_test(self, user_id):
    #     """
    #         Пройдет ли тест пользотвалем
    #     """
    #     self.db.sqlite_connection.row_factory = self.dict_factory
    #     cursor = self.db.sqlite_connection.cursor()
    #     sqlite_select_query = '''SELECT * FROM sqlitedb_quest WHERE '''
    #     cursor.execute(sqlite_select_query)
    #     self.tests = cursor.fetchall()
    #     cursor.close()
    #     return self.tests

        

class QuestModel(CustomModel):
    """
        Модель к вопросу
    """

    _table_name = 'sqlitedb_quest'
    last_id = -1


    def get(self, quest_id):
        self.db.sqlite_connection.row_factory = self.dict_factory
        cursor = self.db.sqlite_connection.cursor()
        sqlite_select_query = '''
            SELECT * FROM sqlitedb_quest
            WHERE id = '{}' 
        '''.format(quest_id)
        cursor.execute(sqlite_select_query)
        self._data = cursor.fetchone()
        cursor.close()


    def create_table(self):
        """
            Создаем таблицу вопросов 
        """
        sqlite_create_table_query = '''
        CREATE TABLE {} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id INT NOT NULL,
            quest VARCHAR(255) NOT NULL,
            answer VARCHAR(255) NULL
        )'''.format(self._table_name)
        cursor = self.db.sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        cursor.execute(sqlite_create_table_query)
        self.db.sqlite_connection.commit()
        print("Таблица SQLite создана")
        cursor.close()


    def add(self, test_id, quest):
        """
            Добавляем вопрос
        """
        sqlite_create_table_query = '''
        INSERT INTO sqlitedb_quest 
            (test_id, quest) 
        VALUES 
            ('{}', '{}')'''.format(test_id, quest)  
        cursor = self.db.sqlite_connection.cursor()
        cursor.execute(sqlite_create_table_query)
        self.db.sqlite_connection.commit()
        cursor.close()
        self.last_id = cursor.lastrowid
        return True


class AnswerModel(CustomModel):
    """
        Модель ответа пользователя
    """

    _table_name = 'sqlitedb_answer'


    def create_table(self):
        """
            Создаем таблицу для ответов пользователя
        """
        sqlite_create_table_query = '''
        CREATE TABLE {} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quest_id INT NOT NULL,
            answer VARCHAR(255) NULL,
            user_id INT NOT NULL,
            date_create datetime default current_timestamp
        )'''.format(self._table_name)
        cursor = self.db.sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        cursor.execute(sqlite_create_table_query)
        self.db.sqlite_connection.commit()
        print("Таблица SQLite создана")
        cursor.close()

    
    def add(self, quest_id, user_id):
        """
            Добавляем ответ на вопрос
        """
        sqlite_create_table_query = '''
        INSERT INTO sqlitedb_answer   
            ('quest_id', 'user_id')
        VALUES 
            ('{}','{}')
        '''.format(quest_id, user_id)  
        cursor = self.db.sqlite_connection.cursor()
        cursor.execute(sqlite_create_table_query)
        self.db.sqlite_connection.commit()
        cursor.close()
        self.last_id = cursor.lastrowid
        return True

    def update(self, answer_id, answer):
        """
            Добавляем ответ на вопрос
        """
        sqlite_create_table_query = '''
        UPDATE sqlitedb_answer SET  
            answer = '{}'
        WHERE id = '{}' 
        '''.format(answer, answer_id)  
        cursor = self.db.sqlite_connection.cursor()
        cursor.execute(sqlite_create_table_query)
        self.db.sqlite_connection.commit()
        cursor.close()
        self.last_id = cursor.lastrowid
        return True

    def get(self, user_id):
        """
            Получение ответов пользователя
        """
        self.db.sqlite_connection.row_factory = self.dict_factory
        cursor = self.db.sqlite_connection.cursor()
        sqlite_select_query = '''SELECT * FROM sqlitedb_answer
            WHERE user_id = '{}' '''.format(user_id)
        cursor.execute(sqlite_select_query)
        self.answer = cursor.fetchall()
        cursor.close()
        return self.answer