
#PAMELA GAVOJDIAN
#FINAL

import sys,socket,threading,time



class ChatServer:

    #FORMAT FOR MESSAGE, FILE REQUEST AND FILE SEND 
    MESSAGE_FORMAT = "!m{}: {}"                 
    FILE_REQUEST_FORMAT = "!r('{}','{}')"       
    FILE_SEND_FORMAT = "!i('{}',{})"            
 

    def __init__(self, port, debug=False):
        self.debug = debug
        self.port = port
        self.clients = {} 
        self.listeningSocket = None                 
        self.incomingFiles = {}             
        self.Sendout = {}                    

    def receiveMessage(self, messageSocket, clientName, port, address='localhost'):

        # First Message Will be Client's Name and Their File Port Number

        fileSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fileSocket.connect((address[0], port))
        self.clients[clientName] = (messageSocket, fileSocket)
        self.incomingFiles[clientName] = None
        

        #print(fileSocket)
        fileForward = threading.Thread(target=self.forwardFile, args=(fileSocket,clientName), daemon=True)
        fileForward.start()
        
        time.sleep(.5)

        # Receive Messages
        message = messageSocket.recv(1024)  

        #while loop to check and see if there are people chatting 
        while message:  

            message = message.decode()
            prefix = message[:2]
            message = message[2:]

            if prefix == '!m':
                self.console("{} sent {}".format(clientName, message).strip(), 'message')
                outMessage = ChatServer.MESSAGE_FORMAT.format(clientName, message.strip()) 

                # for liip that looks at (client1, client2, and client3) 
                for fname in self.clients.keys():  
                    if fname != clientName: 
                        self.clients[fname][0].send(outMessage.encode())  


            elif prefix == '!i':
                if self.incomingFiles[clientName] is None:
                    message = eval(message)                 
                    person = message[0]
                    filename = message[1]
                    fsize = int(message[2])
                   
                    self.incomingFiles[clientName] = (person, filename, fsize)
                    outMessage = ChatServer.FILE_SEND_FORMAT.format(filename, fsize)
                    self.clients[person][0].send(outMessage.encode())


            elif prefix == '!r':
                message = eval(message)
                owner = message[0]
                if owner in self.clients.keys():
                    filename = message[1]
                    
                    outMessage = ChatServer.FILE_REQUEST_FORMAT.format(clientName, filename)
                    self.clients[owner][0].send(outMessage.encode())


                    
                else:
                    self.console("Multiple Incoming Files From {}, cannot Handle!".format(clientName), "important")
            
            #looks for the next message and gets it 
            message = messageSocket.recv(1024)  
        try:
            
            messageSocket.shutdown(socket.SHUT_RDWR)
            fileSocket.shutdown(socket.SHUT_RDWR)
        except OSError:  
            pass

        #close the messange and file sockets 
        messageSocket.close()
        fileSocket.close()

    def forwardFile(self, fileSocket, clientName):

        #print(fileSocket)
        try:
            fileData = fileSocket.recv(1024)
        except OSError:
            return
        while fileData:
            totalSize = self.incomingFiles[clientName][2] 
            person = self.incomingFiles[clientName][0]           
            clientFileSocket = self.clients[person][1] 

            dataReceived = len(fileData)
            clientFileSocket.send(fileData)

            #while loop that keeps going as long as total size is greater than datarecieved 
            while dataReceived < totalSize:
                fileData = fileSocket.recv(1024)
                clientFileSocket.send(fileData)
                dataReceived += len(fileData)
            self.incomingFiles[clientName] = None
            
            try:
                fileData = fileSocket.recv(1024)
            except OSError:
                return

    def console(self, message, messageType=None):
        if self.debug:

            print(message+'\033[0m')

    def listen(self):
        self.listeningSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.listeningSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        self.listeningSocket.bind(('', self.port))  

        # listening for connection
        self.listeningSocket.listen(10)  
        

        #keep looping while its true 
        while True:
            try:
                messageSocket, address = self.listeningSocket.accept()  
                
                clientInformation = eval(messageSocket.recv(1024).decode())
                clientName = clientInformation[0]
                port = int(clientInformation[1])
                chatter = threading.Thread(target=self.receiveMessage, args=(messageSocket, clientName, port, address), daemon=True)
                chatter.start()
            except KeyboardInterrupt:
                
                for fname in self.clients:
                    try:
                        self.clients[fname][0].shutdown(socket.SHUT_RDWR)
                        self.clients[fname][1].shutdown(socket.SHUT_RDWR)
                        self.clients[fname][0].close()
                        self.clients[fname][1].close()
                    except OSError:
                        pass
                break
        
        #close the listeningSocket and exit 
        self.listeningSocket.close()  
        sys.exit()

if __name__ == '__main__':
    try:
        prt = int(sys.argv[1])  
    except (IndexError, TypeError):  
        #exit the program 
        sys.exit()  
    server = ChatServer(prt, True)
    
    server.listen()


