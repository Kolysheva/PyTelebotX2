# ======================================= модуль ДЗ
# -----------------------------------------------------------------------
def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Задание-1":
        dz1(bot, chat_id)

    elif ms_text == "Задание-2":
        dz2(bot, chat_id)

    elif ms_text == "Задание-3":
        dz3(bot, chat_id)

    elif ms_text == "Задание-4":
        dz4(bot, chat_id)

    elif ms_text == "Задание-5":
        dz5(bot, chat_id)

    elif ms_text == "Задание-6":
        dz6(bot, chat_id)

# -----------------------------------------------------------------------


def dz1(bot, chat_id):
    name = "Poline "
    bot.send_message(chat_id, text=f"Привет, меня зовут Полина, я могу делать некоторые веши {name*4}")
# -----------------------------------------------------------------------


def dz2(bot, chat_id):
    my_inputInt(bot, chat_id, "Напомни-ка сколько тебе лет?", dz2_ResponseHandler)


def dz2_ResponseHandler(bot, chat_id, age_int):
    if age_int < 0:
        bot.send_message(chat_id, text=f"О! тебе всего {age_int}! \n кажется ты еще даже не родился..."
                                       f" Твое время еще придет.")

    elif age_int > 100:
        bot.send_message(chat_id, text=f"{age_int}! \n Вам не сюда надо, а в книгу рекордов.")

    elif age_int > 7:
        bot.send_message(chat_id, text=f"Тебе {age_int}, самое время изучать Пайтон!")

    else:
        bot.send_message(chat_id, text=f"ну и о чем мне шутить")
# -----------------------------------------------------------------------


def dz3(bot, chat_id):
    my_inputInt(bot, chat_id, "Реши мне задачу: \n 2^0+2-2=?", dz3_ResponseHandler)


def dz3_ResponseHandler(bot, chat_id, num_int):
    if num_int == 1:
        bot.send_message (chat_id, text="Молодец!")
    else:
        bot.send_message (chat_id, text="Кажется тебе надо обратить внимание на внимательность")
# -----------------------------------------------------------------------


def dz4(bot, chat_id):
    dz4_ResponseHandler = lambda message: bot.send_message(chat_id, text=f"Я владею твои именем, {message.text[1:][:-1] }!")
    my_input(bot, chat_id, "Напомни-ка, как тебя зовут?", dz4_ResponseHandler)
# -----------------------------------------------------------------------


def dz5(bot, chat_id):
    my_inputInt(bot, chat_id, "Сколько вам лет?", dz5_ResponseHandler)


def dz5_ResponseHandler(bot, chat_id, age_int):
    bot.send_message(chat_id, text=f"Тебе {age_int}! \nА через год будет уже {age_int+1}!")
# -----------------------------------------------------------------------


def dz6(bot, chat_id):
    dz6_ResponseHandler = lambda message: bot.send_message(chat_id,
                                                           f"Добро пожаловать {message.text}! У тебя красивое имя, в нём {len(message.text)} букв!")
    my_input(bot, chat_id, "Как тебя зовут?", dz6_ResponseHandler)

# -----------------------------------------------------------------------


def my_input(bot, chat_id, txt, ResponseHandler):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, ResponseHandler)
# -----------------------------------------------------------------------


def my_inputInt(bot, chat_id, txt, ResponseHandler):

    # bot.send_message(chat_id, text=botGames.GameRPS_Multiplayer.name, reply_markup=types.ReplyKeyboardRemove())

    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, my_inputInt_SecondPart, botQuestion=bot, txtQuestion=txt, ResponseHandler=ResponseHandler)
    # bot.register_next_step_handler(message, my_inputInt_return, bot, txt, ResponseHandler)  # то-же самое, но короче


def my_inputInt_SecondPart(message, botQuestion, txtQuestion, ResponseHandler):
    chat_id = message.chat.id
    try:
        if message.content_type != "text":
            raise ValueError
        var_int = int(message.text)
        # данные корректно преобразовались в int, можно вызвать обработчик ответа, и передать туда наше число
        ResponseHandler(botQuestion, chat_id, var_int)
    except ValueError:
        botQuestion.send_message(chat_id,
                         text="Можно вводить ТОЛЬКО целое число в десятичной системе исчисления "
                              "(символами от 0 до 9)!\nПопробуйте еще раз...")
        my_inputInt(botQuestion, chat_id, txtQuestion, ResponseHandler)  # это не рекурсия, но очень похоже
        # у нас пара процедур, которые вызывают друг-друга, пока пользователь не введёт корректные данные,
        # и тогда этот цикл прервётся, и управление перейдёт "наружу", в ResponseHandler

# -----------------------------------------------------------------------
