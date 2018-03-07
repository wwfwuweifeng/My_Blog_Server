from infoOrm import *
from datetime import datetime
import random
from infoServerUrl import BLOGPART,BLOGREADROLE
'''
请求的数据格式：
data{
    'sessionId':sessionId
    'part':partname
    'classify':classifyname
    'body':body
    'state':1
    'readrole':1 or 0
    'name':name
    'introduce':introduce
    'articleurl':'若为1，则为新添加文章，若为其他值，则是编辑文章'
}
发表文章分为两种情况：
1：该文章第一次发表，
2：该文章多次修改并发表
'''
class AddOrEditorArticle():
    def entry(self,receiveRequest,username):
        self.part=receiveRequest.get_argument('part')
        self.classify=receiveRequest.get_argument('classify')
        self.body=receiveRequest.get_argument('body')
        self.state=receiveRequest.get_argument('state')
        self.readrole=receiveRequest.get_argument('readrole')
        self.name=receiveRequest.get_argument('name')
        self.introduce=receiveRequest.get_argument('introduce')
        self.articleurl=receiveRequest.get_argument('articleurl')
        if self.articleurl=='1':
            judge_result=self.judge(username)
            if judge_result['status']==0:
                return judge_result
            else:
                return self.addArticle(username)
        else:
            return self.editorArticle(username)

    def judge(self,username):
        article=MyBaseModel.returnList(blogArticle.select(blogArticle.id).where(blogArticle.articleAuthor==username,blogArticle.articleName==self.name))
        if len(article)>0:
            return {'status':0,'errorInfo':'您的文章列表中存在同名的文章，发表失败'}

        return {'status':1}


    def addArticle(self,username):  #初次发表
        with db.execution_context():
            maxid=blogArticle.select(blogArticle.id).aggregate(fn.Max(blogArticle.id))
            if maxid==None:
                maxid=0
            url=self.setArticleUrl(maxid+1)
            blogArticle.create(**{'articleName':self.name,'articleAuthor':username,'articleIntroduce':self.introduce,
                                'articlePart':BLOGPART.index(self.part),'articleEditorTime':datetime.today(),'articleClassify':self.classify,
                                'articleReadRole':BLOGREADROLE.index(self.readrole),'articleState':int(self.state),'articleBody':self.body,
                                'articleReadTimes':0,'articleUrl':url})
            userclassify=blogClassify.select().where(blogClassify.userName==username,blogClassify.classifyName==self.classify).get()
            userclassify.articleNum=userclassify.articleNum+1
            userclassify.save()
        return {"status":1,'info':'操作成功','url':url}

    def editorArticle(self,username):    #多次发表
        old_article=MyBaseModel.returnList(blogArticle.select(blogArticle.articleClassify).where(blogArticle.articleUrl==self.articleurl))
        flag=0
        if old_article[0]['articleClassify']!=self.classify:
            flag=1
            if old_article[0]['articleClassify']!='未选择':
                with db.execution_context():
                    userclassify = blogClassify.select().where(blogClassify.userName == username,blogClassify.classifyName == old_article[0]['articleClassify']).get()
                    userclassify.articleNum = userclassify.articleNum - 1
                    userclassify.save()

        with db.execution_context():
            blogArticle.update(**{'articleName':self.name,'articleIntroduce':self.introduce,
                                'articlePart':BLOGPART.index(self.part),'articleEditorTime':datetime.today(),'articleClassify':self.classify,
                                'articleReadRole':BLOGREADROLE.index(self.readrole),'articleState':int(self.state),'articleBody':self.body}).where(blogArticle.articleUrl==self.articleurl).execute()

        if flag==1:
            with db.execution_context():
                userclassify = blogClassify.select().where(blogClassify.userName == username,
                                                           blogClassify.classifyName == self.classify).get()
                userclassify.articleNum = userclassify.articleNum + 1
                userclassify.save()
        return {"status":1,'info':'操作成功'}


    def setArticleUrl(self,maxid):
        article_id = ''
        for i in range(6):
            article_id += str(random.randint(0, 9))  # 0<=num<=9
        article_id = str(maxid) + article_id
        return str(article_id)