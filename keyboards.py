from gc import callbacks
from telebot import types
import texts
from db import *
from db_model import *


def main():
    markup = types.ReplyKeyboardMarkup()
    test_begin = types.KeyboardButton(texts.test_begin)
    all_tests = types.KeyboardButton(texts.all_tests)
    markup.row(test_begin)
    markup.row(all_tests)

    return markup


def tests():
    # TODO: подправить для большего количества тестов
    # ограничение 10 строк
    markup = types.ReplyKeyboardMarkup()
    db = TestModel()
    tests = db.get_tests()
    # если нет тестов
    if not tests:
        return types.ReplyKeyboardMarkup()


    for test in tests:
        print(test)
        markup.row(types.KeyboardButton(test['name']))

    return markup


def test_test():
    markup = types.ReplyKeyboardMarkup()
    t = types.KeyboardButton("Проверочный тест")
    markup.row(t)
    return markup

def admin_panel():
    markup = types.ReplyKeyboardMarkup()
    analitica = types.KeyboardButton(texts.ad_text)
    stat = types.KeyboardButton(texts.ad_text1)
    diag = types.KeyboardButton(texts.ad_text2)
    new_test = types.KeyboardButton(texts.ad_new_test)
    markup.row(analitica)
    markup.row(stat)
    markup.row(diag)
    markup.row(new_test)
    return markup
