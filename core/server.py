#!/user/bin/python3

import SocketServer
import Json
import display

__BUFF_SIZE = 1024 

class Tcp(SocketServer.BaseRequestHandler):

    def handler(self):
        self.blob = self.request.recv(server_.__BUFF_SIZE)
        print("Incoming connection from {}".format(self.client_address[0]))
        print("Tcp data : {} ".format(self.blob))

        data = json.load(self.data)
        d = display.Display(data)
        #TODO
        #d.run()



    def run(host, port):
        if host == None or port < 0x0 or or > 0xFFFFF:
            raise ValueError("Invalid parammeters")

        server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
        server.serve_forever()



