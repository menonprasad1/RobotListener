__author__ = 'Prasad'

import os
import sys
import time

class Constants():
    FILE_ALREADY_LOCKED=1
    FILE_SUCCESS_LOCKED=2


class RobotListener():
    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self,fileName):
        #Robot cannot accept a :, it interprets it as start of second arg, hence use ; which will be replaced here.
        self.fileName=fileName.replace(";",":",1)
        self.lockfileName="{0}.lock".format(self.fileName)
        self.fd=0
        self.delay=2

    def lockfile(self):
        try:
            self.fd=os.open(self.lockfileName,os.O_CREAT|os.O_EXCL|os.O_RDWR)
            return Constants.FILE_SUCCESS_LOCKED
        except OSError as o:
            #we except the control here when the file is already locked/created
            return Constants.FILE_ALREADY_LOCKED
        except :
            print sys.exc_info()
            print "File already locked"


    def releaselock(self):
        try:
            if(os.path.exists(self.lockfileName) and self.fd!=0):
                os.close(self.fd)
                os.unlink(self.lockfileName)
            else:
                print "Lock file doesn't exist"
        except:
            print sys.exc_info()


    def end_test(self,arg1,arg2):
        iteration=0
        timedout="FALSE"
        try:
            while(self.lockfile()!=Constants.FILE_SUCCESS_LOCKED):
                if iteration>5:
                    timedout="TRUE"
                    break
                iteration=iteration+1
                time.sleep(self.delay)
            if timedout=="FALSE":
                wFile=open(self.fileName,"a+")
                #wFile.writelines()
                wFile.writelines("NAME:{0},STATUS:{1}\n".format(arg2["longname"],arg2["status"]))
                self.releaselock()
        except:
            print sys.exc_info()


if __name__=="__main__":
    fileName="E;\\op9.txt"
    #ob=RobotListener(fileName)
    #ob.lockfile()
    #ob.releaselock()
    #ob1=RobotListener(fileName)
    #ob1.lockfile()
    #ob1.releaselock()

    #ob1=RobotListener(fileName)
    #ob2=RobotListener(fileName)
    #ob1.lockfile()
    #ob2.releaselock()
    #ob2.lockfile()

    ob1=RobotListener(fileName)
    ob1.end_test("prasad",{"longname":"prasad","status":"PASS"})