# Assignment 02
# File:     web-server-morganmat16.py
# Author:   Matthew Morgan
# Date:     12 February 2018
# Version:  Python 3
# Description:
"""
This server is a continuation of the first assignment's, allowing communication
between the server and a web browser to send data to it via commands specified
in the URL. (These commands are passed via the HTTP header's "GET")

Content-Type List:
https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Complete_list_of_MIME_types
http://www.iana.org/assignments/media-types/media-types.xhtml
"""

"""
Possible issues:
- Jones specified that /download shouldn't download the file.
"""

# Import statements
import socket
import os
import sys

# Command is a class used to represent a single command accepted by the server
# message   :   The message the server displays when the command is recognized
# dataType  :   The type of this command's data
# data      :   The data for this command (such as HTML or a filename)
# fType     :   The type of file (if specified) for streaming files to clients
# fileName  :   The name of the file (usually as stored on-server)
class Command:
    def __init__(self, msg, dType, data, fType='', fName=''):
        self.message = msg
        self.dataType = dType
        self.data = data
        self.fType = fType
        self.fileName = fName
    def getMessage(self): return self.message
    def getData(self): return self.data
    def getTypeData(self): return self.dataType
    def getTypeFile(self): return self.fType
    def getFileName(self): return self.fileName

# SER_CONNECTED is a constant representing a continued connection via client
# SER_DISCONNECTED is a constant representing that a client disconnected
# SER_SHUTDOWN is a constant representing that the server needs to shutdown
SER_CONNECTED, SER_DISCONNECTED, SER_SHUTDOWN = 0, 1, 2

# SERVICES stores all information regarding acceptable commands that can be
# passed to the server
SERVICES = {
	"" : Command("No command specified.", "PAGE", "./files/index.html"),
    "mnm-meme" : Command("File stream: can-meme.png", "FILE", \
        "./files/can-meme.png", "image/png", "can-meme.png"),
    "mnm-text" : Command("File stream: storyofmylife.txt", "FILE", \
        "./files/storyofmylife.txt", "text/plain", "storyofmylife.txt"),
    "echo" : Command("Echo found!"  , "HTML", "<b>Echo</b> found! <i>(Fus-ro-dah!)</i>"),
    "exit" : Command("Exitting now!", "HTML", \
        "The most <b>elite</b> samurai assassinated the server, as per your request, master"),
    "info" : Command("Page request: Info"  , "PAGE", "./files/info.html"),
    "link" : Command("Page request: Link"  , "PAGE", "./files/download.html"),
    "page1" : Command("Page request: page1", "PAGE", "./files/page1.html"),
    "download" : Command("File stream: download.zip", "FILE", \
        "./files/download.zip", "application/zip", "download.zip")
}

# Host and port to launch the server on
connect_host, connect_port = '', 11111

################################################################################
# Parses the desired command/service from the GET request
# cmd: The GET request to parse the command from
# Return: The command, as a string, or "" if no command is given (or empty is)
def parseCommand(cmd):
    # The command is split at spaces, which index 1 is accessed thereafter,
    # with the command being a substring of that index starting from char 1
    # For example: "GET /exit HTTP/1.1" becomes ['GET', '/exit', 'HTTP/1.1']
    # where index 1 is '/exit', and the substring taken is 'exit'
    return cmd.split(" ")[1][1:] if not cmd == None else ""

