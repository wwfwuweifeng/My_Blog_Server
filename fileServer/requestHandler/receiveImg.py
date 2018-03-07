import redis
from fileLogConfig import filelogger,errorMessage
from fileOrm import *
import os
import imghdr
#from fileServerUrl import myUrl
myUrl='http://47.95.203.78:5000/getImg'
class ReceiveImg():
    def entry(self,myImg,sessionId):
        r=redis.Redis(host='127.0.0.1',port=6379)
        userName=r.get(sessionId)
        #userName='zyz'
        if userName==None:
            return {'status':0,'errorinfo':'请先登录'}
        else:
            try:
                userName=userName.decode('utf-8')
                return self.saveImg(myImg,userName)
            except Exception as e:
                filelogger.info(userName + '上传图片：' + myImg['filename'] + '失败')
                filelogger.warning(errorMessage(e))
                return {'status':0,'errorInfo':'上传图片失败'}

    def saveImg(self,myImg,userName):
        # user=MyBaseModel.returnList(blogUser.select(blogUser.userImgPart).where(blogUser.userName==userName))
        user=[{"userImgPart":'ImgMyself'}]
        assert len(user)==1,'该用户不存在'
        imgPart=user[0]['userImgPart']
        dirpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        dirpath = dirpath + '/saveImgFile/'+imgPart+'/'+userName
        filepath=dirpath+'/'+myImg['filename']
        if os.path.isdir(dirpath)==False:
            os.mkdir(dirpath)
        with open(filepath, 'wb') as f:
            f.write(myImg['body'])
        imgType=imghdr.what(filepath)
        if imgType==None:
            os.remove(filepath)
            filelogger.warning('\n\t'+userName+'上传非法文件,已被拦截并且移除')
            return {'status':0,'errorInfo':'请确保上传的是图片格式的文件'}

        filelogger.info(userName + '上传图片：' + myImg['filename'] + '成功')
        imgUrl=myUrl+'/'+imgPart+'/'+userName+'/'+myImg['filename']
        return {'status':1,'data':{'imgUrl':imgUrl}}

