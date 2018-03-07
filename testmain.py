# from fileServer.requestHandler.receiveImg import *
import hashlib
from informationServer.infoOrm import *
def md5():
    m = hashlib.md5()
    m.update(bytes('1', encoding='utf8'))
    return m.hexdigest()
print(md5())
import random
import time
import re
from datetime import datetime
def getArticleId(num):
    article_id=''
    for i in range(6):
        article_id+=str(random.randint(0,9))#0<=num<=9
    article_id=str(num)+article_id
    return article_id


# with db.execution_context():
    # print(blogArticle.select(blogArticle.id).aggregate(fn.Max(blogArticle.id)))
    # blogUser.update(**{'userRole':2}).where(blogUser.userName=='zyz').execute()
#     # blogUser.delete().where(blogUser.id==4).execute()
#
# print(MyBaseModel.returnList(blogUser.select(blogUser.userName,blogUser.id).order_by(-blogUser.userRole,-blogUser.id)))


tt=[1,2,3,4,5]
tt= tt if len(tt)<4 else tt[0:3]
print(tt)
# def test1(name,pwd=None):
#     print(name,pwd)
#
# def test2(name,*args):
#     test1(name,*args)
#
# test2('wwf')
#
# now=datetime.today().strftime("%Y/%m/%d %H:%M:%S")
# now2=datetime.today().date()
# print(now2,str(now2))







