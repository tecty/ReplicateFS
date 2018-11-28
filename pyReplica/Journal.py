#!/usr/bin/env python 
import time
import json 
import Constants

def doJournal(journal,mount_path):
    '''
    act according to the operation type 
    do the operation to disk 
    '''
    journal.toFlush()
    # do the opertion 
    journal.toCommit()
    return True


class Journal(object):
    def __init__(self, ops, data):
        self.state = Constants.S_RUNNING
        self.ops = ops 
        # get the correspond callback 
        self.data = data 
        self.res =""

    def toLocked(self):
        self.state = Constants.S_LOCKED

    def toFlush(self):
        self.state = Constants.S_FLUSH
        # do the callback and store the result in some where 
        # self.res = self.callback(self.data)
        # callback is finished 
        self.toCommit()

    def toCommit(self):
        self.state = Constants.S_COMMIT

    def toFinished(self):
        self.state = Constants.S_FINISHED
        # return back the callback's result 
        return self.res

    def toJson(self):
        json.dumps({
            'ops':self.ops,
            'data': self.data
        })
        

class JournalController(object):
    def __init__(self, mount_path):
        self.idMax = 0
        self.journalDict = {}
        self.mount_path = mount_path
    def getJournal(self, id ):
        return self.journalDict[id]
    

    def canCommit(self):

        return True

    def createJournal(self, ops, data):
        j = Journal(ops, data)
        self.journalDict[self.idMax] = j 
        self.idMax +=1 
        doJournal(j, self.mount_path)
        return j 

    def doCommit(self, id):
        j = self.journalDict[id]
        # commit finished 
        # lock, wait the Tr to finish
        while j.state != Constants.S_COMMIT:
            time.sleep(5)
        j.toFinished()
        return j

    def getAllJournal(self):
        return self.journalDict