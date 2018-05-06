# ECU-3010

## Assignment 01
### Assignment Description
The first programming assignment was about creating a simple client and server that could communicate with one another via text messages. A few keywords – stop, exit, and echo – were to be recognized, and if one (exempting stop) detected in a client’s message, a message sent back. Timeouts were critical to the operation of the assignment to prevent infinite looping of message retrieval by the client.
### Source Files
client-morganmat16.py, server-morganmat16.py
### Compilation, Testing, and Known Issues
```
Testing:
python3 server-morganmat16.py
python3 client-morganmat16.py
```
Notes:
- The server must be started before the client for the assignment to work properly.
- Due to the testing method of the instructor, the server works in conjunction with the client, but also has capabilities to infinitely run until ‘nc’ (on Linux) is used to send an exit signal.
- The server receives a message and detects if `exit` or `echo` is in the message. Only the client checks for `stop`, which terminates the connection to the server.
