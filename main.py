from cgitb import text
import telebot
import config
import texts
import keyboards
import time
import matplotlib.pyplot as plt

from db_model import *


bot = telebot.TeleBot(config.token)

my_id = 1382412434


# 3 кнопки

@bot.message_handler(commands=['start'])
def welcome_handler(message):
    """
        Просто вывод тест "Добро пожаловать" и 
        запуст инциализации пользователя
    """
    user = UserModel()
    user.add(message.from_user.id)

    # пока выставялем всем права админа
    u = user.get(message.from_user.id)
    u['admin'] = 1
    user.update(u)

    bot.send_message(message.from_user.id, texts.welcome_text)
    bot.register_next_step_handler(message, initialisation)


@bot.message_handler(commands=['admin'])
def admin(message):
    """
        Команда проверка админ или нет
    """
    _user = UserModel()
    user = _user.get(message.from_user.id)
    mrkp = keyboards.admin_panel()
    if message.from_user.id == my_id or user['admin'] == 1:
        bot.send_message(message.from_user.id, texts.hi_admin, reply_markup=mrkp)
    else:
        bot.send_message(message.from_user.id, texts.not_admin, reply_markup=mrkp)


@bot.message_handler(command=[texts.test_begin])
def test_begin(message):
    """
        Команда начать тест
    """
    user_start_test(message)


@bot.message_handler(content_types=['text'])
def main_handler(message):
    """
        Основной роут для теста из телеграмма
    """
    _user = UserModel()
    _user.get(message.from_user.id)
    user = _user.data()
    # если пользотателя нет в бд
    # то отправляем ввести ФИО
    if not user:
        welcome_handler(message)
        return


    txt = message.text.strip()
    if user['admin'] == 1 or message.from_user.id == my_id:
        if admin_menu(message) == True:
            return
    # test = db.get_test_f_quest(txt)
    # if test:
    #     bot.send_message(message.from_user.id, test['answer'])
    if txt == texts.all_tests:
        mrkp = keyboards.tests()
        #  если тестов в бд нет
        #  TODO: удалить кнопки у пользователя
        if len(mrkp.keyboard) == 0:
            bot.send_message(message.from_user.id, 'Сейчас нет тестов', reply_markup=mrkp)
            return
        bot.send_message(message.from_user.id, 
        'Все тесты', reply_markup=mrkp)
    elif txt == 'Меню' or txt == 'меню':
        mrkp = keyboards.main()
        bot.send_message(message.from_user.id, 'меню', reply_markup=mrkp)




    elif txt == texts.test_begin:
        """
            Запуск тест по слову
        """
        user_start_test(message)


    else:
        mrkp = keyboards.main()
        bot.send_message(message.from_user.id, 'не понимаю')


def user_start_test(message):
    """
        Вывод всех тестов в кноку при запросе
    """
    mrkp = keyboards.tests()
    bot.send_message(message.from_user.id, 'Выберите тест', reply_markup=mrkp)
    bot.register_next_step_handler(message, user_select_test)


def user_select_test(message):
    """
        Пользователь выбирает тест
    """
    # db = DbBot()
    # user = db.get_user(message.from_user.id)
    _user = UserModel()
    user = _user.get(message.from_user.id)
    print(user)
    txt = message.text.strip()
    #  ищем тест по названию
    _test = TestModel()
    test = _test.get_test_name(txt)
    if test:
        # обновляем пользователя
        data = {
            'id':user['id'],
            'test_id': test['id']
        }
        _user.update(data)
        # обновляем пользователя
        bot.send_message(message.from_user.id, texts.print_test_begin+'\n'+test['name'])
        # присылаем вопрос
        # _user_answer = AnswerModel()
        # user_answer = _user_answer.get(user['id'])
        # quests = _test.get_quests()
        # user['quest_id'] = quests[0]['id']
        # _user.update(user)
        # print(user,quests)
        # _user_answer.add(quests[0]['id'], user['id'])
        # bot.send_message(message.from_user.id, quests[0]['quest'])
        # bot.register_next_step_handler(message, test_user_set_answer)
        # bot.register_next_step_handler(message, test_user_send_quest)
        test_user_send_quest(message)
    
    else:
        bot.send_message(message.from_user.id, 'Нет такого теста')


