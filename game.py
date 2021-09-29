from player import Player

class GipGame:
    def __init__(self): # init the game with required variables
        self.player1 = Player() # create player 1
        self.player2 = Player() # create player 2
        self.players = [self.player1, self.player2] # list of players
        self.round_score = 0 # set score to 0

    def reset(self):
        for player in self.players:
            player = Player()
        """self.player1 = Player()
        self.player2 = Player()"""
        self.round_score = 0 # set round score to 0

    def play_again(self):
        for player in self.players:
            player.reset_score()
        """self.player1.reset_score() # reset player score
        self.player2.reset_score() # reset player score"""

    def update_round_score(self, dice_roll):
        if dice_roll == 1:
            self.round_score = 0
            return False
        else:
            self.round_score += dice_roll
            return True

    def is_winner(self):
        if self.player1.score >= 100 or self.player2.score >= 100:
            return True
        else:
            return False
