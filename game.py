from player import Player
from dice import Dice
from random import randint


class GipGame:
    def __init__(self):  # init the game with required variables

        self.players = [Player(), Player()]  # list of players
        self.dice = Dice()  # create a dice object
        self.round_score = 0  # declaring round score variable

    def reset(self):
        """
        Recreates all the players in the game,
        resets the rounds score and requests
        names for the new players
        """
        for player in range(len(self.players)):  # loop through the players
            self.players[player] = Player()  # re create the players
            self.players[player].set_name(input(f"Player {player+1} name \n: ").capitalize())
            
        self.reset_round_score()

    def play_again(self):
        """
        resets the scores of every player
        and the rounds score
        """
        for player in range(len(self.players)):  # loop through the players
            self.players[player].reset_score()  # set the players score to 0

        self.reset_round_score()

    def is_winner(self):
        """
        loops through all the players
        and checks for a winner
        """
        for player in self.players:  # loop through the players
            if player.get_score() >= 100:  # check if the player has won
                return True
        return False

    def reset_round_score(self):
        """
        this is to reset the rounds score to 0,
        this is just to reduce magic numbers.
        """
        self.round_score = 0

    def is_bust(self, dice_value):
        """
        check if the player rolled a 1
        """
        if dice_value == 1:
            return True
        else:
            return False

    def roll_again_request(self):
        """
        Ask if the player wants to roll again
        checks for input string of "y" or "n"
        returns bool to indicate
        """
        player_input = ""
        while player_input not in ["y", "n"]:  # list of legal characters
            player_input = input("Roll Again Y/N\n: ").lower()  # request input

        return True if player_input == "y" else False  # return true if the player wants to roll again

    def player_roll(self):
        """
        this function handles rolling the dice for the player
        first assigns a roll to a variable
        checks for bust return False
        else appends variable for roll to round score return True
        """
        dice_value = self.dice.roll()
        print(f"you rolled a {dice_value}")
        if self.is_bust(dice_value):
            print("You hit a 1 unlucky round score 0")
            self.reset_round_score()
            return False
        else:
            self.round_score += dice_value
            print(f"now your score for this round is {self.round_score}")
            return True

    def play_round(self):
        """
        handles the basic flow of each round
        and returns the score for that round
        """
        if self.player_roll():
            while True:
                if self.roll_again_request():
                    if self.player_roll():
                        continue
                    else:
                        return self.round_score
                else:
                    return self.round_score
        else:
            return self.round_score

    def main_loop(self):
        self.reset()
        player_turn = randint(0, 1)
        current_player = self.players[player_turn]

        while not self.is_winner():
            player_turn = abs(player_turn - 1)
            current_player = self.players[player_turn]
            print(f"______________{current_player.get_name()}'s Turn______________")
            self.players[player_turn].add_score(self.play_round())
            self.reset_round_score()
            print(f"______________{current_player.get_name()}'s Score is {current_player.get_score()}")


game = GipGame()
game.main_loop()
