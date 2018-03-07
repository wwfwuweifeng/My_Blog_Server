from infoOrm import *
from infoServerUrl import BLOGREADROLE,BLOGPART
'''
get请求
获取热门文章列表
'''
class GetHotArticleList():
    def entry(self):
        t_articles = MyBaseModel.returnList(
            blogArticle.select(blogArticle.articleName,blogArticle.articleUrl).where(
                blogArticle.articleState == 1, blogArticle.articleReadRole == 1).order_by(-blogArticle.articleReadTimes,-blogArticle.articleEditorTime))
        articles =[]
        t_articles=t_articles if len(t_articles)<6 else t_articles[0:6]

        for article in t_articles:
            articles.append({'name': article['articleName'],'url':'/showarticle/'+article['articleUrl']})

        return {'status': 1, 'articles': articles}