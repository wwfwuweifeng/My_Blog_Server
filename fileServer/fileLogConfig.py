import logging
import sys,traceback
import logging.config
import cloghandler
import platform
import os
if 'Windows' in platform.system():
    class_str  = 'logging.handlers.RotatingFileHandler'
else:
    class_str  = 'cloghandler.ConcurrentRotatingFileHandler'
"""
使用前需先安装：ConcurrentLogHandler
        pip install ConcurrentLogHandler
log日志最多保存50M的内容
日志形式为：时间-记录日志的文件名-进程名-日志等级：日志信息
日志文件存放地址为tornado/run_log/log_tornado.log
"""
# LOG_FILE = 'log_tornado.log'
#
# log_file_handler = logging.handlers.TimedRotatingFileHandler(LOG_FILE, when="W0", interval=1, backupCount=4)
# fmt = '%(asctime)s - %(filename)s - %(process)d - %(levelname)s : %(message)s'
#
# formatter = logging.Formatter(fmt)
# log_file_handler.setFormatter(formatter)
# logger = logging.getLogger()
# logger.addHandler(log_file_handler)
# logger.setLevel(logging.INFO)

filepath=os.path.dirname(os.path.abspath(__file__))+'/FileServerLog/log_tornado.log'
print(filepath)
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(filename)s %(levelname)s :%(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        # 'console': {
        #     'level': 'DEBUG',
        #     'class': 'logging.StreamHandler',
        #     'formatter': 'verbose'
        # },
        'file': {
            'level': 'INFO',
            # 如果没有使用并发的日志处理类，在多实例的情况下日志会出现缺失
            'class': class_str,
            # 当达到10MB时分割日志
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 5,
            'encoding':"utf-8",
            'delay': True,
            'filename': filepath,
            'formatter': 'verbose'
        }
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    }
})

filelogger=logging.getLogger()

"""
取出报错栈里的全部错误信息，只用于获取未知错误使用
"""
def errorMessage(error,*args):
  try:
      raise error
  except:
      _, reason, exc_tb = sys.exc_info()
      error = traceback.extract_tb(exc_tb)
      # if len(error)>5:
      #     result=error[0:5]
      # else:
      result=error
      message=' '
      if(len(args)>0):
          message=message+('user: %s request url: %s is fail\n'%(args[0],args[1]))
      message=message+'\t'+str(reason)+'\n'
      for lineError in result:
          message = message+("\tfile: %s--line: %s--errorfunc: %s()--errorsource: %s \n" % (lineError[0], lineError[1], lineError[2], lineError[3]))
      return message
