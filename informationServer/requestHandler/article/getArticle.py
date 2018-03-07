from infoOrm import *
from infoServerUrl import BLOGREADROLE,BLOGPART
'''
请求格式：
get：进行文章展示时
{
    'articleurl':url
}
post：文章作者进行请求，获取文章内容，进行修改等操作
{
    'sessionId':id
    'articleurl':url

}

'''
class GetArticle():
    def entry(self,receiveRequest,username=None):
        articleurl=receiveRequest.get_argument('articleurl')
        if username==None:
            with db.execution_context():
                try:
                    article_t=blogArticle.select().where(blogArticle.articleUrl==articleurl).get()
                except:
                    return {'status':0,'errorInfo':'该文章不存在'}

                if article_t.articleState==0:
                    return {'status':0,'errorInfo':'该文章尚未编辑完成，无法查看'}
                elif article_t.articleReadRole==0:
                    return {'status':0,'errorInfo':'该文章为私有文章，无法查看'}
                else:
                    article_t.articleReadTimes = article_t.articleReadTimes + 1
                    article={'body':article_t.articleBody,'author':article_t.articleAuthor,'date':article_t.articleEditorTime.strftime("%Y-%m-%d %H:%M:%S"),'readtimes':article_t.articleReadTimes,
                             'name':article_t.articleName,'introduce':article_t.articleIntroduce}
                    article_t.save()
            return {'status':1,'article':article}

        else:
            article_t=MyBaseModel.returnList(blogArticle.select().where(blogArticle.articleUrl==articleurl))
            if len(article_t)<1:
                return {'status':0,'errorInfo':'该文章不存在'}
            article_t=article_t[0]
            if article_t['articleAuthor']==username:
                article={'body':article_t['articleBody'],'introduce':article_t['articleIntroduce'],
                         'part':BLOGPART[article_t['articlePart']],'classify':article_t['articleClassify'],
                         'readrole':BLOGREADROLE[article_t['articleReadRole']],'name':article_t['articleName']}
                return {'status':1,'article':article}
            else:
                return {'status':0,'errorInfo':'操作失败，您无权限进行此操作'}