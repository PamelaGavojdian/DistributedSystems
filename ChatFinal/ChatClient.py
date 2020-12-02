#Pamela Gavojdian

import getopt,threading, sys, socket, os, time

def getArguments():
    HPort = None
    connectPort = None
    options, arguments = getopt.getopt(sys.argv[1:], "l:p:s:")
    for opt in options:
        if opt[0] == '-l':
            HPort = int(opt[1])
        if opt[0] == '-p':
            connectPort = int(opt[1])
    return HPort, connectPort

class ChatClient:

#FORMAT FOR GRETTING, FILE INFORMATION AND FILE REQUEST
    GREETING_FORMAT = "('{}',{})"                   
    FILE_INFORMATION_FORMAT = "!i('{}','{}',{})"      
    FILE_REQUEST_FORMAT = "!r('{}','{}')"             


    def __init__(self, host, connect, debug):
        self.HPort = host
        self.debug = debug
        self.messageSocket = None
        self.connectPort = connect
        self.fileSocket = None
        self.fileQueue = []
        self.receiveInfo = None
        

    def MESSAGECHAT(self):
        fileSender = threading.Thread(target=self.sendFile, daemon=True)
        fileReceiver = threading.Thread(target=self.receiveFile, daemon=True)
        messageReceiver = threading.Thread(target=self.receiveMessage, daemon=True)

        #start the file sender, file and message reciever
        fileSender.start()
        fileReceiver.start()
        messageReceiver.start()


        # prompts the user to enter a value then returns the value the user entered 
        print("Enter an option ('m', 'f', 'x'):\n (M)essage (send)\n (F)ile (request)\ne(X)it")
        usrinput = sys.stdin.readline()
        while usrinput:
            usrinput = usrinput[:-1]

            if usrinput == 'm':
                print('Enter your message:')
                message = sys.stdin.readline()
                message = '!m' + message 
                self.messageSocket.send(message.encode())


            elif usrinput == 'f':
                print("Who owns the file?")
                owner = sys.stdin.readline()
                print('Which file do you want?')
                filename = sys.stdin.readline()
                message = ChatClient.FILE_REQUEST_FORMAT.format(owner.strip(), filename.strip())
                self.messageSocket.send(message.encode())



            elif usrinput == 'x':
                self.console("Self Terminating", "important")
                self.messageSocket.shutdown(socket.SHUT_RDWR)
                self.messageSocket.close()
                self.fileSocket.shutdown(socket.SHUT_RDWR)
                self.fileSocket.close()
                print("closing your sockets...goodbye")
                sys.exit()


            print("Enter an option ('m', 'f', 'x'):\n (M)essage (send)\n (F)ile (request)\ne(X)it" )
            usrinput = sys.stdin.readline()

       
        self.messageSocket.shutdown(socket.SHUT_RDWR)
        self.messageSocket.close()
        self.fileSocket.shutdown(socket.SHUT_RDWR)
        self.fileSocket.close()
        

    def connect(self):
        
        self.messageSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.messageSocket.connect(('localhost', self.connectPort))

        

        listener = threading.Thread(target=self.getFileSocket, args=(self.HPort,))
        listener.start()

        

        fname = sys.stdin.readline().strip()  
        greeting = ChatClient.GREETING_FORMAT.format(fname, self.HPort)
        self.messageSocket.send(greeting.encode())

        
        listener.join()

        

    def console(self, message, messageType=None):
        if self.debug:

            print(message+'\033[0m')

    def findFile(self, filename, requester):
        try:
            stats = os.stat(filename)
            if stats.st_size:
                self.console("Found {} with {} bytes, sending to {}".format(filename, stats.st_size, requester), "file")
                self.fileQueue.append((filename, requester, stats.st_size))
        except OSError:
            pass

    def getFileSocket(self, HPort):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  

        # Bind to the port 
        listener.bind(('', HPort))  

        # listen for connections 
        listener.listen(10)  
        fileSocket, address = listener.accept()
        listener.close()
        self.fileSocket = fileSocket

    def sendFile(self):
        while True:
            q = list(self.fileQueue)
            for f in q:
                #file size
                fsize = f[2]

                #file name
                fname = f[0]
                recipient = f[1]

                self.messageSocket.send(ChatClient.FILE_INFORMATION_FORMAT.format(recipient, fname, fsize).encode())
                time.sleep(.1)
                file = open(fname, 'rb')
                data = file.read(1024)
                while data:
                    self.fileSocket.send(data)
                    data = file.read(1024)
                #close the file 
                file.close() 
                self.fileQueue.remove(f)
            time.sleep(.1)

    def receiveFile(self):
        fileData = self.fileSocket.recv(1024)
        while fileData:
            self.console("Receiving {}".format(self.receiveInfo[0]), 'file')
            dataReceived = len(fileData)
            if self.debug:
                file = open(self.receiveInfo[0], 'wb')
            else:
                file = open(self.receiveInfo[0], 'wb')
            file.write(fileData)
            while dataReceived < self.receiveInfo[1]:
                fileData = self.fileSocket.recv(1024)
                file.write(fileData)  
                dataReceived += len(fileData)

            #close the file
            file.close()  
            self.receiveInfo = None
        
            fileData = self.fileSocket.recv(1024)

    def receiveMessage(self):
        try:
            message = self.messageSocket.recv(1024)
            while message:
                message = message.decode()

                # parse and get the data 
                prefix = message[:2]  
                message = message[2:]  

                if prefix == '!m':  
                    print(message)

                elif prefix == '!r':  
                    message = eval(message)
                    requester = message[0]
                    filename = message[1]
                    
                    finder = threading.Thread(target=self.findFile, args=(filename,requester), daemon=True)
                    finder.start()

                elif prefix == '!i':  
                    message = eval(message)
                    filename = message[0]
                    fsize = int(message[1])
                   
                    self.receiveInfo = (filename, fsize)
                message = self.messageSocket.recv(1024)
        except OSError:
            pass
        os._exit(0)

if __name__ == '__main__':
    h, c = getArguments()
    cl = ChatClient(h, c, True)
    cl.connect()
    cl.MESSAGECHAT()
    
