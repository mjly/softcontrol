# -*- coding: utf-8 -*-
"""
Created on Thu May 10 15:02:59 2018

@author: MERLIN.MA
"""
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.iostream import IOStream, StreamClosedError
from tornado.tcpclient import TCPClient
from tornado.tcpserver import TCPServer
from tornado.platform.asyncio import to_tornado_future, to_asyncio_future
import file_data
import sub_process


class MyServer(TCPServer):

    async def handle_stream(self, stream, address):
        while True:
            try:
                encoded = "*".encode()
                msg = await stream.read_until(encoded)
                msg = msg.decode('utf-8')
                print(msg)
                path =None
                if msg:
                    print(msg)


                    print(msg)
                    if msg == 'getinfo*':
                        try :
                             print('date=', msg)
                             path, md5, sha1 = file_data.getData()
                             msg = msg + ' ' + path + ' ' + md5 + ' ' + sha1 + ' ' + '*'
                             await stream.write(msg.encode())
                        except IOError:
                            break


                    if msg == 'install*':
                        sub_process.install(path)


                else:
                    break

            except StreamClosedError:
                print("connection error")
                break


server = MyServer()
server.listen(8000)
IOLoop.current().start()
