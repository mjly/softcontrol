
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship



database_setting = {'database_type': 'mysql',  # 数据库类型
                    'connector': 'pymysql',  # 数据库连接器
                    'name': 'merlin',  # 软件名，根据实际情况修改
                    'password': 'merlin',  # 软件密码，根据实际情况修改
                    'host_name': '10.10.6.222',  # 在本机上运行
                    'database_name': 'soft_manage',
                    }

Base = declarative_base()

class Dep(Base):
    __tablename__ = 'dep_info'
    name = Column(String(64), nullable=True)
    id = Column(Integer, primary_key=True)

class Soft(Base):
    __tablename__ = 'soft_info'

    name = Column(String(64), primary_key=True)
    md5 = Column(String(64), nullable=False)
    sha1 = Column(String(64), nullable=False)
    dep = Column(Integer,ForeignKey('dep_info.id'), nullable=False)

class User(Base):
    __tablename__ = 'user_info'

    name = Column(String(64), primary_key=True)
    dep = Column(Integer, ForeignKey('dep_info.id'), nullable=False)

class ORMManager():
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
            database_setting['name'] +
            ':' +
            database_setting['password'] +
            '@' +
            database_setting['host_name'] +
           r'/' +
            database_setting['database_name']
        )


        # 生成一个会话类，并与上面建立的数据库引擎绑定
        self.Session = sessionmaker()
        self.Session.configure(bind=self.engine)

        # 创建一个会话
        self.session = self.Session()


    def CreateNewSoft(self, info):
        '''''
            # 这个方法根据传递过来的软件信息列表新建一个软件
            # info是一个列表，包含了从表单提交上来的信息
        '''
        new_soft = Soft(
            name = info['name'],
            md5 = info['md5'],
            sha1 =info['sha1'],
            dep = info['dep']
        )
        self.session.add(new_soft)  # 增加新软件
        self.session.commit()  # 保存修改

    def GetSoftByName(self, name):  # 根据软件名返回信息
        return self.session.query(Soft).filter_by(
            name=name).all()[0]
    def GetSoftByMd5(self, md5):  # 根据软件md5返回信息
        return self.session.query(Soft).filter_by(
            md5=md5).all()[0]

    def GetAllSoft(self):  # 返回所有软件的列表
        return self.session.query(Soft)

    def UpdateSoftInfoByName(self, info):  # 根据提供的信息更新软件资料
        name = info['name']
        info_without_name = {'md5': info['md5'],
                             'sha1': info['sha1'],
                             'dep': info['dep']
                              }
        self.session.query(Soft).filter_by(name=name).update(
            info_without_name)
        self.session.commit()

    def DeletesoftByName(self, name):  # 删除指定名的软件
        need_to_delete = self.session.query(Soft).filter_by(
            name=name).all()[0]
        self.session.delete(need_to_delete)
        self.session.commit()

    def CreateNewUser(self, info):
        ''''' 
            # 这个方法根据传递过来的用户信息列表新建一个用户 
            # info是一个列表，包含了从表单提交上来的信息 
        '''
        new_user = User(
            name = info['name'],
            dep = info['dep']
        )
        self.session.add(new_user)  # 增加新用户  
        self.session.commit()  # 保存修改  

    def GetUserByName(self, name):  # 根据用户名返回信息
        return self.session.query(User).filter_by(
            name=name).all()[0]

    def GetUserByDep(self, dep):  # 根据用户dep返回信息
        return self.session.query(User).filter_by(
            dep=dep)

    def GetAllUser(self):  # 返回所有用户的列表
        return self.session.query(User)

    def UpdateUserInfoByName(self, info):  # 根据提供的信息更新用户资料
        name = info['name']
        info_without_name = {'dep': info['dep']}
        self.session.query(User).filter_by(name=name).update(
            info_without_name)
        self.session.commit()

    def DeleteuserByName(self, name):  # 删除指定名的用户
        need_to_delete = self.session.query(User).filter_by(
            name=name).all()[0]
        self.session.delete(need_to_delete)
        self.session.commit()
# if __name__ == "__main__":
#     engine = create_engine(  # 生成连接字符串，有特定的格式
#         database_setting['database_type'] +
#         '+' +
#         database_setting['connector'] +
#         r'://' +
#         database_setting['name'] +
#         ':' +
#         database_setting['password'] +
#         '@' +
#         database_setting['host_name'] +
#         r'/' +
#         database_setting['database_name']
#        )
#     Base.metadata.create_all(engine)