# ECU-3010

## Assignment 02
### Assignment Description
This assignment is another take on the first assignment; however, instead of using a predefined client or nc to communicate with the server, a web browser is used. This is done by accessing localhost via the browser, and making page requests. 
### Source Files
Source Files: web-server-morganmat16.py

Data Files: can-meme.png, download.html, download.zip, index.html, info.html, page1.html
### Compilation, Testing, and Known Issues
```
Testing: python3 web-server-morganmat16.py
```
Issues:
- Accessing the server via Firefox, and going to `localhost:11111` results in a lot of “favicon.ico” requests. Firefox has also been found to send background requests, which the server does take notice of. (You’ll see this in the output of the console if/when it occurs.)
- According to my information, the server attempts to send the download.zip file even if the user doesn’t press the ‘accept’ button for downloading.

Notes:
- The assignment only required that a couple of HTML documents and a ZIP download be available; however, to thoroughly test the server’s capabilities, I also utilized an image and a text file.
- The page `localhost:11111` will display an index page with a list of commands. These commands are also on display in the console on startup.
- A couple of commands don’t have files that correspond to their detection – `echo` and `exit`. The file is hard-coded to send HTML to the browser when these commands are detected.
