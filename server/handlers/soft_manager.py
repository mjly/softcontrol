#!/usr/bin/env python  

# This is a Web Server for softManager  


import tornado.httpserver  # 引入tornado的一些模块文件
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from models import soft_orm

define('port', default=9999, help='run on the given port', type=int)

soft_orm = soft_orm.SoftManageORM()  # 创建一个全局ORM对象


class SoftMainHandler(tornado.web.RequestHandler):  # 主Handler，用来响应首页的URL
    ''''' 
        MainHandler shows all data and a form to add new soft 
    '''

    def get(self):  # 处理主页面(softManager.html)的GET请求  
        # show all data and a form  
        title = 'soft Manager V0.1'  # 这个title将会被发送到softManager.html中的{{title}}部分  

        softs = soft_orm.GetAllSoft()  # 使用ORM获取所有软件的信息
        # 下面这一行会将title和softs两个变量分别发送到指定模板的对应变量中去  
        self.render('../templates/SoftManager.html', title=title, softs=softs)  # 并显示该模板页面

    def post(self):
        pass  # 这里不处理POST请求  


class AddSoftHandler(tornado.web.RequestHandler):  # 响应/Addsoft的URL
    ''''' 
        AddsoftHandler collects info to create new soft 
    '''

    def get(self):
        pass

    def post(self):  # 这个URL只响应POST请求，用来收集软件信息并新建记录  
        # Collect info and create a soft record in the database  
        soft_info = {
            'soft_name': self.get_argument('soft_name'),
            'soft_version': self.get_argument('soft_version'),
            'soft_md5': self.get_argument('soft_md5'),
            'soft_sha1': self.get_argument('soft_sha1'),
            'soft_dep': self.get_argument('soft_dep')
        }
        soft_orm.CreateNewSoft(soft_info)  # 调用ORM的方法将新建的软件信息写入数据库

        self.redirect('http://localhost:9999/soft/')  # 页面转到首页


class EditSoftHandler(tornado.web.RequestHandler):  # 响应/Editsoft的URL
    ''''' 
        Show a page to edit soft info, 
        soft name is given by GET method 
    '''

    def get(self):  # /Editsoft的URL中，响应GET请求  
        soft_info = soft_orm.GetSoftByName(self.get_argument('soft_name'))  # 利用ORM获取指定软件的信息
        self.render('../templates/EditSoftInfo.html', soft_info=soft_info)  # 将该软件信息发送到EditsoftInfo.html以供修改

    def post(self):
        pass


class UpdateSoftInfoHandler(tornado.web.RequestHandler):  # 软件信息编辑完毕后，将会提交到UpdatesoftInfo，由此Handler处理
    ''''' 
        Update soft info by given list 
    '''

    def get(self):
        pass

    def post(self):  # 调用ORM层的UpdatesoftInfoByName方法来更新指定软件的信息  
        soft_orm.UpdateSoftInfoByName({
            'soft_name': self.get_argument('soft_name'),
            'soft_version': self.get_argument('soft_version'),
            'soft_md5': self.get_argument('soft_md5'),
            'soft_sha1': self.get_argument('soft_sha1'),
            'soft_dep': self.get_argument('soft_dep'),
        })
        self.redirect('http://localhost:9999/soft/')  # 数据库更新后，转到首页


class DeleteSoftHandler(tornado.web.RequestHandler):  # 这个Handler用来响应/Deletesoft的URL
    ''''' 
        Delete soft by given name 
    '''

    def get(self):
        # 调用ORM层的方法，从数据库中删除指定的软件  
        soft_orm.DeletesoftByName(self.get_argument('soft_name'))

        self.redirect('http://localhost:9999/soft/')  # 数据库更新后，转到首页

    def post(self):
        pass



