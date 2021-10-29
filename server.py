from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
from time import sleep

# this is a global variable to hold all the clients.
global clients
clients = {}


class ClientChannel(Channel):
    """
    This class listens to data sent to the server.
    """

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

                # if i is not equal to the id of the sender client.
                if (i + 1) != data["ID"]:
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

    def Connected(self, channel, addr):
        """
        When a client connects to the server
        this method is called.
        """
        global clients

        # add the new client to the global variable.
        clients[len(clients) + 1] = channel

        # set the id of the new client to its position in the dictionary.
        print("new connection:", channel)
        channel.Send({"action": "setID", "value": (len(clients))})

        # tell the first client to wait.
        if len(clients) == 1:
            clients[1].Send({"action": "print", "sender": "Server", "message": "Waiting for a friend..."})

        # if a third client tries to connect tell them the server is full.
        elif len(clients) > 2:
            clients[3].Send({"action": "print", "sender": "Server", "message": "-----Server Full-----"})
            clients[3].Send({})
            clients.pop(3)

        # when a second client joins notify the first.
        if len(clients) == 2:
            clients[1].Send({"action": "print", "sender": "Server", "message": "-----Friend connected-----"})


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
