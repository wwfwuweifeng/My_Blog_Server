from tornado import web
import json
import time
from requestHandler.responseImg import ResponseImg
from requestHandler.receiveImg import ReceiveImg
from fileLogConfig import filelogger,errorMessage

def isClose(request_self):
    request_self.finish({'status': 0, 'errorInfo': "功能关闭时间00：30-05：30", 'data': ''})


def judgeIsOpen(func):      #用于检测服务器是否关闭
    def is_open(self_request):
        now=int(time.strftime("%H%M%S"))
        if now>=3000 and now<=53000:    #服务关闭
            return isClose(self_request)
        else:
            return func(self_request)
    return is_open


def getErrorMessage(post):
    def diyPost(self_request,*args):
        try:
            post(self_request,*args)
        except Exception as e:
            filelogger.warning(errorMessage(e))
            self_request.finish({"status":0, "errorInfo":"服务器出错，请稍后再试"})
    return diyPost


class BaseHandler(web.RequestHandler):  #每个请求的基类
    def initialize(self):
        self.set_header("Access-Control-Max-Age", 3628800)
        self.set_header('Content-type','multipart/form-data')
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,authorization")
        self.set_header('Access-Control-Allow-Methods', 'POST,GET,PUT,DELETE,OPTIONS')
        self.set_header("Access-Control-Allow-Origin", "*")


class TestHandler(BaseHandler):
    def post(self):
        print('I am post ')
        # global blog
        # blog=self.get_argument('content')
        self.finish('I am test')

    def get(self, *args, **kwargs):
        self.finish()

    def options(self, *args, **kwargs):
        self.set_status(204)
        print('I am in options')
        self.finish()


class ReceiveImgHandler(BaseHandler):
    @getErrorMessage
    def post(self):
        myImg=self.request.files['file'][0]
        sessionId=self.get_argument('sessionId','no have')
        self.finish(ReceiveImg().entry(myImg,sessionId))

    def options(self, *args, **kwargs):
        self.set_status(204)
        self.finish()


class ResponseImgHandler(BaseHandler):

    @getErrorMessage
    def get(self,*args):
        img=ResponseImg().entry(*args)
        self.set_header("Content-type", " text/plain")
        self.write(img)
        self.finish()
        




# class ReceiveArticleHandler(BaseHandler):
#     def post(self, *args, **kwargs):
#         article = self.get_argument('content')
#         self.finish('ok')
#
#
# class ResponseArticleHandler(BaseHandler):
#     def get(self, *args, **kwargs):
#         self.finish('ok')