#FORMAT FOR MESSAGE, FILE REQUEST, AND FILE SEND 
MESSAGE_FORMAT = "!m{}: {}"                 
FILE_REQUEST_FORMAT = "!r('{}','{}')"       
FILE_SEND_FORMAT = "!i('{}',{})"            


debug = False;
port = None
clients = {}
incomingFiles = {}
Sendout = {}
listeningSocket = None



def receiveMessage(self, messageSocket, clientName, port, address='localhost'):
    # First Message Will be Client's Name and Their File Port Number
    fileSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fileSocket.connect((address[0], port))
    self.clients[clientName] = (messageSocket, fileSocket)
    self.incomingFiles[clientName] = None
    
    #print(fileSocket)
    fileForward = threading.Thread(target=self.forwardFile, args=(fileSocket,clientName), daemon=True)
    fileForward.start()
    
    time.sleep(.5)

    # Receive Messages

    message = messageSocket.recv(1024)  
    while message:  

        message = message.decode()
        prefix = message[:2]
        message = message[2:]

        if prefix == '!m':
            self.console("{} sent {}".format(clientName, message).strip(), 'message')
            #reformats the message 
            outMessage = ChatServer.MESSAGE_FORMAT.format(clientName, message.strip())  

            
            # loop that keeps going for each of the clients (1,2,3)
            for fname in self.clients.keys(): 
                if fname != clientName:  
                    self.clients[name][0].send(outMessage.encode())  


        elif prefix == '!r':
            message = eval(message)
            owner = message[0]
            if owner in self.clients.keys():
                filename = message[1]
                
                outMessage = ChatServer.FILE_REQUEST_FORMAT.format(clientName, filename)
                self.clients[owner][0].send(outMessage.encode())


        elif prefix == '!i':
            if self.incomingFiles[clientName] is None:
                #evaluate the incoming message 
                message = eval(message)                 
                person = message[0]
                filename = message[1]
                fsize = int(message[2])
                self.console("Incoming File {} from {} for {}".format(filename, clientName, person), 'file')
                self.incomingFiles[clientName] = (person, filename, fsize)
                outMessage = ChatServer.FILE_SEND_FORMAT.format(filename, fsize)
                self.clients[person][0].send(outMessage.encode())
                
            else:
                self.console("Multiple Incoming Files From {}, cannot Handle!".format(clientName), "important")
       
       # go to the next message and get it 
        message = messageSocket.recv(1024)  
    try:
        
        messageSocket.shutdown(socket.SHUT_RDWR)
        fileSocket.shutdown(socket.SHUT_RDWR)
    except OSError:  
        pass

    #CLOSE THE MESSAGESOCKET AND FILESOCKET
    messageSocket.close()
    fileSocket.close()

def forwardFile(self, fileSocket, clientName):
    #print(fileSocket)
    try:
        fileData = fileSocket.recv(1024)
    except OSError:
        return
    while fileData:

        # Size of the file 
        totalSize = self.incomingFiles[clientName][2] 
        # who is thre person getting it       
        person = self.incomingFiles[clientName][0] 
         # where should the file go 
        clientFileSocket = self.clients[person][1]       


        
        dataReceived = len(fileData)
        clientFileSocket.send(fileData)


        #while loop that keeps going as long as totalsize is larger then dataRecieved
        while dataReceived < totalSize:
            fileData = fileSocket.recv(1024)
            clientFileSocket.send(fileData)
            dataReceived += len(fileData)
        self.incomingFiles[clientName] = None
        
        try:
            fileData = fileSocket.recv(1024)
        except OSError:
            return

def console(self, message, messageType=None):
    if self.debug:

        print(message+'\033[0m')

def listen(self):
    self.listeningSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.listeningSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

    #bing the listeningSocket to the Port
    self.listeningSocket.bind(('', self.port))  

    #Listen for any connections 
    self.listeningSocket.listen(10)  
    
    #loop that keeps going as long as true
    while True:
        try:
            messageSocket, address = self.listeningSocket.accept()  
            
            clientInformation = eval(messageSocket.recv(1024).decode())
            clientName = clientInformation[0]
            port = int(clientInformation[1])
            chatter = threading.Thread(target=self.receiveMessage, args=(messageSocket, clientName, port, address), daemon=True)
            chatter.start()
        except KeyboardInterrupt:
            
            for fname in self.clients:
                try:
                    #SHUTDOWN THE SOCKETS 
                    self.clients[fname][0].shutdown(socket.SHUT_RDWR)
                    self.clients[fname][1].shutdown(socket.SHUT_RDWR)

                    #CLOSE THEM 
                    self.clients[fname][0].close()
                    self.clients[fname][1].close()
                except OSError:
                    pass
            break
    
    #close the listener and exit 
    self.listeningSocket.close()  
    sys.exit()

if __name__ == '__main__':
    try:
        prt = int(sys.argv[1])  
    except (IndexError, TypeError):  
        # Exit and end 
        sys.exit()  

    server = ChatServer(prt, True)

    
    server.listen()

    
