#!/usr/bin/env python 


S_RUNNING = 1
S_LOCKED = 2
S_FLUSH = 3
S_COMMIT = 4 
S_FINISHED = 5

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
    def __init__(self):
        self.idMax = 0
        self.journalDict = {}
    def getJournal(self, id ):
        return self.journalDict[id]
    
    def createJournal(self, ops, data):
        self.journalDict[self.idMax] = Journal(ops, data)
        self.idMax +=1 

    def getAllJournal(self):
        return self.journalDict