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
        
    def addUser(self, userid, username, numberofpoints, numberofvotes):
        user = User(userid, username, numberofpoints, numberofvotes)
        self.database.append(user)
        
    #def getUserBySong(self, songtitle):
    #    result = ''
    #    for user in self.database:
    #        if (user.songtitle1 == songtitle) or (user.songtitle2 == songtitle):
    #            result = user.username
    #    return result
        
class User(object):
    def __init__(self, userid, username, numberofpoints, numberofvotes):
        self.userid = userid
        self.username = username
        self.numberofpoints = numberofpoints
        self.numberofvotes = numberofvotes        

##SONGDATABASE

class SongDatabase(object):

    def __init__(self):
        self.database = []
        
    def __getitem__(self, index):
        return self.database[index]

    def getlen(self):
        return len(self.database)
    
    def addSong(self, interpret, songtitle, numberofvotes, fromuser):
        song = Song(interpret, songtitle, numberofvotes, fromuser)
        self.database.append(song)
        
    def getUser(self, songtitle):
        result = ''
        for song in self.database:
            if song.songtitle == songtitle:
                result = song.fromuser
                break
        return 'WINNER: '+str(result)
    
    #def getSongsByAlbum(self, album):
    #    result = ''
    #    for song in self.database:
    #        if song.album == album: 
    #            result = result + song.toStrA() + '\n'
    #    return album +':\n' + result
    

class Song(object):
    def __init__(self, interpret, songtitle, numberofvotes, fromuser):
        self.interpret = interpret
        self.songtitle = songtitle
        self.numberofvotes = numberofvotes
        self.fromuser = fromuser
        
    def toStr(self):
        return self.interpret+"##"+self.songtitle+"##"+self.numberofvotes
    #def toStrA(self):
    #    return 'Vom Interpreten {self.interpret} {self.title}; Laenge: {self.length}'.format(self=self)    
