# coding=utf8

from peewee import SelectQuery, CharField, IntegerField, fn, Model, FloatField, MySQLDatabase, TextField,\
    DateTimeField,TextField
from playhouse.shortcuts import model_to_dict as to_dict
import playhouse as ph

from playhouse.pool import PooledMySQLDatabase
from fileLogConfig import filelogger

users=[{'name':'','pwd':''}]
for user in users:
  try:
      db = PooledMySQLDatabase(
      database='myblog',
      max_connections=4,
      stale_timeout=60,  # 1 hour
      timeout=0,
      user=user['name'],
      host='127.0.0.1',
      passwd=user['pwd'],
      )
      with db.execution_context():
          pass
      break
  except:
      filelogger.warning("this mysql username is not "+user['name'])


def applyConnect(func):
    def applyFunc(cls, *args, **kwargs):
      with db.execution_context():
        return func(cls, *args, **kwargs)
    return applyFunc

# Model是peewee的基类
class MyBaseModel(Model):
    class Meta:
        database = db

    @classmethod
    @applyConnect
    def getOne(cls, *query, **kwargs):

        """
        为了方便使用，新增此接口，查询不到返回None，而不抛出异常
        """
        try:
            return cls.get(*query, **kwargs)
        except:
            raise

    @classmethod
    @applyConnect
    def returnList(cls, Model=None, key=None):
        """
        将结果返回成一个列表嵌套字典的结构返回
        """
        if not type(Model) == SelectQuery:
            return None
        list = []
        for con in Model:
            if type(con) == dict:
                if not key == None:
                    list.append(con[key])
                else:
                    list.append(con)
            else:
                list.append(to_dict(con))
        return list


class blogUser(MyBaseModel):
    userName=CharField(null=False)
    userPwd=CharField(null=False)
    userEmail=CharField(null=True)
    userImgPart=CharField(null=False)
    userRole=CharField(null=True)
    userCollectionArticle=TextField(null=True)
    userCollectionBlog=TextField(null=True)
    class Meta:
        db_table = 'blog_user'
        # primary_key=True

class blogClassify(MyBaseModel):
    userName=CharField(null=False)
    belongPart=IntegerField(null=False)
    classifyName=CharField(null=False)
    createDate=DateTimeField(null=False)
    articleNum=IntegerField(null=False)
    class Meta:
        db_table='blog_classify'



class blogArticle(MyBaseModel):
    articleName=CharField(null=False)
    articleAuthor=CharField(null=False)
    articleIntroduce=TextField(null=False)
    articlePart=IntegerField(null=False)
    articleEditorTime=DateTimeField(null=False)
    articleClassify=CharField(null=False)
    articleReadRole=IntegerField(null=False)    #1表所有人，0表自己
    articleState=IntegerField(null=False)   #0表示未完成，1表示完成
    articleBody=TextField(null=True)
    articleReadTimes=IntegerField(null=False)
    articleUrl=CharField(null=False)
    class Meta:
        db_table='blog_article'
        # primary_key=True


# max_date = stu_transaction_record.select(stu_transaction_record.tradingTime).where(stu_transaction_record.stuID == stu_id).aggregate(fn.Max(stu_transaction_record.tradingTime))
db.create_tables([blogUser,blogArticle], safe=True)