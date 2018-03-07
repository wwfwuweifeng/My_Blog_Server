from tornado import web
import time
from informationServer.requestHandler.login.mySession import Session
from informationServer.infoLogConfig import logger, errorMessage
from informationServer.requestHandler.login.userLogin import UserLogin
from informationServer.requestHandler.article.addOrEditorArticle import AddOrEditorArticle
from informationServer.requestHandler.article.getArticleList import GetArticleList
from informationServer.requestHandler.user.addOneUser import AddOneUser
from informationServer.requestHandler.user.addOrDelClassify import AddOrDelClassify
from informationServer.requestHandler.user.getUserClassify import GetUserClassify
from informationServer.requestHandler.user.getUserName import GetUserName
from informationServer.requestHandler.user.getUserBasicInfo import GetUserBasicInfo
from informationServer.requestHandler.article.delArticle import DelArticle
from informationServer.requestHandler.article.saveNotFinishArticle import SaveNotFinishArticle
from informationServer.requestHandler.article.getHotArticleList import GetHotArticleList
from informationServer.requestHandler.article.getArticle import GetArticle
from informationServer.requestHandler.getSomeInfo.searchSomeInfo import SearchSomeInfo

def isClose(request_self):
    request_self.finish({'status': 0, 'errorInfo': "功能关闭时间00：30-05：30", 'data': ''})


def judgeIsOpen(func):  # 用于检测服务器是否关闭
    def is_open(self_request):
        now = int(time.strftime("%H%M%S"))
        if now >= 3000 and now <= 53000:  # 服务关闭
            return isClose(self_request)
        else:
            return func(self_request)
    return is_open

def judgeIsLogin(func):
    def is_login(self_request,*args):
        mySession=Session(self_request)
        username=mySession['getname']
        if username==None:
            del mySession
            self_request.finish({"status": 0, "errorInfo": "请先登录"})
        else:
            username=username.decode('utf-8')
            args=args+(username,)
            func(self_request,*args)
    return is_login



def getErrorMessage(post):
    def diyPost(self_request, *args):
        try:
            post(self_request, *args)
        except Exception as e:
            logger.warning(errorMessage(e))
            self_request.finish({"status": 0, "errorInfo": "服务器出错，请稍后再试"})

    return diyPost


class BaseHandler(web.RequestHandler):  # 每个请求的基类
    def initialize(self):
        self.set_header("Access-Control-Max-Age", 3628800)
        self.set_header('Content-type', 'multipart/form-data')
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,authorization")
        self.set_header('Access-Control-Allow-Methods', 'POST,GET,PUT,DELETE,OPTIONS')
        self.set_header('Access-Control-Allow-Credentials', True)
        self.set_header("Access-Control-Allow-Origin", "*")


class TestHandler(BaseHandler):
    def post(self):
        print(self.request.headers['Origin'])
        self.set_cookie(Session.session_id, '1231312312')
        print('i am get')
        self.finish({'status': 1})

    def get(self, *args, **kwargs):
        print(self.request)




class AddOrEditorArticleHandler(BaseHandler):
    @getErrorMessage
    @judgeIsLogin
    def post(self, *args, **kwargs):
        self.finish(AddOrEditorArticle().entry(self,*args))

class GetArticleListHandler(BaseHandler):
    @getErrorMessage
    @judgeIsLogin
    def post(self, *args, **kwargs):
        self.finish(GetArticleList().entry(*args))

    @getErrorMessage
    def get(self, *args, **kwargs):
        self.finish(GetArticleList().entry())

class AddOneUserHandler(BaseHandler):
    @getErrorMessage
    def post(self, *args, **kwargs):
        self.finish(AddOneUser().entry(self))

class AddOrDelClassifyHandler(BaseHandler):
    @getErrorMessage
    @judgeIsLogin
    def post(self, *args, **kwargs):
        self.finish(AddOrDelClassify().entry(self,*args))

class GetUserClassifyHandler(BaseHandler):
    @getErrorMessage
    @judgeIsLogin
    def post(self, *args, **kwargs):
        self.finish(GetUserClassify().entry(*args))

class ResponseArticleHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.finish('ok')

class DelArticleHandler(BaseHandler):
    @getErrorMessage
    @judgeIsLogin
    def post(self, *args, **kwargs):
        self.finish(DelArticle().entry(self,*args))

class GetArticleHandler(BaseHandler):
    @getErrorMessage
    def get(self, *args):
        self.finish(GetArticle().entry(self))

    @getErrorMessage
    @judgeIsLogin
    def post(self, *args, **kwargs):
        self.finish(GetArticle().entry(self,*args))

class GetHotArticleListHandler(BaseHandler):
    @getErrorMessage
    def get(self, *args, **kwargs):
        self.finish(GetHotArticleList().entry())

class SaveNotFinishArticleHandler(BaseHandler):
    @getErrorMessage
    @judgeIsLogin
    def post(self, *args, **kwargs):
        self.finish(SaveNotFinishArticle().entry(self,*args))

class GetUserBasicInfoHandler(BaseHandler):
    @getErrorMessage
    @judgeIsLogin
    def post(self, *args, **kwargs):
        self.finish(GetUserBasicInfo().entry(*args))

class GetUserNameHandler(BaseHandler):
    @getErrorMessage
    def post(self, *args, **kwargs):
        self.finish(GetUserName().entry(self))

class LoginHandler(BaseHandler):
    @getErrorMessage
    def post(self, *args, **kwargs):
        self.finish(UserLogin().entry(self))

class CancleLoginHandler(BaseHandler):
    @getErrorMessage
    @judgeIsLogin
    def post(self, *args):
        mySession=Session(self)
        del mySession['user']
        self.finish({'status':1})

class SeachSomeInfoHandler(BaseHandler):
    @getErrorMessage
    def post(self, *args, **kwargs):
        mySession = Session(self)
        username = mySession['getname']
        if username == None:
            del mySession
            self.finish(SearchSomeInfo().entry(self))
        else:
            username = username.decode('utf-8')
            self.finish(SearchSomeInfo().entry(self,username))

