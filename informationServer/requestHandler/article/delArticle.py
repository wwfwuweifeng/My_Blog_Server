from infoOrm import *
'''
请求数据格式：
{
    'sessionId':sessionId,
    'articleurl':url

}
对文章进行删除
'''
class DelArticle():
    def entry(self,receiveRequest,username):
        self.articleurl = receiveRequest.get_argument('articleurl')
        article=MyBaseModel.returnList(blogArticle.select(blogArticle.articleAuthor,blogArticle.articleClassify).where(blogArticle.articleUrl==self.articleurl))
        if article[0]['articleAuthor']==username:
            with db.execution_context():
                if  article[0]['articleClassify']!='未选择':
                    classify=blogClassify.select().where(blogClassify.userName==username,blogClassify.classifyName==article[0]['articleClassify']).get()
                    classify.articleNum=classify.articleNum-1
                    classify.save()
                blogArticle.delete().where(blogArticle.articleUrl==self.articleurl).execute()
            return {'status':1,'info':'删除成功'}
        else:
            return {'status':0,'errorInfo':'删除失败，您无权进行此操作'}