################################################################################
# Processes a single request based on the command passed, using the client
# connection stored in "cl" to do the processing. Processing is done based on
# the type of the command detected
# cmd: The command to use during processing
# cl: The client socket to send data to during processing
def processRequest(cmd, cl):
    # The header for HTML content, the data to be sent, the filename (if one)
    # and the command's data as stored in the SERVICES dictionary
    header = "HTTP/1.0 200 OK\r\nContent-Length:"
    data, fName = "", None
    cmdData = SERVICES[cmd]

    # If the type of data is HTML, the HTML to send is stored in-program.
    # If the type of data is PAGE, the HTML to send is stored in a file.
    # If the type of data is FILE, data should be sent from a file.
    if cmdData.getTypeData() == "HTML":
        data = "<html><body>"+cmdData.getData()+"</body></html>"
    elif cmdData.getTypeData() == "PAGE" or cmdData.getTypeData() == "FILE":
        fName = cmdData.getData()
    
    # Read in file data if a filename has been detected to need reading. If a
    # file is being read (and not HTML page), the flag 'rb' is used for reading
    if not fName == None:
        flags = 'rb' if cmdData.getTypeData() == "FILE" else 'r'
        with open(fName, flags) as f:
            data = f.read()

    # Finalize header
    header += str(len(data))+";"
    if cmdData.getTypeData() == "FILE":
        header += "\r\nContent-Type: "+cmdData.getTypeFile()+";"+ \
               "\r\nContent-Disposition: attachment;"+ \
               "filename=\""+cmdData.getFileName()+"\";"
    header += "\r\n\n"

    # Send the header and content data in two SEPARATE messages
    cl.sendall(header.encode())
    cl.sendall(data if cmdData.getTypeData() == "FILE" else data.replace('\n','').encode())

################################################################################
# Receives data from a client, decoding it and processing it
# cl: The client receiving the data from
# Return: SER_DISCONNECTED if the client's request was handled, or they
#     disconnected automatically, or SER_SHUTDOWN if "exit" was sent as request
def receiveData(cl):
    # The data that's been received, and the piece of the data we need
    dataFull = cl.recv(1024).decode()

    if dataFull:
        # Split the HTTP header into list entries, parse the command, then
        # print the GET request
        dataFull = dataFull.split('\n')
        cmd = parseCommand(dataFull[0])
        print("  Received data: "+dataFull[0])

        # Get the message to be shown, if the command is valid
        msg = None if not SERVICES.__contains__(cmd) else SERVICES[cmd].getMessage()
        if not msg == None:
            print("    ", msg.rstrip('\n'), sep='')
            processRequest(cmd, cl)
        else:
            print("  ERR: The command '"+cmd+"' is unrecognized!")

        # Return the client was disconnected if the command given was unrecognized
        # OR if the command was not found to be "exit"
        if msg == None: return SER_DISCONNECTED
        elif cmd == "exit": return SER_SHUTDOWN
        else: return SER_DISCONNECTED
    else:
        # No data was received (or Firefox stealth-requested info)
        print("  ERR: No more data received. Disconnect assumed.")
        print("       Did Firefox try stealthily shooting a request?")
        return SER_DISCONNECTED

################################################################################
# Accepts a client connection from the server
# sSocket: The server's socket to accept the connection from
# Return: True if the server should close, or false if it shouldn't
def acceptConnection(sSocket):
    try:
        # The client and the address they connected from
        # The result (should the server close) and client connection status
        cl, clAddr = sSocket.accept()
        res, connected = False, SER_CONNECTED

        with cl:
            print("SERVER: Connection from", clAddr)
            while connected == SER_CONNECTED: connected = receiveData(cl)
            cl.shutdown(socket.SHUT_RDWR)
            cl.close()
        
        res = False if connected == SER_DISCONNECTED else True
        return res
    except ConnectionResetError:
        print("  ERR: Something went wrong with the connection...")
        return False

################################################################################
def __main__():
    global connect_host, connect_port

    # Generates the socket, binds it, and begins listening on the host and port
    sSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sSocket.bind((connect_host, connect_port))
    sSocket.listen(5)

    # Print the host/port where the server is listening and available commands
    print("SERVER: Listening on address '"+connect_host+":"+str(connect_port)+"'...")
    print("SERVER: Available commands:", list(SERVICES.keys()))

    # Accepts connections from clients until an exit command is reached
    endServer = False
    while not endServer: endServer = acceptConnection(sSocket)

    # Shut down server
    print("SERVER: Closing down server...")
    sSocket.close()

__main__()