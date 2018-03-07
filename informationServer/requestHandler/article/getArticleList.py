from infoOrm import *
from infoServerUrl import BLOGPART,BLOGREADROLE
'''
如果是获取全部文章列表：get
{
    无传入数据，单纯的get请求
}

如果是获取个人用户的文章：post
{
    'sessionId':sessionId

}
'''

class GetArticleList():
    def entry(self,username=None):
        if username==None:
            t_articles=MyBaseModel.returnList(blogArticle.select(blogArticle.articleAuthor,blogArticle.articleIntroduce,blogArticle.articleEditorTime,blogArticle.articleName,blogArticle.articlePart,blogArticle.articleReadTimes,
                blogArticle.articleUrl).where(blogArticle.articleState==1,blogArticle.articleReadRole==1))
            articles=[]
            for article in t_articles:
                articles.append({'name':article['articleName'],'author':article['articleAuthor'],
                                 'part':BLOGPART[article['articlePart']],'introduce':article['articleIntroduce'],
                                 'time':article['articleEditorTime'].strftime("%Y-%m-%d %H:%M:%S"),'readtimes':article['articleReadTimes'],'url':'/showarticle/'+article['articleUrl']})

            return {'status':1,'articles':list(reversed(articles)) }
        else:
            states=['未完成','完成']
            t_articles=MyBaseModel.returnList(blogArticle.select(blogArticle.articleState,blogArticle.articleEditorTime,blogArticle.articleReadTimes,blogArticle.articleUrl,
                    blogArticle.articlePart,blogArticle.articleReadRole,blogArticle.articleName,blogArticle.articleClassify).where(blogArticle.articleAuthor==username))
            articles=[]
            for article in t_articles:
                articles.append({'name': article['articleName'],'readtimes':article['articleReadTimes'],'url':article['articleUrl'],'part': BLOGPART[article['articlePart']],'time': article['articleEditorTime'].strftime("%Y-%m-%d %H:%M:%S"),
                                 'classify':article['articleClassify'],'readrole':BLOGREADROLE[article['articleReadRole']],'state':states[article['articleState']]})

            return {'status':1,'articles':list(reversed(articles))}
