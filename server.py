from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
from player import Player
from dice import Dice
from random import randint
from time import sleep

# this is a global variable to hold all the clients.
global clients
clients = {}

global sentInput
sentInput = ""


class ClientChannel(Channel):
    """
    This class listens to data sent to the server.
    """
    #playerInput = ""
    global sentInput

    def Network_retrieveInput(self, data):
        global sentInput
        #self.playerInput = f"{data['playerInput']}"
        sentInput = data['playerInput']

    def Network_sendMessage(self, data):
        self.SendMessage(data)


    def SendMessage(self, data):
        """
        This function allows clients to send
        messages to the server and the other
        clients.
        """

        # if there are more than one client.
        if len(clients) > 1:

            # for every client.
            for i in range(len(clients)):

                # send a message to the client.
                sender = f"Client: {data['ID']}"
                clients[i + 1].Send({"action": "print", "sender": sender, "message": data["message"]})


    def Network(self, data):
        """
        When data is sent to the server from
        a client this method is called.
        """
        print(data)


class MyServer(Server):
    """
    This class is the server itself and holds
    an instace of the listener class.
    """

    channelClass = ClientChannel
    global clients
    global sentInput

    players = [Player(), Player()]  # list of players
    dice = Dice()  # create a dice object
    round_score = 0  # declaring round score variable


    def Connected(self, channel, addr):
        """
        When a client connects to the server
        this method is called.
        """
        global clients

        # add the new client to the global variable.
        channel.Send({"action": "setID", "value": (len(clients))})
        clients[len(clients)] = channel

        # set the id of the new client to its position in the dictionary.
        print("new connection:", channel)

        # tell the first client to wait.
        if len(clients) == 1:
            clients[0].Send({"action": "print", "sender": "Server", "message": "Waiting for a friend..."})

        # if a third client tries to connect tell them the server is full.
        elif len(clients) > 2:
            clients[2].Send({"action": "print", "sender": "Server", "message": "-----Server Full-----"})
            clients[2].Send({"action": "serverFull"})
            clients.pop(2)

        # when a second client joins notify the first.
        if len(clients) == 2:
            clients[0].Send({"action": "print", "sender": "Server", "message": "-----Friend connected-----"})
            self.main_loop()


    def getInput(self, ID, type):
        """
        This function is used to retrieve an input from
        one player while sending a message to the other.
        """

        global sentInput

        clients[ID].Send({"action": "getInput", "type": f"{type}"})

        if type != "name":
            clients[abs(ID - 1)].Send({"action": "print", "message": "Waiting for player to make turn"})

        while sentInput == "":
            self.Pump()
            sleep(0.1)

        playerInputTemp = sentInput
        sentInput = ""
        return playerInputTemp

    def reset(self):
        """
        Recreates all the players in the game,
        resets the rounds score and requests
        names for the new players
        """
        self.players = [Player(), Player()]

        for player in range(len(self.players)):  # loop through the players
            self.players[player] = Player()  #re create the players
            self.players[player].set_name(self.getInput(player, "name"))

            if player:
                while self.players[player].get_name() == self.players[0].get_name():
                    clients[player].Send({"action" : "print", "message" : "-----Name already taken-----"})
                    self.players[player].set_name(self.getInput(player, "name"))

        self.reset_round_score()

    def play_again(self):
        """
        resets the scores of every player
        and the rounds score
        """
        for player in range(len(self.players)):  # loop through the players
            self.players[player].reset_score()  # set the players score to 0

        self.reset_round_score()

        self.main_loop()

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


    def roll_again_request(self, player):
        """
        Ask if the player wants to roll again
        checks for input string of "y" or "n"
        returns bool to indicate
        """
        player_input = ""
        while player_input not in ["y", "n"]:  # list of legal characters
            player_input = self.getInput((self.players.index(player)), "y/n")  # request input

        return True if player_input == "y" else False  # return true if the player wants to roll again


    def player_roll(self, player):
        """
        this function handles rolling the dice for the player
        first assigns a roll to a variable
        checks for bust return False
        else appends variable for roll to round score return True
        """
        dice_value = self.dice.roll()
        playerIndex = self.players.index(player)

        clients[playerIndex].Send({"action": "print", "ID": "server", "message": f"[{player.get_score()}]"})
        clients[playerIndex].Send({"action": "print", "ID": "server", "message": f"you rolled a {dice_value}"})
        clients[abs(playerIndex - 1)].Send({"action": "print", "ID": "server", "message": f"{player.get_name()} rolled a {dice_value}"})
        if self.is_bust(dice_value):
            clients[playerIndex].Send({"action": "print", "ID": "server", "message": "You hit a 1 unlucky round score 0"})
            clients[abs(playerIndex - 1)].Send({"action": "print", "ID": "server", "message": f"{player.get_name()} hit a 1 unlucky round score 0"})
            self.reset_round_score()
            return False
        else:
            self.round_score += dice_value
            clients[playerIndex].Send({"action": "print", "ID": "server", "message": f"now your score for this round is {self.round_score}"})
            clients[abs(playerIndex - 1)].Send({"action": "print", "ID": "server", "message": f"now {player.get_name()}'s score for this round is {self.round_score}"})
            return True

    def play_round(self, player):
        """
        handles the basic flow of each round
        and returns the score for that round
        """
        if self.player_roll(player):
            while True:
                if self.roll_again_request(player):
                    if self.player_roll(player):
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
        print(player_turn)
        current_player = self.players[player_turn]
        player_input = ""

        while not self.is_winner():
            player_turn = abs(player_turn - 1)
            current_player = self.players[player_turn]
            clients[0].Send({"action": "print", "ID": "server", "message": f"______________{current_player.get_name()}'s Turn______________"})
            clients[1].Send({"action": "print", "ID": "server", "message": f"______________{current_player.get_name()}'s Turn______________"})
            self.players[player_turn].add_score(self.play_round(current_player))
            self.reset_round_score()
            clients[0].Send({"action": "print", "ID": "server", "message": f"______________{current_player.get_name()}'s Score is {current_player.get_score()}"})
            clients[1].Send({"action": "print", "ID": "server", "message": f"______________{current_player.get_name()}'s Score is {current_player.get_score()}"})

        clients[0].Send({"action": "print", "ID": "server", "message": f"THE WINNER IS {current_player.get_name().upper()}!!! WITH A SCORE OF {current_player.get_score()}"})
        clients[1].Send({"action": "print", "ID": "server", "message": f"THE WINNER IS {current_player.get_name().upper()}!!! WITH A SCORE OF {current_player.get_score()}"})
        clients[0].Send({"action": "print", "ID": "server", "message": f"{self.players[abs(player_turn - 1)].get_name()} had a score of {self.players[abs(player_turn - 1)].get_score()}"})
        clients[1].Send({"action": "print", "ID": "server", "message": f"{self.players[abs(player_turn - 1)].get_name()} had a score of {self.players[abs(player_turn - 1)].get_score()}"})


        while player_input not in ["y", "n"]:
            player_input = self.getInput(player_turn, "replay")
        self.play_again() if player_input == "y" else quit()



while True:
    # get an address from the user.
    address = input("Host:Port (localhost:8000): ")

    # if the address is empty.
    if not address:
        # set host to localhost.
        # and set port to 8000.
        host, port = "localhost", 8000

    # otherwise split the given address into a host and port.
    else:
        host, port = address.split(":")

    # try to create the server with the given address.
    try:
        myserver = MyServer(localaddr=(host, int(port)))
        print(f"Server Initiated on {host}:{port}")
        break
    except:
        print("Error creating server")

# while true update the server data.
while True:
    myserver.Pump()
    sleep(0.1)
