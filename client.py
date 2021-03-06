from time import sleep
from PodSixNet.Channel import Channel
from PodSixNet.Connection import ConnectionListener, connection


class MyNetworkListener(ConnectionListener):
    # the id of this client
    id = 0

    # a boolean that tells this client if it
    # is this clients turn.
    turn = True


    def __init__(self):
        """
        when there is a new isntance of this class,
        connect to the server and update the server
        data.
        """
        self.Conn()
        self.Update()


    def Update(self):
        """
        This function updates the data from the server.
        """
        connection.Pump()
        self.Pump()


    def Network_serverFull(self, data):
        """
        If the server is full, end this client.
        """
        i = 10
        print("Quiting", end="")

        while i > 0:
            print(".", end="")
            i -= 1
            sleep(0.05)

        quit()


    def Network_getInput(self, data):
        """
        This function retrieves info from the user and
        sends it to the server.
        """

        playerInput = ""

        if data["type"] == "y/n":

            while playerInput not in ["y", "n"]:
                playerInput = (input("Roll Again? Y/N\n: ")).lower()


        elif data["type"] == "name":

            playerInput = input("Username?\n: ")


        elif data["type"] == "replay":

            while playerInput not in ["y", "n"]:
                playerInput = (input("Play Again? Y/N\n: ")).lower()


        connection.Send({"action": "retrieveInput", "playerInput": f"{playerInput}"})


    def Network_print(self, data):
        """
        When this function is called by the server.
        print a message.
        """
        
        print(f"{data['message']}")


    def Network_setID(self, data):
        """
        This function allows the server to control
        this clients id. and if it is the first client
        it is not this clients turn to speak.
        """
        self.id = data["value"]
        if data["value"] == 1:
            self.turn = False


    def Conn(self):
        """
        Request a server address and connect to the server
        if no address is given, default to LocalHost:8000
        """

        # while the address doesnt work.
        while True:

            # get a server address from the user.
            address = input("Address of Server: ")

            # if the address is empty.
            # default the host to localhost 
            # and the port to 8000.
            if not address:
                host, port = "localhost", 8000

                # otherwise split the input into
                # a host and a port.
            else:
                host, port = address.split(":")

            # try to connect to the server.
            try:
                self.Connect((host, int(port)))
                # when the client connects print a message.
                print(f"Client Joined {host}:{port}")
                break

            # print an error.
            except:
                print("Error Connecting to Server")


# create an instance of the server.
myClient = MyNetworkListener()

while True:
    # while the clients id is still default.
    # or if it is not this clients turn.
    # update the server data and wait.
        myClient.Update()
        sleep(0.1)