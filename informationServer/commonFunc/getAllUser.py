from infoOrm import *

class GetAllUser():
    def __init__(self):
        self.users=MyBaseModel.returnList(blogUser.select(blogUser.userName,blogUser.userEmail))

    def getAllUserName(self):
        usersname=[]
        for user in self.users:
            usersname.append(user['userName'])

        return usersname


    def getAllUserEmain(self):
        usersemail=[]
        for user in self.users:
            usersemail.append(user['userEmail'])

        return usersemail