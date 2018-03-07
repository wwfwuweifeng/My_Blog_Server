# -*- coding:utf-8 -*-
import tornado
from fileServerRequest import *

myUrl='http://47.95.203.78:5000/getImg'

class MyApplication(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/test", TestHandler),
            # (r"/getImg/ImgFirst/wwf/test", ResponseImgHandler)
            (r"/getImg/([^/]+)/([^/]+)/([^/]+)",ResponseImgHandler),
            (r"/uploadImg",ReceiveImgHandler)
        ]

        settings = {

        }
        tornado.web.Application.__init__(self, handlers,debug = False,**settings)
                #使用多进程的时候，记得设置为false