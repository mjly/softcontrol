# -*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import *

# Settings to connect to mysql database  
database_setting = {'database_type': 'mysql',  # 数据库类型  
                    'connector': 'pymysql',  # 数据库连接器
                    'soft_name': 'merlin',  # 软件名，根据实际情况修改
                    'password': 'merlin',  # 软件密码，根据实际情况修改
                    'host_name': '10.10.6.222',  # 在本机上运行  
                    'database_name': 'soft_manage',
                    }


# 下面这个类就是实体类，对应数据库中的soft表  
class Soft(object):
    def __init__(self, soft_name, soft_version,
                 soft_md5, soft_sha1, soft_dep):
        self.soft_name = soft_name
        self.soft_version = soft_version
        self.soft_md5 = soft_md5
        self.soft_sha1 = soft_sha1
        self.soft_dep = soft_dep

    # 这个类就是直接操作数据库的类  


class SoftManageORM():
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
            database_setting['soft_name'] +
            ':' +
            database_setting['password'] +
            '@' +
            database_setting['host_name'] +
           r'/' +
            database_setting['database_name']
        )
        self.metadata = MetaData(self.engine)
        self.soft_table = Table('soft_info', self.metadata,
                                autoload=True)

        # 将实体类soft映射到soft表  
        mapper(Soft, self.soft_table)

        # 生成一个会话类，并与上面建立的数据库引擎绑定  
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)

        # 创建一个会话  
        self.session = self.Session()

    def CreateNewSoft(self, soft_info):
        ''''' 
            # 这个方法根据传递过来的软件信息列表新建一个软件 
            # soft_info是一个列表，包含了从表单提交上来的信息 
        '''
        new_soft = Soft(
            soft_info['soft_name'],
            soft_info['soft_version'],
            soft_info['soft_md5'],
            soft_info['soft_sha1'],
            soft_info['soft_dep']
        )
        self.session.add(new_soft)  # 增加新软件  
        self.session.commit()  # 保存修改  

    def GetSoftByName(self, soft_name):  # 根据软件名返回信息
        return self.session.query(Soft).filter_by(
            soft_name=soft_name).all()[0]

    def GetAllSoft(self):  # 返回所有软件的列表
        return self.session.query(Soft)

    def UpdateSoftInfoByName(self, soft_info):  # 根据提供的信息更新软件资料
        soft_name = soft_info['soft_name']
        soft_info_without_name = {'soft_version': soft_info['soft_version'],
                                  'soft_md5': soft_info['soft_md5'],
                                  'soft_sha1': soft_info['soft_sha1'],
                                  'soft_dep': soft_info['soft_dep']
                                  }
        self.session.query(Soft).filter_by(soft_name=soft_name).update(
            soft_info_without_name)
        self.session.commit()

    def DeletesoftByName(self, soft_name):  # 删除指定名的软件
        soft_need_to_delete = self.session.query(Soft).filter_by(
            soft_name=soft_name).all()[0]
        self.session.delete(soft_need_to_delete)
        self.session.commit()  