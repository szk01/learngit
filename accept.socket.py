import socket

def log(*args, **kwargs):
    print(*args, **kwargs)


def RecHttp(response):
    ip = '106.15.44.224'         #局域网IP,路由器分配给电脑的，在cmd可以查询
    port = 80
    client = socket.socket()
    address = (ip, port)
    client.bind(address)

    while True:
        client.listen(5)
        log('connect waiting...')
        connection, address = client.accept()
        request = connection.recv(1024)
        log('connect sucessed...')
        log('ip and request, {}\n{}'.format(address, request.decode('utf-8')))
        #返回响应
        connection.sendall(response)
        connection.close()


if __name__ == '__main__':
    response = 'hello world!'
    RecHttp(response)