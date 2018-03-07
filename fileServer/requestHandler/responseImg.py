import os
from fileLogConfig import filelogger,errorMessage
class ResponseImg():
    def entry(self,*args):
        dirpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        try:
            filepath=dirpath+'/saveImgFile/'+args[0]+'/'+args[1]+'/'+args[2]

            with open(filepath,'rb') as f:
                img=f.read()
            return img
        except Exception as e:
            filelogger.warning(errorMessage(e))
            filepath=dirpath+'/saveImgFile/nofind.jpg'
            with open(filepath,'rb') as f:
                img=f.read()
            return img

