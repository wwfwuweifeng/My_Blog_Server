from infoOrm import *
from datetime import datetime
from infoServerUrl import BLOGPART
'''
在装饰器中取得用户名，，从请求中取出分类名,判断操作类型
请求数据格式：
{
'sessionId':sessionId,
'classifyname':classifyname,
'operation':'add'、'del'
'belongpart':partname

}
注意使用peewee模块时，要进行数据库筛选时，且筛选条件有两个，应使用','，不是使用 and
'''
class AddOrDelClassify():
    def entry(self,receiveRequest,username):

        classifyname=receiveRequest.get_argument('classifyname')
        operation=receiveRequest.get_argument('operation')
        belongpart=receiveRequest.get_argument('belongpart')
        classify = MyBaseModel.returnList(blogClassify.select(blogClassify.articleNum).where(
            blogClassify.classifyName == classifyname , blogClassify.userName == username))
        if operation=='del':
            assert len(classify)==1,'搜索到的某用户的某分类不唯一或不存在'
            if classify[0]['articleNum']>0:
                return {'status':0,'errorInfo':('无法删除该分类，有%d篇文章位于该分类'%classify[0]['articleNum'])}
            else:
                with db.execution_context():
                    blogClassify.delete().where(blogClassify.userName==username , blogClassify.classifyName==classifyname).execute()
                return {'status':1,'info':'删除成功'}
        elif operation =='add':
            if len(classify)>0:
                return {'status':0,'errorinfo':'该分类已经存在，无法再次创建'}
            else:
                with db.execution_context():
                    blogClassify.create(**{'userName': username, 'belongPart': BLOGPART.index(belongpart), 'classifyName':
                                classifyname, 'createDate': datetime.today().date(), 'articleNum': 0})

                return {'status':1,'info':'添加分类成功'}

