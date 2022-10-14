import random
from random import randrange


class Bot:

    def __init__(self, win_objective):
        self.win_objective = win_objective  # True=win or False=lose
        self.amount = int()
        self.current_sum = int()
        self.winning_amount = 100
        self.cant_lose = 99
        self.dream_number = 89
        self.max_amount = 10
        self.mid_amount = 5
        self.small_amount = 2

    def __repr__(self):
        return self.__class__.__name__

    def give_sum(self, _sum):
        self.current_sum = _sum
        if not self.get_to_approx_sixty():
            if self.win_objective:
                WinnerBot.apply_strategy(self)
            else:
                LoserBot.apply_strategy(self)
        self.output_current_sum()

    def register(self, amount):
        """registers the amount to a self attr"""
        self.amount = amount

    def output_current_sum(self):
        print(f"{self} added {self.amount} to the sum")

    def get_to_approx_sixty(self):
        """we dont really care much about the sum strategy before 60"""
        if 60 - self.current_sum >= self.max_amount:
            self.register(self.max_amount)
            return True
        elif 60 - self.current_sum >= self.mid_amount:
            self.register(self.mid_amount)
            return True
        elif 60 - self.current_sum >= self.small_amount:
            self.register(self.small_amount)
            return True
        return False

    @staticmethod
    def consecutive_ints(first, second):
        return True if first + 1 == second else False

    def possible_to_get_to_(self, amount):
        return True if amount - self.current_sum <= self.max_amount else False


class WinnerBot(Bot):

    def __init__(self):
        super(WinnerBot, self).__init__(win_objective=True)

    def apply_strategy(self):
        if self.possible_to_get_to_(self.winning_amount):
            self.win()
        elif self.possible_to_get_to_(self.dream_number):
            self.get_to_dream_number()
        else:
            self.prepare_the_win()

    def win(self):
        amount_to_win = self.winning_amount - self.current_sum
        self.register(amount_to_win)

    def get_to_dream_number(self):
        amount_to_dream = self.dream_number - self.current_sum
        self.register(amount_to_dream)

    def prepare_the_win(self):
        for i in range(self.current_sum, self.current_sum + 10):
            if not self.consecutive_ints(int(str(i)[0]), int(str(i)[1])):
                continue
            else:
                self.register(i - self.current_sum)
                break
        else:
            self.register(10)


class LoserBot(Bot):

    def __init__(self):
        super(LoserBot, self).__init__(win_objective=False)

    def apply_strategy(self):
        if self.current_sum == self.cant_lose:
            self.sadly_win()
        elif self.possible_to_get_to_(self.cant_lose):
            self.force_opponent_win()
        elif self.possible_to_get_to_(self.winning_amount):
            self.avoid_winning()
        elif self.possible_to_get_to_(self.dream_number):
            self.avoid_dream_number()
        else:
            self.prepare_loss()

    def force_opponent_win(self):
        if self.current_sum in list(range(self.current_sum, self.winning_amount)):
            self.amount = self.cant_lose - self.current_sum

    def avoid_winning(self):
        possible_amounts = list(range(self.current_sum + 1, self.winning_amount))
        for i in possible_amounts:
            if i == self.winning_amount:
                self.sadly_win()
            elif len(possible_amounts) == 1 and i == 99:
                self.amount = 1
            elif i >= self.current_sum:
                possible_amounts.remove(i)
        self.register(self.winning_amount - random.choice(possible_amounts))

    def avoid_dream_number(self):
        possible_amounts = list(range(self.dream_number - 10, self.dream_number))
        if self.current_sum in possible_amounts:
            possible_amounts.remove(self.current_sum)
            self.register(random.choice(possible_amounts))
        if self.current_sum == 88 or self.current_sum == self.dream_number:
            self.register(randrange(2, 9))
        else:
            amount_to_dream = self.dream_number - self.current_sum
            non_dream_amount = randrange(1, amount_to_dream)
            self.register(non_dream_amount)

    def prepare_loss(self):
        for i in range(self.current_sum + 1, self.current_sum + 11):
            if self.consecutive_ints(int(str(i)[0]), int(str(i)[1])):
                continue
            else:
                self.register(i - self.current_sum)
                break
        else:
            self.register(1)

    def sadly_win(self):
        print("Im a proud loser bot, but I must sadly win...")
        self.amount = 1