def test_user_send_quest(message):
    """
        Прохождение теста 
        Отправялем пользователю вопрос
    """
    _user = UserModel()
    user = _user.get(message.from_user.id)
    txt = message.text.strip()
    # получаем всех вопросы
    _test = TestModel()
    test = _test.get(user['test_id'])
    print(user)
    quests = _test.get_quests()

    _user_answer = AnswerModel()
    user_answer = _user_answer.get(user['id'])
    if not user_answer:
        # если пользователь еще не ответит не на один вопрос
        # добавляем запись о начале вопроса
        user['quest_id'] = quests[0]['id']
        _user.update(user)
        _user_answer.add(quests[0]['id'], user['id'])
        bot.send_message(message.from_user.id, quests[0]['quest'])
        bot.register_next_step_handler(message, test_user_set_answer)
        return
    else:
        # ответ хотя бы на один вопрос
        for quest in quests:
            if int(quest['id']) > int(user_answer[-1]['quest_id']):
                _user_answer.add(quest['id'], user['id'])
                user['quest_id'] = quest['id']
                _user.update(user)
                bot.send_message(message.from_user.id, quest['quest'])
                bot.register_next_step_handler(message, test_user_set_answer)
                return
    # если выше условия не сработали
    # значит тест завершен
    bot.send_message(message.from_user.id, texts.test_end)
    '''
    # получаем все ответы пользователя
    answer = db.get_answers_user(user)
    for i, val in enumerate(quests):
        # ищем номер пол количеству ответов пользователя
        # вопросы на которые еще не отвечал
        if len(answer) == i:
            db.add_user_answer(val['id'], txt, user['id'] + ' \n {} == {}'.format(len(answer), len(quests)))
            if(i + 1 < len(quests)):
                bot.send_message(message.from_user.id, quests[i+1]['quest'])
        
    # снова получаем список ответов пользователя
    answer = db.get_answers_user(user)
    # если количество вопрос = количество ответов
    # то завершаем тест
    if(len(answer)==len(quests)):
        bot.send_message(message.from_user.id, texts.end_test)
    else:
        bot.register_next_step_handler(message, test_user_send_quest)
    '''

def test_user_set_answer(message):
    """
        Сохранение ответа пользователя на вопрос
    """
    _user = UserModel()
    user = _user.get(message.from_user.id)
    txt = message.text.strip()
    # получаем всех вопросы
    _test = TestModel()
    test = _test.get(user['test_id'])
    quests = _test.get_quests()

    _user_answer = AnswerModel()
    user_answer = _user_answer.get(user['id'])

    _user_answer.update(user_answer[-1]['id'], txt)
    bot.send_message(message.from_user.id, texts.test_save_asnwer)
    test_user_send_quest(message)
    # bot.register_next_step_handler(message, test_user_send_quest)


def admin_menu(message):
    """
        Меню админа
    """
    _user = UserModel()
    user = _user.get(message.from_user.id)
    txt = message.text.strip()
    if txt == texts.ad_new_test:
        bot.send_message(message.from_user.id, 'Назовите тест')
        bot.register_next_step_handler(message, create_new_test)
        return True

    if txt == texts.ad_text2:
        bot.send_message(message.from_user.id, 'Выбирете тест')
        diagrama_select_test(message)
        bot.register_next_step_handler(message, diagrama)
        return True
    return False


def create_new_test(message):
    """
        Создание нового теста
    """
    _user = UserModel()
    user = _user.get(message.from_user.id)
    txt = message.text.strip()
    test = TestModel()
    if not test.add(txt):
        bot.send_message(message.from_user.id, 
        '''Такой тест уже есть.\n\nВведите другое название''')
        bot.register_next_step_handler(message, create_new_test)
        return
    # записываем id теста которые добавлили
    user['test_id'] = test.last_id
    _user.update(user)
    # при создание теста, вопросы пустые
    number_quest = 1
    bot.send_message(message.from_user.id, f'Введите вопрос #{number_quest}')
    bot.register_next_step_handler(message, create_new_test_quest)


def create_new_test_quest(message):
    """
        Создание нового вопроса в тесте
    """
    _user = UserModel()
    user = _user.get(message.from_user.id)
    txt = message.text.strip()
    quest = QuestModel()
    quest.add(user['test_id'], txt)
    user['quest_id'] = quest.last_id
    _user.update(user)

    test = TestModel()
    test.get(user['test_id'])
    test.get_quests()
    number_quest = len(test.quests)

    bot.send_message(message.from_user.id, f'Ответ на вопрос #{number_quest}')
    bot.register_next_step_handler(message, create_new_quest_answer)


def create_new_quest_answer(message):
    """
        Добавляем ответ на вопрос
    """
    _user = UserModel()
    user = _user.get(message.from_user.id)
    txt = message.text.strip()

    quest = QuestModel()
    quest.get(user['quest_id'])
    answer = AnswerModel()
    answer.add(quest.data()['id'], txt)

    test = TestModel()
    test.get(user['test_id'])
    test.get_quests()
    number_quest = len(test.quests)


    bot.send_message(message.from_user.id, f'Вопрос сохранен #{number_quest}')
    bot.send_message(message.from_user.id, f'Записать еще вопрос (Да/Нет)')
    bot.register_next_step_handler(message, more_add_quest)


