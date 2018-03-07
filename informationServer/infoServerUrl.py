# -*- coding:utf-8 -*-
import tornado
BLOGPART=['编程语言','操作系统','开发框架','学习笔记','其他','未选择']
BLOGREADROLE=['自己','所有人','部分人','未选择']
from informationServer.infoServerRequest import *

class MyApplication(tornado.web.Application):
    def __init__(self):
        handlers = [

            (r"/test", TestHandler),
            (r"/login",LoginHandler),
            (r"/canclelogin",CancleLoginHandler),
            (r"/user/addoneuser",AddOneUserHandler),
            (r"/user/addordelclassify",AddOrDelClassifyHandler),
            (r"/user/getuserclassify",GetUserClassifyHandler),
            (r"/user/getusername",GetUserNameHandler),
            (r"/user/getuserbasicinfo",GetUserBasicInfoHandler),
            (r"/article/addoreditorarticle",AddOrEditorArticleHandler),
            (r"/article/getarticlelist",GetArticleListHandler),
            (r"/article/delarticle",DelArticleHandler),
            (r"/article/gethotarticlelist",GetHotArticleListHandler),
            (r"/article/savenotfinisharticle",SaveNotFinishArticleHandler),
            (r"/article/getarticle",GetArticleHandler),
            (r"/getsomeinfo/searchsomeinfo",SeachSomeInfoHandler)

        ]

        settings = {

        }
        tornado.web.Application.__init__(self, handlers,debug = False,**settings)
                #使用多进程的时候，记得设置为false