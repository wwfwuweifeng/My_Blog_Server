from infoOrm import *
from commonFunc.getAllUser import GetAllUser
import random
from datetime import datetime
class AddOneUser():
    def entry(self,receiveRequest):
        # username = receiveRequest.get_argument('username')
        # pwd = receiveRequest.get_argument('pwd')
        # useremail=receiveRequest.get_argument('email','no have')
        username = ''
        pwd = ''
        useremail= ''
        imgpart=self.getUserPart()
        userRole='正常'
        result=self.judgeIsCanAdd(username,useremail)
        if result['status']==0:
            return result

        with db.execution_context():
            blogUser.create(**{"userName": username, "userPwd": pwd,"userEmail":useremail,
            "userImgPart":imgpart,"userRole":userRole,'userCollectionArticle':str([]),'userCollectionBlog':str([])})

            blogClassify.create(**{'userName':username,'belongPart':4,'classifyName':'默认',
                'createDate':datetime.today().date(),'articleNum':0})

        return {"status":1,"info":"注册成功"}


    def judgeIsCanAdd(self,username,useremail):
        getalluser=GetAllUser()
        if username in getalluser.getAllUserName():
            return {"status":0,'errorinfo':"该用户名已被注册"}

        if useremail in getalluser.getAllUserEmain():
            return {"status":0,'errorinfo':"该邮箱地址已被使用"}

        return {"status":1}


    def getUserPart(self):
        imgFile = ['ImgPart3', 'ImgPartOne', 'ImgSecond']
        return imgFile[random.randint(0, 2)]