def more_add_quest(message):
    """
        Добавить еще один вопрос?
    """
    _user = UserModel()
    user = _user.get(message.from_user.id)
    txt = message.text.strip()
    if txt.lower() == 'нет':
        user['test_id'] = -1
        user['quest_id'] = -1
        _user.update(user)
        bot.send_message(message.from_user.id, 'Тест сохранен')
        return
    

    quest = QuestModel()
    quest.get(user['quest_id'])
    answer = AnswerModel()
    answer.add(quest.data()['id'], txt)

    test = TestModel()
    test.get(user['test_id'])
    test.get_quests()
    number_quest = len(test.quests) + 1
    bot.send_message(message.from_user.id, f'Введите вопрос #{number_quest}')
    bot.register_next_step_handler(message, create_new_test_quest)



@bot.message_handler(content_types=['start_test'])
def start_test(message):
    print('start test', message.from_user.id)


def initialisation(message):
    mrkp = keyboards.main()
    _user = UserModel()
    user = _user.get(message.from_user.id)
    fio = message.text.split(' ')
    print(user)
    print(fio)
    if len(fio) == 3:
        user['last_name'] = fio[0]
        user['name'] = fio[1]
        user['sure_name'] = fio[2]
        _user.update(user)
        if not user:
            bot.send_message(message.from_user.id, "not validata fio")
            bot.register_next_step_handler(message, initialisation)
        else:
            bot.send_message(message.from_user.id, 'Сохранено ФИО:\n{} {} {}'.format(fio[0], fio[1], fio[2]),
                             reply_markup=mrkp)
    else:
        bot.send_message(message.from_user.id, "not validata fio")
        bot.register_next_step_handler(message, initialisation)


def testing(message):
    pass

# def testing(message):
#     # global score
#     # global current_q
#     # global current_test
#     # global q_num
#     questions = current_test.keys()
#     q_num = len(questions)
#     if current_q < q_num:
#         bot.send_message(message.from_user.id, list(questions)[current_q])
#         bot.register_next_step_handler(message, correct_answer)
#     else:
#         mrkp = keyboards.main()
#         bot.send_message(message.from_user.id,
#                          f'Вы прошли тест, поздравляю, вы ответили на {str(score)} из {str(len(tests.t))} вопросов правильно')
#         connection = sqlite3.connect('sqlite_python.db')
#         cursor = connection.cursor()
#         sqlite_create_table_query = '''UPDATE sqlitedb_users
#         SET test1 = '{}' WHERE id = '{}' '''.format(str(score), message.from_user.id)
#         cursor.execute(sqlite_create_table_query)
#         connection.commit()
#         cursor.close()
#         current_q = 0
#         score = 0


# def correct_answer(message):
#     # вставить обработчик времени если кончилось время current_q = q_num
#     global score
#     global current_q
#     global current_test
#     ans = message.text.lower()
#     # print(ans)
#     key = list(current_test.keys())[current_q]
#     # print(key)
#     # print(current_test[key])
#     if ans in current_test[key]:
#         score += 1
#         print(score)
#     current_q += 1
#     testing(message)


def diagrama_select_test(message):
    _user = UserModel()
    user = _user.get(message.from_user.id)
    txt = message.text.strip()
    # получаем всех вопросы
    _test = TestModel()
    # test = _test.get(user['test_id'])
    mrkp = keyboards.tests()
    bot.send_message(message.from_user.id, 
    'Все тесты', reply_markup=mrkp)
    


def diagrama(message):
    # if message == texts.ad_text:
    _user = UserModel()
    user = _user.get(message.from_user.id)
    txt = message.text.strip()
    # получаем всех вопросы
    _test = TestModel()
    test = _test.get_test_name(txt)
    quests = _test.get_quests()

    # данные для диаграммы
    sizes = []
    # всех пользователй
    users = _user.get_users()

    # количество пользователей пршедших тест
    has_answer = 0
    for u in users:
        _answer = AnswerModel()
        answer = _answer.get(u['id'])
        # если пользовтеля нет и его ответов
        # смотрим следующего пользователя
        if u and not answer:
            continue
        if quests[-1]['id'] == answer[-1]['quest_id']:
            has_answer += 1

    sizes.append(has_answer)
    sizes.append(len(users) - has_answer)


    labels = 'прошли тест', 'не прошли тест'
    # sizes = [15, 30]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels)
    plt.savefig('saved_figure.png')
    img = open('saved_figure.png', 'rb')
    bot.send_photo(message.chat.id, img)


if __name__ == '__main__':
    '''
        Проверяем наличие таблиц в бд и отключаемся

        Работает только при запуске python main.py
    '''
    model = CustomModel()
    model.check_model()
    # db = DbBot()
    # дисконект от дб
    # del db
    bot.polling(none_stop=True)
