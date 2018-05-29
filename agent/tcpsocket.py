from tornado import gen
from tornado.ioloop import IOLoop
from tornado.iostream import IOStream, StreamClosedError
from tornado.tcpclient import TCPClient
from tornado.tcpserver import TCPServer
from tornado.platform.asyncio import to_tornado_future, to_asyncio_future


class MyServer(TCPServer):

    async def handle_stream(self, stream, address):
        while True:
            try:
                encoded = "*".encode()
                msg = await stream.read_until(encoded)
                print(msg)

                if stream:
                    msg1 = "wolo*"
                    await stream.write(msg1.encode())

            except StreamClosedError:
                print("connection error")
                break

server = MyServer()
server.listen(8000)
IOLoop.current().start()