import re
import socket
import multiprocessing
# import dynamic.mini_frame
import sys

class WSGIserver(object):
    def __init__(self,port,frame,app):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.bind(('',int( port)))
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_socket.listen(128)
        self.frame=frame
        self.app=app
    def server(self, new_socket):
        request = new_socket.recv(1024)
        request_decode = request.decode()
        if request_decode:
            # print(request_decode.splitlines())
            res = re.match(r'[^/]+/([^ ]*) ', request_decode.splitlines()[0])
            file_name = res.group(1)
            if file_name == '':
                file_name = 'index.html'
            # print(file_name)
            if not file_name.endswith('.py'):
                content='static request'
                new_socket.send('HTTP/1.1 200 OK\r\n\r\n'.encode())
                new_socket.send(content.encode())
            else:
                # head = 'HTTP/1.1 200 OK\r\n\r\n'
                env={}
                env['file_name']=file_name
                body =self.app(env,self.set_header)
                header='HTTP/1.1 '+self.status
                for temp in self.header:
                    header+='{}:{}\r\n'.format(temp[0],temp[1])
                header+='\r\n'
                response = header + body
                new_socket.send(response.encode())

        new_socket.close()
    def set_header(self,status,headers):
        self.status=status
        self.header=headers

    def run(self):

        while True:
            print('waiting...')
            new_socket, addr = self.tcp_socket.accept()
            t = multiprocessing.Process(target=self.server, args=(new_socket,))
            t.start()
            new_socket.close()


def main():

    if len(sys.argv)==4:
        port=sys.argv[1]
        framename=sys.argv[2]
        appname=sys.argv[3]
        sys.path.append('./dynamic')
        # print(sys.path)
        frame=__import__(framename)
        app=getattr(frame,appname)
        wsgi_server = WSGIserver(port,frame,app)
        wsgi_server.run()


if __name__ == '__main__':
    main()
