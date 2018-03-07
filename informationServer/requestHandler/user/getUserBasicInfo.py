from infoOrm import *
from infoServerUrl import BLOGPART,BLOGREADROLE
'''
获取在发表文章时，需要的选择信息，如文章分类，已有的文章名等
请求数据格式
{
    'sessionId':id
}
返回的数据格式：
{
    classify:[
    {
    'value':'partname
    'label':partname
    'children':[
        {
            value: classifyname,
            label: classifyname,
        }
        ]
    },
    {
    ......
    }
    ],


    articles:[name1,name2,...],
    readrole:[role1,role2,....]
}
'''

class GetUserBasicInfo():
    def entry(self,username):
        userarticles=MyBaseModel.returnList(blogArticle.select(blogArticle.articleName).where(blogArticle.articleAuthor==username))
        articles=[]
        for article in userarticles:
            articles.append(article['articleName'])
        readrole=BLOGREADROLE[0:2]
        classify=[]
        for part in BLOGPART:
            if part!='未选择':
                userclassifies=MyBaseModel.returnList(blogClassify.select(blogClassify.classifyName).where(blogClassify.userName==username,blogClassify.belongPart==BLOGPART.index(part)))
                if len(userclassifies)>0:
                    children=[]
                    for line in userclassifies:
                        children.append({'value':line['classifyName'],'label':line['classifyName']})
                    classify.append({'value':part,'label':part,'children':children})

        return {'status':1,'articles':articles,'readrole':readrole,'classify':classify}
