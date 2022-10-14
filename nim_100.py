from nim_bots import WinnerBot, LoserBot

####
#   Representation of an alternative nim-style game, so called 'nim 100'
#   https://en.wikipedia.org/wiki/Nim
####

rules = """
===================================

Welcome to Nim_100

whereby the rules are as follows...
    - two players take turns to add (no other actions possible) an integer between 1-10 to a sum (which starts at 0)
    - the sum will increase by the amount the last player has added to the sum
    - the player who gets the sum to 100 is the winner, and the game ends
    - you can play against a bot who will try to win or lose on purpose

===================================
"""

class Sum:
    """
    Object representing the sum the players are adding to.
    """
    def __init__(self):
        self.total_sum = 0
        self.target_sum = 100

    def check_sum_over_target(self, sum):
        """

        :param sum: the current value of sum
        :type sum: int
        :return: if sum is more than the value of self.target_sum
        :rtype: bool
        """
        return True if sum > self.target_sum else False

    def display_total(self):
        print(f"Current total is: {self.total_sum}/{self.target_sum}")


class Player:
    """
    Object representing a player, who will add a number to the sum
    """

    def __init__(self):
        self.amount = 0
        self.name = input("Welcome Player -  Whats your name? (or enter bot for a bot player): ")
        if self.name == "bot":
            self.bot_player = True
            self.win_or_lose = input("Do you want this bot to try to win/lose against the other player? (win|lose): ")

    def give_sum(self, _sum=None):
        """
        Player gives an amount to the sum.
            - Checks if the amount is valid
                - if yes -> registers the amount to a self attr.
                - if no -> user must try again
        :return:  None
        """
        _ = _sum
        while True:
            amount = int(input(f"{self.name}, give me an integer between 1 - 10 to add to sum: "))
            if self.is_valid(amount):
                self.register(amount)
                break
            else:
                print(f"Nah {self.name}, you have to give me an integer between 1 - 10")

    @staticmethod
    def is_valid(amount):
        """
        :return: if  amount is an integer between 1 and 10
        :rtype: bool
        """
        is_int = type(amount) is int
        is_in_range = 0 < amount < 11
        return True if all([is_int, is_in_range]) else False

    def register(self, amount):
        """registers the amount to a self attr"""
        self.amount = amount

    def try_again(self):
        """Prompts the user to try again (their given amount took the sum over 100)"""
        print(f"Nah, {self.name}, your addition to the total sum took you over 100, try again.")


class Game:
    """
    Object representing the game being played
    """
    def __init__(self, sum_obj: Sum, players: list[Player]):
        self.sum_obj = sum_obj
        self.players = players
        self.game_over = False
        for player in self.players:
            if hasattr(player, 'bot_player'):
                player_index = players.index(player)
                players[player_index] = WinnerBot() if player.win_or_lose == "win" else LoserBot()
            continue
        self.current_player = self.players[0]

    def add_players_sum_to_total_sum(self):
        self.sum_obj.total_sum += self.current_player.amount

    def check_if_winner(self):
        while True:
            if not self.sum_obj.check_sum_over_target(self.sum_obj.total_sum):
                break
            self.current_player.try_again()

        if self.sum_obj.total_sum == self.sum_obj.target_sum:
            print(f"{self.current_player} is the winner.")
            self.end_game()

    def next_player(self):
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]

    @staticmethod
    def end_game():
        print("Game Over")
        exit(0)


def introduce_game_rules():
    print(rules)


def init_game():
    s = Sum()
    p1 = Player()
    p2 = Player()
    return Game(s, [p1, p2])


def main():
    introduce_game_rules()
    game_instance = init_game()

    while True:
        current_sum = game_instance.sum_obj.total_sum
        game_instance.current_player.give_sum(current_sum)
        game_instance.add_players_sum_to_total_sum()
        game_instance.check_if_winner()
        game_instance.sum_obj.display_total()
        game_instance.next_player()


if __name__ == '__main__':
    main()
