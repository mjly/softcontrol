# -*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import *

# Settings to connect to mysql database  
database_setting = {'database_type': 'mysql',  # 数据库类型  
                    'connector': 'pymysql',  # 数据库连接器
                    'user_name': 'merlin',  # 用户名，根据实际情况修改
                    'password': 'merlin',  # 用户密码，根据实际情况修改
                    'host_name': '10.10.6.222',  # 在本机上运行  
                    'database_name': 'soft_manage',
                    }


# 下面这个类就是实体类，对应数据库中的user表  
class User(object):
    def __init__(self, user_name, user_dep):
        self.user_name = user_name
        self.user_dep = user_dep

    # 这个类就是直接操作数据库的类  


class UserManageORM():
    def __init__(self):
        ''''' 
            # 这个方法就是类的构造函数，对象创建的时候自动运行

            "mysql+pymysql://root:123456@localhost/test",
                                    encoding='utf-8', echo=True
        '''
        self.engine = create_engine(  # 生成连接字符串，有特定的格式  
            database_setting['database_type'] +
            '+' +
            database_setting['connector'] +
            r'://' +
            database_setting['user_name'] +
            ':' +
            database_setting['password'] +
            '@' +
            database_setting['host_name'] +
           r'/' +
            database_setting['database_name']
        )
        self.metadata = MetaData(self.engine)
        self.user_table = Table('user_info', self.metadata,
                                autoload=True)

        # 将实体类user映射到user表  
        mapper(User, self.user_table)

        # 生成一个会话类，并与上面建立的数据库引擎绑定  
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)

        # 创建一个会话  
        self.session = self.Session()

    def CreateNewUser(self,user_info):
        ''''' 
            # 这个方法根据传递过来的用户信息列表新建一个用户 
            # user_info是一个列表，包含了从表单提交上来的信息 
        '''
        new_user = User(
            user_info['user_name'],
            user_info['user_dep']
        )
        self.session.add(new_user)  # 增加新用户  
        self.session.commit()  # 保存修改  

    def GetUserByName(self, user_name):  # 根据用户名返回信息
        return self.session.query(User).filter_by(
            user_name=user_name).all()[0]
    def GetUserByDep(self, user_dep):  # 根据用户md5返回信息
        return self.session.query(User).filter_by(
            user_dep=user_dep).all()[0]
    def GetAllUser(self):  # 返回所有用户的列表
        return self.session.query(User)

    def UpdateUserInfoByName(self, user_info):  # 根据提供的信息更新用户资料
        user_name = user_info['user_name']
        user_info_without_name = { 'user_dep': user_info['user_dep']}
        self.session.query(User).filter_by(user_name=user_name).update(
            user_info_without_name)
        self.session.commit()

    def DeleteuserByName(self, user_name):  # 删除指定名的用户
        user_need_to_delete = self.session.query(User).filter_by(
            user_name=user_name).all()[0]
        self.session.delete(user_need_to_delete)
        self.session.commit()  