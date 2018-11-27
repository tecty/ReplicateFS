#!/usr/bin/env python 
import time

S_RUNNING = 1
S_LOCKED = 2
S_FLUSH = 3
S_COMMIT = 4 
S_FINISHED = 5

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
        self.state = S_RUNNING
        self.ops = ops 
        self.data = data 

    def toLocked(self):
        self.state = S_LOCKED

    def toFlush(self):
        self.state = S_FLUSH

    def toCommit(self):
        self.state = S_COMMIT

    def toFinished(self):
        self.state = S_FINISHED


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
        while j.state != S_COMMIT:
            time.sleep(5)
        j.toFinished()
        return j

    def getAllJournal(self):
        return self.journalDict