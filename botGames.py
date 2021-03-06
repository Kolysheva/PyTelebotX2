import requests
from telebot import types
from menuBot import goto_menu


def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Карту!":
        game21 = getGame(chat_id)
        if game21 is None:  # если мы случайно попали в это меню, а объекта с игрой нет
            goto_menu(bot, chat_id, "Выход")
            return

        text_game = game21.get_cards(1)
        bot.send_media_group(chat_id, media=game21.mediaCards)  # получим и отправим изображения карт
        bot.send_message(chat_id, text=text_game)

        if game21.status is not None:  # выход, если игра закончена
            stopGame(chat_id)
            goto_menu(bot, chat_id, "Выход")
            return

    elif ms_text == "Стоп!":
        stopGame(chat_id)
        goto_menu(bot, chat_id, "Выход")
        return

    elif ms_text in GameRPS.values:
        gameRSP = getGame(chat_id)
        if gameRSP is None:  # если мы случайно попали в это меню, а объекта с игрой нет
            goto_menu(bot, chat_id, "Выход")
            return
        text_game = gameRSP.playerChoice(ms_text)
        bot.send_message(chat_id, text=text_game)
        gameRSP.newGame()


# -----------------------------------------------------------------------

activeGames = {}  # Тут будем накапливать все активные игры. У пользователя может быть только одна активная игра


def newGame(chatID, newGame):
    activeGames.update({chatID: newGame})
    return newGame


def getGame(chatID):
    return activeGames.get(chatID, None)


def stopGame(chatID):
    activeGames.pop(chatID, None)


# -----------------------------------------------------------------------
class Card:
    emo_SPADES = "U0002660"  # Unicod эмоджи Пики
    emo_CLUBS = "U0002663"  # Unicod эмоджи Крести
    emo_HEARTS = "U0002665"  # Unicod эмоджи Черви
    emo_DIAMONDS = "U0002666"  # Unicod эмоджи Буби

    def __init__(self, card):
        if isinstance(card, dict):  # если передали словарь
            self.__card_JSON = card
            self.code = card["code"]
            self.suit = card["suit"]
            self.value = card["value"]
            self.cost = self.get_cost_card()
            self.color = self.get_color_card()
            self.__imagesPNG_URL = card["images"]["png"]
            self.__imagesSVG_URL = card["images"]["svg"]
            # print(self.value, self.suit, self.code)

        elif isinstance(card, str):  # карту передали строкой, в формате "2S"
            self.__card_JSON = None
            self.code = card

            value = card[0]
            if value == "0":
                self.value = "10"
            elif value == "J":
                self.value = "JACK"
            elif value == "Q":
                self.value = "QUEEN"
            elif value == "K":
                self.value = "KING"
            elif value == "A":
                self.value = "ACE"
            elif value == "X":
                self.value = "JOKER"
            else:
                self.value = value

            suit = card[1]
            if suit == "1":
                self.suit = ""
                self.color = "BLACK"

            elif suit == "2":
                self.suit = ""
                self.color = "RED"

            else:
                if suit == "S":
                    self.suit = "SPADES"  # Пики
                elif suit == "C":
                    self.suit = "CLUBS"  # Крести
                elif suit == "H":
                    self.suit = "HEARTS"  # Черви
                elif suit == "D":
                    self.suit = "DIAMONDS"  # Буби

                self.cost = self.get_cost_card()
                self.color = self.get_color_card()

    def get_cost_card(self):
        if self.value == "JACK":
            return 2
        elif self.value == "QUEEN":
            return 3
        elif self.value == "KING":
            return 4
        elif self.value == "ACE":
            return 11
        elif self.value == "JOKER":
            return 1
        else:
            return int(self.value)

    def get_color_card(self):
        if self.suit == "SPADES":  # Пики
            return "BLACK"
        elif self.suit == "CLUBS":  # Крести
            return "BLACK"
        elif self.suit == "HEARTS":  # Черви
            return "RED"
        elif self.suit == "DIAMONDS":  # Буби
            return "RED"


