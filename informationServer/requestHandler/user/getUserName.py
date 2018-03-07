from requestHandler.login.mySession import Session
from infoServerUrl import BLOGPART,BLOGREADROLE
class GetUserName():
    def entry(self,receiveRequest):
        mySession = Session(receiveRequest)
        username = mySession['getname']
        if username == None:
            return {'status':0,'part':BLOGPART[0:5],'readrole':BLOGREADROLE[0:2]}
        else:
            username=username.decode('utf-8')
            return {'status':1,'part':BLOGPART[0:5],'readrole':BLOGREADROLE[0:2],'username':username}
