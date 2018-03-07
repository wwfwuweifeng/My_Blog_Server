# -*- coding:utf-8 -*-
import tornado.options
import tornado.httpserver
import tornado.ioloop
from tornado.options import options,define
from infoServerUrl import MyApplication

define("port",default=5001,help="跑在5001",type=int)


if __name__=='__main__':
    tornado.options.parse_command_line()
    app = MyApplication()
    # app.listen(options.port)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(options.port)
    http_server.start(4)  # 如果为0,则根据cpu自己创建一定舒服的fork，如果是大于等于1的，则创建对应数目的fork
    tornado.ioloop.IOLoop.instance().start()