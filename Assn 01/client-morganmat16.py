# Assignment 01
# File:     client-morganmat16.py
# Author:   Matthew Morgan
# Date:     21 January 2018

# Import statements
import socket

# Message constants
MSG_EXIT = "Exiting now!"
MSG_CL_DIS = "Disconnecting"

# Host and port used for connecting to the server
connect_host, connect_port = socket.gethostbyname('localhost'), 11111

def receiveData(cSocket):
    # Declare message and feedback storage variables
    msg, msgReturned, feedback = None, None, None

    # Continue to send messages and get new messages from the user until "stop" has been found
    while True:
        msg = input("CLIENT: Write a message to send the server > ")
        if msg == "stop": break
        cSocket.sendall(msg.encode())

        # Print the message received back
        msgReturned = cSocket.recv(1024).decode().rstrip('\n')
        if msgReturned: print("  Message: ", msgReturned)

        # Attempt to receive feedback and print the feedback
        try:
            feedback = cSocket.recv(1024).decode().rstrip('\n')
            if feedback:
                print("  Feedback:", feedback)
                if feedback == MSG_EXIT: break
        except socket.timeout:
            print("  No feedback...")

    # Send disconnection msg to the server since no more messages are being sent
    print("CLIENT: Disconnecting from server...")
    cSocket.sendall(MSG_CL_DIS.encode())

def __main__():
    # Generates the socket and connects to the server
    try:
        cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cSocket.settimeout(5)
        cSocket.connect((connect_host, connect_port))

        # Attempt sending of messages to the server unless an error occurs
        try: receiveData(cSocket)
        except ConnectionResetError:
            print("CLIENT: Connection was forcibly closed; terminating program")

        # Close the socket
        cSocket.close()
    except ConnectionError:
        print("CLIENT: Something went wrong; is the server on?")

    exit(0)

__main__()
