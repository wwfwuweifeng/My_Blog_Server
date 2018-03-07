from infoOrm import *
from datetime import datetime
import random
from infoServerUrl import BLOGPART,BLOGREADROLE
'''
请求的数据格式：
data{
    'sessionId':sessionId
    'body':body
    'state':0
    'name':name
    'articleurl':'若为1，则为新添加文章，若为其他值，则是编辑文章'
}
保存文章分为两种情况：
1：第一次保存
2：多次保存
'''
class SaveNotFinishArticle():
    def entry(self,receiveRequest,username):
        self.body = receiveRequest.get_argument('body')
        self.state = receiveRequest.get_argument('state')
        self.name = receiveRequest.get_argument('name')
        self.articleurl = receiveRequest.get_argument('articleurl')
        if self.articleurl == '1':
            judge_result = self.judge(username)
            if judge_result['status'] == 0:
                return judge_result
            else:
                return self.firstSaveArticle(username)
        else:
            return self.saveArticle(username)



    def judge(self,username):
        article=MyBaseModel.returnList(blogArticle.select(blogArticle.id).where(blogArticle.articleAuthor==username,blogArticle.articleName==self.name))
        if len(article)>0:
            return {'status':0,'errorinfo':'您的文章列表中存在同名的文章，保存失败'}

        return {'status':1}


    def firstSaveArticle(self,username):
        with db.execution_context():
            maxid=blogArticle.select(blogArticle.id).aggregate(fn.Max(blogArticle.id))
            if maxid==None:
                maxid=0
            url=self.setArticleUrl(maxid+1)
            blogArticle.create(**{'articleName':self.name,'articleAuthor':username,'articleIntroduce':'暂无',
                                'articlePart':BLOGPART.index('未选择'),'articleEditorTime':datetime.today(),'articleClassify':'未选择',
                                'articleReadRole':BLOGREADROLE.index('未选择'),'articleState':int(self.state),'articleBody':self.body,
                                'articleReadTimes':0,'articleUrl':url})
        return {"status":1,'info':'操作成功','url':url}



    def saveArticle(self,username):

        old_article=MyBaseModel.returnList(blogArticle.select(blogArticle.articleName).where(blogArticle.articleUrl==self.articleurl))
        if old_article[0]['articleName'] !=self.name:
            judge_result = self.judge(username)
            if judge_result['status'] == 0:
                return judge_result

        with db.execution_context():
            blogArticle.update(**{'articleName': self.name, 'articleEditorTime': datetime.today(),'articleState': int(self.state),
                                  'articleBody': self.body}).where(blogArticle.articleUrl == self.articleurl).execute()
        return {"status": 1, 'info': '操作成功'}



    def setArticleUrl(self,maxid):
        article_id = ''
        for i in range(6):
            article_id += str(random.randint(0, 9))  # 0<=num<=9
        article_id = str(maxid) + article_id
        return str(article_id)

