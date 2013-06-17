'''
Created on 10 Jun 2013

@author: Alex
'''
##USERDATABASE

class UserDatabase(object):

    def __init__(self):
        self.database = []

    def __getitem__(self, index):
        return self.database[index]
    
    def getlen(self):
        return len(self.database)
        
    def addUser(self, userid, userip,username, numberofpoints, numberofvotes):
        user = User(userid, userip, username, SuggestedSong("LE##ER","LE##ER"), SuggestedSong("LE##ER","LE##ER"),numberofpoints, numberofvotes,[])
        self.database.append(user)
        
    def getUser(self, interpret, songtitle):
        for user in self.database:
            if user.song1.songtitle == songtitle and user.song1.interpret == interpret:
                return user
            if user.song2.songtitle == songtitle and user.song2.interpret == interpret:
                return user
        
class User(object):
    def __init__(self, userid, userip, username, song1, song2, numberofpoints, numberofvotes, votedfor):
        self.userid = userid
        self.username = username
        self.userip = userip
        self.numberofpoints = numberofpoints
        self.numberofvotes = numberofvotes
        self.song1 = song1
        self.song2 = song2
        self.votedfor = votedfor
        
class SuggestedSong(object):
    def __init__(self,interpret,songtitle):
        self.interpret = interpret
        self.songtitle = songtitle
        self.status = 0

##SONGDATABASE

class SongDatabase(object):

    def __init__(self):
        self.database = []
        self.topseven = []
        
    def __getitem__(self, index):
        return self.database[index]

    def getlen(self):
        return len(self.database)
    
    def addSong(self, interpret, songtitle, numberofvotes, fromuser):
        song = Song(interpret, songtitle, numberofvotes, fromuser)
        self.database.append(song)

        if len(self.topseven) < 7:
            self.topseven.append(song)
    
    def checktopseven (self,oldtopseven):
        if len(oldtopseven) != len(self.topseven):
            return True
        for song in oldtopseven:
            for pong in self.topseven:
                if song.interpret != pong.interpret or song.songtitle != pong.songtitle or song.numberofvotes != pong.numberofvotes:
                    return True              
        return False
    
    def tolist (self,songarray):
        strlist = []
        i = 1
        for song in songarray:
            strlist.append(str(i)+". "+str(song.interpret)+" / "+str(song.songtitle)+" / V:"+str(song.numberofvotes))
            i+=1
        while i <= 7:
            strlist.append(str(i)+". ")
            i+=1
        return strlist
    
    def getUser(self, interpret, songtitle):
        for song in self.database:
            if song.songtitle == songtitle and song.interpret == interpret:
                return song.fromuser

class Song(object):
    def __init__(self, interpret, songtitle, numberofvotes, fromuser):
        self.interpret = interpret
        self.songtitle = songtitle
        self.numberofvotes = numberofvotes
        self.fromuser = fromuser
        
    def toStr(self):
        return self.interpret+"##"+self.songtitle+"##"+self.numberofvotes
