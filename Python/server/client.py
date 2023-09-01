import socket

class BaseClient:
    def __init__(self,timeout=10,buffer=1024):
        self.__socket = None
        self.__address = None
        self.__timeout = timeout
        self.__buffer = buffer

    def connect(self,address,family:int,typ:int,proto:int):
        self.__address = address
        self.__socket = socket.socket(family,typ,proto)
        self.__socket.settimeout(self.__timeout)
        self.__socket.connect(self.__address)

    def send(self,message:str=""):
        flag = False
        while True:
            if message =="":
                message_send = input(">")
            else:
                message_send = message
                flag = True
            self.__socket.send(message_send.encode('utf-8'))
            message_recv = self.__socket.recv(self.__buffer).decode('utf-8')
            self.received(message_recv)

            if flag:
                break
        try:
            self.__socket.shutdown(socket.SHUT_RDWR)
            self.__socket.close()
        except:
            pass

    def received(self,message:str):
        print(message)

class InetClient(BaseClient):
    def __init__(self,host="127.0.0.1",port=8080):
        self.server=(host,port)
        super().__init__(timeout=60,buffer=1024)
        super().connect(self.server,socket.AF_INET,socket.SOCK_STREAM,0)

if __name__ == "__main__":
    cli = InetClient()
    cli.send()
