from infoOrm import *
from requestHandler.login.mySession import Session
from requestHandler.user.addOneUser import AddOneUser
'''
请求数据格式：
{
    'username':name,
    'pwd':pwd
}

'''
class UserLogin():
    def entry(self,receiveRequest):
        username=receiveRequest.get_argument('username','nohave')
        pwd=receiveRequest.get_argument('pwd','null')
        AddOneUser().entry('firstadd')
        return self.judge(receiveRequest,username,pwd)

    def judge(self,receiveRequest,username,pwd):
        try:
            nowuser = MyBaseModel.returnList(blogUser.select().where(blogUser.userName==username))
            if len(nowuser) > 0:
                if nowuser[0]['userPwd'] == pwd:

                    my_session = Session(receiveRequest)
                    session_id = my_session.getSessionId()
                    my_session['name'] = username
                    logger.info('用户：%s 登录' % username)
                    return {"status": 1,'session_id': session_id,'username':username}
                else:
                    logger.info('用户：%s 登录失败，原因：密码错误' % username)
                    return {"status": 0, "errorInfo": "密码错误"}

            else:
                logger.info('用户：%s 登录失败，原因：该用户不存在' % username)
                return {"status": 0, "errorInfo": "该用户名不存在"}
        except:
            raise