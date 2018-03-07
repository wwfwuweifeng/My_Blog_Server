from infoOrm import *
from infoServerUrl import BLOGPART
'''
直接在装饰器中取得用户名，传进来
'''
class GetUserClassify():
    def entry(self,username):
        userClassify=MyBaseModel.returnList(blogClassify.select().where(blogClassify.userName==username))
        result=[]
        for line in userClassify:
            classify={'part':BLOGPART[line['belongPart']],'classifyname':line['classifyName'],
                      'num':line['articleNum'],'createdate':str(line['createDate'].date())}
            result.append(classify)
        return {"status":1,'data':list(reversed(result))}