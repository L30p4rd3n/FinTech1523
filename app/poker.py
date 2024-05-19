import random


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value} {self.suit}"


class Deck:
    def __init__(self):
        self.cards = []
        suits = ['Червы', 'Бубны', 'Трефы', 'Пики']
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Валет', 'Дама', 'Король', 'Туз']
        for suit in suits:
            for value in values:
                self.cards.append(Card(suit, value))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 0:
            return self.cards.pop(0)
        else:
            return None


class PokerHand:
    def __init__(self):
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def __str__(self):
        return ", ".join(str(card) for card in self.hand)

    def has_pair(self):
        values = [card.value for card in self.hand]
        for value in set(values):
            if values.count(value) == 2:
                return True
        return False

    def has_two_pairs(self):
        values = [card.value for card in self.hand]
        pairs = 0
        for value in set(values):
            if values.count(value) == 2:
                pairs += 1
        return pairs == 2

    def has_three_of_a_kind(self):
        values = [card.value for card in self.hand]
        for value in set(values):
            if values.count(value) == 3:
                return True
        return False

    def has_straight(self):
        values = [card.value for card in self.hand]
        straight_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Валет', 'Дама', 'Король', 'Туз']
        values.sort(key=lambda x: straight_values.index(x))
        return len(set(values)) == 5 and straight_values.index(values[-1]) - straight_values.index(values[0]) == 4

    def has_flush(self):
        suits = [card.suit for card in self.hand]
        return len(set(suits)) == 1

    def determine_hand(self, table_hand):
        all_cards = self.hand + table_hand
        if self.has_straight() and self.has_flush():
            return "Стрит-флеш"
        elif self.has_three_of_a_kind():
            return "Тройка"
        elif self.has_two_pairs():
            return "Две пары"
        elif self.has_pair():
            return "Пара"
        elif self.has_flush():
            return "Флеш"
        elif self.has_straight():
            return "Стрит"
        else:
            return "Нет комбинации"



def determine_winner(player_hand, bot_hand, table_hand):
    player_combination = player_hand.determine_hand(table_hand)
    bot_combination = bot_hand.determine_hand(table_hand)

    combinations = [
        "Нет комбинации",
        "Пара",
        "Две пары",
        "Тройка",
        "Стрит",
        "Флеш",
        "Стрит-флеш"

    ]

    player_strength = combinations.index(player_combination)
    bot_strength = combinations.index(bot_combination)

    if player_strength > bot_strength:
        return "Игрок победил!"
    elif player_strength < bot_strength:
        return "Бот победил!"
    else:
        # Если комбинации одинаковы, сравниваем старшие карты
        player_values = [card.value for card in player_hand.hand]
        bot_values = [card.value for card in bot_hand.hand]

        player_values.sort(reverse=True)
        bot_values.sort(reverse=True)

        if (player_values[0] > bot_values[0]):
            return "Игрок победил!"
        else:
            return "Бот победил!"


# Создаем колоду и перетасовываем ее
deck = Deck()
deck.shuffle()

# Раздаем карты игроку и боту
player_hand = PokerHand()
bot_hand = PokerHand()
for _ in range(2):
    player_hand.add_card(deck.deal())
    bot_hand.add_card(deck.deal())

# Раздаем карты на стол
table_hand = []
for _ in range(5):
    table_hand.append(deck.deal())

def play():

    a = player_hand.determine_hand(table_hand)
    b = bot_hand.determine_hand(table_hand)

    ", ".join(str(card) for card in table_hand)

    result = determine_winner(player_hand, bot_hand, table_hand)


    return {
        "player" : player_hand.__str__(),
        "bot" : bot_hand.__str__(),
        "table" : ", ".join(str(card) for card in table_hand),
        "playerwon" : 1
    } if result == "Бот победил!" else {
        "player": player_hand.__str__(),
        "bot": bot_hand.__str__(),
        "table": ", ".join(str(card) for card in table_hand),
        "playerwon": 0
    }
