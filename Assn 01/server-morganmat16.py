# Assignment 01
# File:     server-morganmat16.py
# Author:   Matthew Morgan
# Date:     21 January 2018

# Special notes:
# This server is programmed to work in cooperation with its client,
# but also works as a standalone. It will shut down when either
# a number of predefined clients connects and disconnects, or the
# 'nc' command sends it an exit signal (infinite messages permitted
# in this case). A client can also force the server to shut down
# via sending the exit signal.

# Import statements
import socket

# Message constants
MSG_ECHO = "Echo found!\n"
MSG_EXIT = "Exiting now!\n"
MSG_CL_DIS = "Client disconnected...\n"

# Return constants for receiveData
CL_DISC, CL_EXIT, CL_NORM, CL_SPEC = 0, 1, 2, 3

# Host and port to launch the server on
global connect_left, connect_host, connect_port

def dataTest(data):
    # Return the message constant corresponding to the keyword found, or
    # None if there is no special message to send
    if "disconnecting" in data: return MSG_CL_DIS
    if "echo" in data: return MSG_ECHO
    if "exit" in data: return MSG_EXIT
    return None

def receiveData(cl):
    data = cl.recv(1024).decode()
    if data:
        # Print received data and bounce it back to the client
        print("  Received data: " + data.rstrip('\n'))
        cl.sendall(data.encode())

        # Get the special message to be shown, if any, and print it
        msg = dataTest(data.lower())
        if not msg == None:
            print("    " + msg.rstrip('\n'))
            if not msg == MSG_CL_DIS: cl.sendall(msg.encode())

        # Return the appropriate constant regarding connection status
        if msg == MSG_CL_DIS: return CL_DISC
        elif msg == MSG_EXIT: return CL_EXIT
        else: return CL_NORM
    else:
        # Special case code: Client disconnects before sending data
        # This case catches the usage of 'nc' in Linux
        print("  ERR: No more data received. Disconnect assumed.")
        return CL_SPEC

def acceptConnection(sSocket):
    # The client, their address, and status of connection
    cl, clAddr = sSocket.accept()
    cl_connected = CL_NORM

    # Continue receiving messages while the client is connected
    with cl:
        print("SERVER: Connection from", clAddr)
        while cl_connected == CL_NORM: cl_connected = receiveData(cl)
    
    # Return the result of the message received from client
    return cl_connected

def __main__():
    # connect_host, connect_port, connect_left = socket.gethostbyname('localhost'), 11111, 5
    connect_host, connect_port, connect_left = '', 11111, 5

    # Generates the socket, binds it, and begins listening on the host and port
    sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sSocket.bind((connect_host, connect_port))
    sSocket.listen(connect_left)

    # Print where the server is listening and accept a connection if one becomes available
    print("SERVER: Listening on address '"+connect_host+":"+str(connect_port)+"'...")

    # Accept connections until no more are allowed. If the special
    # recipient case is met, no modification happens to the number
    # of connections; however, if the client disconnects or sends
    # the exit signal, the number is modified
    while connect_left > 0:
        connectionResult = acceptConnection(sSocket)
        if connectionResult == CL_EXIT: connect_left = 0
        elif connectionResult == CL_DISC: connect_left -= 1

    # Shut down server
    print("SERVER: Closing down server...")
    sSocket.close()
    exit(0)

__main__()