# -----------------------------------------------------------------------
class Game21:
    def __init__(self, deck_count=1, jokers_enabled=False):
        new_pack = self.new_pack(deck_count, jokers_enabled)  # в конструкторе создаём новую пачку из deck_count-колод
        if new_pack is not None:
            self.pack_card = new_pack  # сформированная колода
            self.remaining = new_pack["remaining"],  # количество оставшихся карт в колоде
            self.card_in_game = []  # карты в игре
            self.arr_cards_URL = []  # URL карт игрока
            self.mediaCards = []
            self.score = 0  # очки игрока
            self.status = None  # статус игры, True - игрок выиграл, False - Игрок проиграл, None - Игра продолжается

    # ---------------------------------------------------------------------

    def new_pack(self, deck_count, jokers_enabled=False):
        txtJoker = "&jokers_enabled=true" if jokers_enabled else ""
        response = requests.get(f"https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count={deck_count}" + txtJoker)
        # создание стопки карт из "deck_count" колод по 52 карты
        if response.status_code != 200:
            return None
        pack_card = response.json()
        return pack_card

    # ---------------------------------------------------------------------
    def get_cards(self, card_count=1):
        if self.pack_card is None:
            return None
        if self.status is not None:  # игра закончена
            return None

        deck_id = self.pack_card["deck_id"]
        response = requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={card_count}")
        # достать из deck_id-колоды card_count-карт
        if response.status_code != 200:
            return False

        new_cards = response.json()
        if new_cards["success"] is not True:
            return False
        self.remaining = new_cards["remaining"]  # обновим в классе количество оставшихся карт в колоде

        arr_newCards = []
        for card in new_cards["cards"]:
            card_obj = Card(card)  # создаем объекты класса Card и добавляем их в список карт у игрока
            arr_newCards.append(card_obj)
            self.card_in_game.append(card_obj)
            self.score = self.score + card_obj.cost
            self.arr_cards_URL.append(card["image"])
            self.mediaCards.append(types.InputMediaPhoto(card["image"]))

        if self.score > 21:
            self.status = False
            text_game = "Очков: " + str(self.score) + " ВЫ ПРОИГРАЛИ!"

        elif self.score == 21:
            self.status = True
            text_game = "ВЫ ВЫИГРАЛИ!"
        else:
            self.status = None
            text_game = "Очков: " + str(self.score) + " в колоде осталось карт: " + str(self.remaining)

        return text_game


# -----------------------------------------------------------------------
class GameRPS:
    values = ["Камень", "Ножницы", "Бумага"]
    name = "Камень-Ножницы-Бумага"
    text_rules = "<b>Победитель определяется по следующим правилам:</b>\n" \
                 "1. Камень побеждает ножницы\n" \
                 "2. Бумага побеждает камень\n" \
                 "3. Ножницы побеждают бумагу\n"
    url_picRules = "https://i.ytimg.com/vi/Gvks8_WLiw0/maxresdefault.jpg"

    def __init__(self):
        self.computerChoice = self.__class__.getRandomChoice()

    def newGame(self):
        self.computerChoice = self.__class__.getRandomChoice()

    @classmethod
    def getRandomChoice(cls):
        lenValues = len(cls.values)
        import random
        rndInd = random.randint(0, lenValues - 1)
        return cls.values[rndInd]

    def playerChoice(self, player1Choice):
        winner = None

        code = player1Choice[0] + self.computerChoice[0]
        if player1Choice == self.computerChoice:
            winner = "Ничья!"
        elif code == "КН" or code == "БК" or code == "НБ":
            winner = "Игрок выиграл!"
        else:
            winner = "Компьютер выиграл!"

        return f"{player1Choice} vs {self.computerChoice} = " + winner


# -----------------------------------------------------------------------

# --------------------------


if __name__ == "__main__":
    print("Этот код должен использоваться ТОЛЬКО в качестве модуля!")
