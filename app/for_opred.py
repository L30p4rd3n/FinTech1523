import random
from flask import flash, request

riskovo = 0


class FinancialSimulator:
    def __init__(self):
        self.goal = 1000000  # Цель в миллионах рублей
        self.starting_capital = 0  # Стартовый капитал в рублях
        self.current_capital = self.starting_capital
        self.salary = 20000
        self.tax_rate = 0.05
        self.month = 1
        self.is_game_over = False
        self.risk = 0
        self.stabilnost = 0

    def show_status(self):
        flash(f"Месяц {self.month}")
        flash(f"Текущий капитал: {self.current_capital} рублей")
        flash(f"Цель: {self.goal} рублей")

    def earn_salary(self):
        flash(f"Вы получили зарплату! Целых {self.salary / 1000} тыщ рублей")
        self.current_capital += self.salary

    def pay_tax(self):
        tax_amount = self.current_capital * self.tax_rate
        flash(f"Вы заплатили налог в размере {tax_amount} рублей.")
        self.current_capital -= tax_amount

    def invest_stable(self, amount):
        # Стабильные инвестиции: небольшой, но стабильный доход
        income = amount * 0.05  # Пример стабильного дохода
        self.stabilnost += 10
        self.current_capital += income
        flash(f"Вы инвестировали {amount} рублей в стабильные инвестиции.")
        flash(f"Ваш стабильный доход: {income} рублей")

    def invest_risky(self, amount):
        # Рискованные инвестиции: более высокий доход с шансом на потерю
        chance = random.random()  # Генерация случайного шанса (от 0 до 1)
        self.risk += 5
        if chance < 0.5:  # 50% шанс потерять инвестицию
            loss = amount * 0.3  # Пример потери
            self.current_capital -= loss
            flash(f"Вы потеряли {loss} рублей на рискованных инвестициях.")
        else:
            income = amount * 0.2  # Пример дохода
            self.current_capital += income
            flash(f"Вы инвестировали {amount} рублей в рискованные инвестиции.")
            flash(f"Ваш доход: {income} рублей")

    def withdraw(self, amount):
        # Вывод средств из инвестиций
        if self.current_capital >= amount:
            self.current_capital -= amount
            flash(f"Вы вывели {amount} рублей из инвестиций.")
        else:
            flash("У вас недостаточно средств для вывода.")

    def invest(self):
        flash("Выберите тип инвестиций:")
        flash("1. Стабильные инвестиции")
        flash("2. Рискованные инвестиции")
        flash("3. Вывести деньги из инвестиций")

        def choice():
            flash("Введите номер выбранного вида инвестиций: ")
            choice = request.form.get('inputText')
            return choice

        if choice == '1':
            flash("Введите сумму для стабильных инвестиций: ")
            amount = request.form.get()
            self.invest_stable(amount)
        elif choice == '2':
            amount = float(input("Введите сумму для рискованных инвестиций: "))
            self.invest_risky(amount)
        elif choice == '3':
            amount = float(input("Введите сумму для вывода из инвестиций: "))
            self.withdraw(amount)
        else:
            print("Некорректный выбор.")

    def random_event(self):
        event = random.randint(1, 3)
        if event == 1:
            flash("Счастливый месяц! Вы получили бонус в размере 5000 рублей!")
            self.current_capital += 5000
        elif event == 2:
            flash("Несчастливый месяц! Ваши расходы увеличились на 2000 рублей.")
            self.current_capital -= 2000
        else:
            flash("Этот месяц прошел спокойно без событий.")

    def play(self):
        while not self.is_game_over:
            self.show_status()
            self.earn_salary()
            self.pay_tax()
            self.random_event()

            flash("Что вы хотите сделать?")
            flash("1. Инвестировать")
            flash("2. Сыграть в казино")
            flash("3. Пропустить этот ход")


            choice = input("Выберите действие: ")

            if choice == '1':
                self.invest()
            elif choice == '2':
                self.play_casino()
                self.risk += 10
            if self.risk >= 100:
                self.is_game_over = True
                flash("Wow")
                flash("Похоже ты слишком часто рискуешь")
            self.month += 1
            if self.current_capital >= self.goal:
                flash("Поздравляем! Вы достигли своей финансовой цели!")
                self.is_game_over = True
            elif self.current_capital <= 0:
                flash(f"Вы банкрот. Игра окончена. Вы продержались {self.month} ход")
                self.is_game_over = True
        return [self.risk, self.stabilnost]

    def play_casino(self):
        flash("Вы решили поиграть в казино.")
        result = casino_game(self.current_capital)
        self.current_capital += result


def dice_game(bet_amount):
    dice_roll = random.randint(1, 6)
    dice_roll_comp = random.randint(1, 6)

    flash(f"Вы бросили кости и выпало: {dice_roll}")
    flash(f"Казино бросило кости и выпало: {dice_roll_comp}")

    if dice_roll > dice_roll_comp:
        flash(f"Поздравляем! Вы выиграли {bet_amount} рублей!")
        return bet_amount
    elif dice_roll < dice_roll_comp:
        flash("К сожалению, вы проиграли.")
        return -bet_amount
    else:
        flash("Ничья! Ваши деньги возвращаются.")
        return 0


def slot_machine_game():
    bet_amount = 1000  # Ставка на автомате всегда 1000 рублей

    symbols = ['♠', '♣', '♥', '♦']
    slot1 = random.choice(symbols)
    slot2 = random.choice(symbols)
    slot3 = random.choice(symbols)

    flash(f"Автомат показывает: {slot1} {slot2} {slot3}")

    if slot1 == slot2 == slot3:
        flash(f"Поздравляем! Вы выиграли {bet_amount * 10} рублей!")
        return bet_amount * 10
    else:
        flash("К сожалению, вы проиграли.")
        return -bet_amount


def casino_game(capital):
    play_again = True
    itog = 0
    while play_again:
        flash("Добро пожаловать в казино!")
        flash("Выберите игру:")
        flash("1. Игра в кости")
        flash("2. Игровые автоматы")

        choice = flash("Выберите номер игры: ")

        if choice == '1':
            bet = int(input("Введите сумму ставки для игры в кости: "))
            if capital >= bet:
                itog += dice_game(bet)
            else:
                flash("У вас недостаточно средств для игры.")

        elif choice == '2':
            flash("Вы играете на игровых автоматах за 1000 рублей.")
            itog += slot_machine_game()
        else:
            flash("Некорректный выбор.")
            return casino_game(capital)

        flash(f"Ваш результат: {itog} рублей")

        play_again_input = input("Хотите сыграть еще раз? (да/нет): ")
        play_again = play_again_input.lower() == 'да'
    return itog


def launch_a_game():
    game = FinancialSimulator()
    flash(game.play())
    return