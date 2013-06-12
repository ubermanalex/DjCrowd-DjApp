'''
Created on May 1, 2013

@author: Steffi
'''

class SongDatabase(object):

    def __init__(self):
        self.database = []
        
    def addSong(self, interpret, title, album, length):
        song = Song(interpret, title, album, length)
        self.database.append(song)
        
    def getSongsByInterpret(self, interpret):
        result = ''
        for song in self.database:
            if song.interpret == interpret:
                result = result + song.toStrI() + '\n'
        return interpret + ':\n' + result
    
    def getSongsByAlbum(self, album):
        result = ''
        for song in self.database:
            if song.album == album: 
                result = result + song.toStrA() + '\n'
        return album +':\n' + result
    

class Song(object):
    def __init__(self, interpret, title, album, length):
        self.interpret = interpret
        self.title = title
        self.album = album
        self.length = length
    
    def toStrI(self):
        return '{self.title} aus dem Album {self.album}; Laenge: {self.length}'.format(self=self)
    
    def toStrA(self):
        return 'Vom Interpreten {self.interpret} {self.title}; Laenge: {self.length}'.format(self=self)


def main():
    sDB = SongDatabase()
    sDB.addSong("M. Jackson", "Billy Jean", "Bad", "3:25")
    sDB.addSong("M. Jackson", "Heal the world", "Earth", "4:13")
    print(sDB.getSongsByInterpret("M. Jackson"))
    print(sDB.getSongsByAlbum("Bad"))
    
if __name__ == "__main__":
    main()