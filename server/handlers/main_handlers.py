# -*- coding: utf-8 -*-
from sqlalchemy.testing import db
from tornado.web import RequestHandler,Application,url
import tornado.ioloop
import tornado.web
from handlers.send_msg import *
from models.orm import *
class MyFormHandler(tornado.web.RequestHandler):

        def get(self):
                self.write('<html><body><form action="/install" method="POST">'
                   #  '<input type="text" name="message">'
                     '<input type="submit" value="安装软件">'
                     '</form></body></html>')



        def post(self):
            self.orm = ORMManager()  # 创建一个ORM对象
            self.set_header("Content-Type", "text/plain")
            ipaddr=self.request.remote_ip
            #print(ipaddr)
            msg = sendMsg(ipaddr,'getinfo')

            filename,md5,sha1,username = msg.split(' ', 4);

            print(filename)
            print(md5)
            print(sha1)
            print(username)
            print(msg)
            user_dep = self.orm.GetUserByName(username).dep
            soft_info = self.orm.GetSoftByMd5(md5)
            print(user_dep)
            print(soft_info)
            self.write("You wrote " +msg)
            #msg =sendMsg(ipaddr, 'install')
            #print(msg)

