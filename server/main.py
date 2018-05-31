from handlers.soft_manager import *
from handlers.main_handlers import *
from handlers.user_manager import *
def MainProcess():  # 主过程，程序的入口
    tornado.options.parse_command_line()
    application = tornado.web.Application([  # 这里就是路由表，确定了哪些URL由哪些Handler响应
        url(r'/soft/', SoftMainHandler),  # 路由表中的URL是用正则表达式来过滤的
        url(r'/soft/Addsoft', AddSoftHandler),
        url(r'/soft/EditSoft', EditSoftHandler),
        url(r'/soft/DeleteSoft', DeleteSoftHandler),
        url(r'/soft/UpdateSoftInfo', UpdateSoftInfoHandler),
        url(r'/user/', UserMainHandler),  # 路由表中的URL是用正则表达式来过滤的
        url(r'/user/Adduser', AddUserHandler),
        url(r'/user/EditUser', EditUserHandler),
        url(r'/user/DeleteUser', DeleteUserHandler),
        url(r'/user/UpdateUserInfo', UpdateUserInfoHandler),
        url(r"/install", MyFormHandler)
    ])

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)  # 在上面的的define中指定了端口为9999
    tornado.ioloop.IOLoop.instance().start()  # 启动服务器
if __name__ == "__main__":
    MainProcess()
