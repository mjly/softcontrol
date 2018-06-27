#!/usr/bin/env python  

# This is a Web Server for userManager  


import tornado.httpserver  # 引入tornado的一些模块文件
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from models import orm

orm = orm.ORMManager()  # 创建一个全局ORM对象


class UserMainHandler(tornado.web.RequestHandler):  # 主Handler，用来响应首页的URL
    ''''' 
        MainHandler shows all data and a form to add new user 
    '''

    def get(self):  # 处理主页面(userManager.html)的GET请求  
        # show all data and a form  
        title = 'user Manager V0.1'  # 这个title将会被发送到userManager.html中的{{title}}部分  

        users = orm.GetAllUser()  # 使用ORM获取所有用户的信息
        # 下面这一行会将title和users两个变量分别发送到指定模板的对应变量中去  
        self.render('../templates/UserManager.html', title=title, users=users)  # 并显示该模板页面

    def post(self):
        pass  # 这里不处理POST请求  


class AddUserHandler(tornado.web.RequestHandler):  # 响应/Adduser的URL
    ''''' 
        AdduserHandler collects info to create new user 
    '''

    def get(self):
        pass

    def post(self):  # 这个URL只响应POST请求，用来收集用户信息并新建记录  
        # Collect info and create a user record in the database  
        info = {
            'name': self.get_argument('name'),
            'dep': self.get_argument('dep')
        }
        orm.CreateNewUser(info)  # 调用ORM的方法将新建的用户信息写入数据库

        self.redirect('http://localhost:9999/user/')  # 页面转到首页


class EditUserHandler(tornado.web.RequestHandler):  # 响应/Edituser的URL
    ''''' 
        Show a page to edit user info, 
        user name is given by GET method 
    '''

    def get(self):  # /Edituser的URL中，响应GET请求  
        info = orm.GetUserByName(self.get_argument('name'))  # 利用ORM获取指定用户的信息
        self.render('../templates/EditUserInfo.html', info=info)  # 将该用户信息发送到EdituserInfo.html以供修改

    def post(self):
        pass


class UpdateUserInfoHandler(tornado.web.RequestHandler):  # 用户信息编辑完毕后，将会提交到UpdateuserInfo，由此Handler处理
    ''''' 
        Update user info by given list 
    '''

    def get(self):
        pass

    def post(self):  # 调用ORM层的UpdateuserInfoByName方法来更新指定用户的信息  
        orm.UpdateUserInfoByName({
            'name': self.get_argument('name'),
            'dep': self.get_argument('dep'),
        })
        self.redirect('http://localhost:9999/user/')  # 数据库更新后，转到首页


class DeleteUserHandler(tornado.web.RequestHandler):  # 这个Handler用来响应/Deleteuser的URL
    ''''' 
        Delete user by given name 
    '''

    def get(self):
        # 调用ORM层的方法，从数据库中删除指定的用户  
        orm.DeleteuserByName(self.get_argument('name'))

        self.redirect('http://localhost:9999/user/')  # 数据库更新后，转到首页

    def post(self):
        pass



