from informationServer.infoOrm import *
import re
from informationServer.infoServerUrl import BLOGPART,BLOGREADROLE

'''
请求格式：
post：进行文章模糊搜索
{
    'searchStr':str
}

'''

class SearchSomeInfo():
    def entry(self,receiveRequest,userName=None):
        searchStr = receiveRequest.get_argument('searchStr')
        # searchStr=receiveRequest
        t_articles = MyBaseModel.returnList(
            blogArticle.select(blogArticle.articleAuthor, blogArticle.articleIntroduce, blogArticle.articleEditorTime,
                               blogArticle.articleName, blogArticle.articlePart, blogArticle.articleReadTimes,
                               blogArticle.articleUrl, blogArticle.id).where(blogArticle.articleState == 1,
                                                                             blogArticle.articleReadRole == 1))
        if userName!=None:

            t_articles_myself = MyBaseModel.returnList(
                blogArticle.select(blogArticle.articleAuthor, blogArticle.articleIntroduce,
                                   blogArticle.articleEditorTime, blogArticle.articleName, blogArticle.articlePart,
                                   blogArticle.articleReadTimes,
                                   blogArticle.articleUrl, blogArticle.id).where(blogArticle.articleAuthor==userName,blogArticle.articleState==1,blogArticle.articleReadRole==0))
            for article in t_articles_myself:
                t_articles.append(article)

        articles = []
        search_result=self.search(searchStr,t_articles)
        for article in t_articles:
            if article['id'] in search_result:
                articles.append({'name': article['articleName'], 'author': article['articleAuthor'],
                                 'part': BLOGPART[article['articlePart']], 'introduce': article['articleIntroduce'],
                                 'time': article['articleEditorTime'].strftime("%Y-%m-%d %H:%M:%S"),
                                 'readtimes': article['articleReadTimes'],
                                 'url': '/showarticle/' + article['articleUrl']})

        return {'status': 1, 'articles': articles}

    def search(self,searchStr,collection):  #返回匹配的文章ID
        suggestions = []
        pattern = '.*'.join(searchStr)
        regex = re.compile(pattern, re.I)
        for item in collection:
            match_articleName = regex.search(item['articleName'])
            if match_articleName:
                suggestions.append((len(match_articleName.group()), match_articleName.start(), item['id']))
            else:
                match_articleIntroduce = regex.search(item['articleIntroduce'])
                if match_articleIntroduce:
                    suggestions.append(
                        (len(match_articleIntroduce.group()), match_articleIntroduce.start(), item['id']))
                else:
                    match_articleAuthor = regex.search(item['articleAuthor'])
                    if match_articleAuthor:
                        suggestions.append(
                            (len(match_articleAuthor.group()), match_articleAuthor.start(), item['id']))

        return [x for _, _, x in sorted(suggestions)]













