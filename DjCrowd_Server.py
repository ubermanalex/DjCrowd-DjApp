'''
Created on 12.06.2013

@author: Alex
'''

from libavg import *

class ListNode(DivNode):

    def __init__ (self, slist, scount, **kwargs):
        super(ListNode, self).__init__(**kwargs)
        self.slist  = slist 
        self.scount = scount 
        
        self.window = avg.DivNode(id="window", size=(self.size.x, len(slist)*20), pos =(0,0), parent= self)
        i = 0 
        p = 0 
        node = slist
        for string in slist:
            node[i] = WordsNode(id = str(i), text= str(string), color="FFFFFF", pos=(5,p), parent=self.window)
            node[i].setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click)
            node[i].setEventHandler(avg.CURSORUP , avg.MOUSE,  self.MouseUpOut)
            node[i].setEventHandler(avg.CURSOROUT , avg.MOUSE,  self.MouseUpOut)
            p = p+20
            i = i +1
            
        self.captureHolder = None
        self.dragOffsetY = 0
        self.setEventHandler(avg.CURSORDOWN, avg.MOUSE | avg.TOUCH, self.startScroll)
        self.setEventHandler(avg.CURSORMOTION, avg.MOUSE | avg.TOUCH, self.doScroll)
        self.setEventHandler(avg.CURSORUP, avg.MOUSE | avg.TOUCH, self.endScroll)
        self.setEventHandler(avg.CURSOROUT, avg.MOUSE | avg.TOUCH, self.outofDiv)
        self.SelectedString = ""
        self.node_old = 0
        self.timeid = None
        self.current_event = None
        
        #start = WordsNode(id="start", text="Liste 2", pos=(315,10), color="FFFFFF", parent=rcv.player.getRootNode())
        #start.setEventHandler(avg.CURSORUP, avg.MOUSE, self.updater)
     
        #entry =  WordsNode(id="entry", text="Take ", pos=(315,30), color="000000", parent=rcv.player.getRootNode())
        #entry.setEventHandler(avg.CURSORUP, avg.MOUSE, self.getSelectedEntryPrint)
    
    #def clicklong(self, event):
    #    self.timeid = rcv.player.setTimeout(2000,self.selectString)
    #    self.current_event = event
    
    def click(self, event):
        self.current_event = event 
        print ('hallo')
        
    def MouseUpOut(self,event):
        if self.timeid == None:
            pass
        else:
            rcv.player.clearInterval(self.timeid)

    def selectString(self):
        event = self.current_event
        self.SelectedString = event.node.text
        if (event.node.id != self.node_old):
            id = rcv.player.getElementByID(str(self.node_old))
            id.color = "555555"
            event.node.color = "000000"
        else:
            pass
        self.node_old = event.node.id
        rcv.player.clearInterval(self.timeid)
    
    def update(self, list):
        self.window.pos = avg.Point2D(0,0)
        self.SelectedString = ""
        id = rcv.player.getElementByID(str(self.node_old))
        id.color = "EE3B3B"
        i = 0
        lsl = len(self.slist)
        while i < len(self.slist):
            e = rcv.player.getElementByID(str(i))
            e.text = ""
            i = i + 1
        p = 0
        s = 0
        ii = 0
        node = list
        l1 = list[0:lsl-1]
        l2 = list[lsl:len(list)-1]
        if len(list) < lsl:
            for string in l1:
                e = rcv.player.getElementByID(str(ii))
                e.text = string
                ii = ii +1
                p = p+20
            while s < (lsl - len(list)):
                self.window.size = (avg.Point2D(self.window.size.x, self.window.size.y - 20))
                s = s+1
        elif len(list) > lsl:
            for string in l1:
                e = rcv.player.getElementByID(str(ii))
                e.text = string
                ii = ii +1
                p = p+20
            for string in l2:
                ii = ii +1
                node[ii] = WordsNode(id = str(ii), text= str(string), color="79CDCD", pos=(5,p), parent=self.window)
                node[ii].setEventHandler(avg.CURSORDOWN, avg.MOUSE, self.selectString)
                self.window.size = (avg.Point2D(self.window.size.x, self.window.size.y + 20))
                p = p+20
        else:
            for string in list:
                e = rcv.player.getElementByID(str(ii))
                e.text = string
                ii = ii +1
        self.slist = list
    
    def updater(self,event):
        self.update(["Lied01",
                     "Lied02","Lied03","Lied04","Lied05","Lied06","Lied07","Lied08",
                     "Lied09","Lied10","Lied11","Lied12","Lied13","Lied14","Lied15","Lied01",
                     "Lied02","Lied03","Lied04","Lied05","Lied06","Lied07","Lied08",
                     "Lied09","Lied10","Lied11","Lied12","Lied13","Lied14","Lied15"])
    def startScroll(self, event):
        if self.captureHolder is None:
            self.captureHolder = event.cursorid
            self.dragOffsetY = self.window.pos.y - event.pos.y
    
    def doScroll(self, event):
        if self.window.size.y > event.node.size.y:
            if event.cursorid == self.captureHolder:
                self.window.pos = avg.Point2D(self.window.pos.x, event.pos.y + self.dragOffsetY)
                
    def endScroll(self, event):
        if event.cursorid == self.captureHolder:
            self.captureHolder = None
        if self.window.pos.y >=  self.size.y -20:
                anim = avg.EaseInOutAnim(self.window, "y", 1000, self.window.pos.y, self.size.y -21, 50, 1000)
                anim.start()
        if self.window.pos.y + self.window.size.y - 20 <=  -1:
                anim = avg.EaseInOutAnim(self.window, "y", 1000, self.window.pos.y, 20 - self.window.size.y, 50, 1000)
                anim.start()
    
    def outofDiv(self, event):
        self.captureHolder = None
        if self.window.pos.y >=  self.size.y -20:
                anim = avg.EaseInOutAnim(self.window, "y", 1000, self.window.pos.y, self.size.y -21, 50, 1000)
                anim.start()
        if self.window.pos.y + self.window.size.y - 20 <=  -1:
                anim = avg.EaseInOutAnim(self.window, "y", 1000, self.window.pos.y, 20 - self.window.size.y, 50, 1000)
                anim.start()

    def getSelectedEntryPrint(self, event):
        print self.getSelectedEntry()
    
    def getSelectedEntry(self):
        if self.SelectedString == "":
            return "Kein String selektriert"
        else:
            return self.SelectedString
        
##USERDATABASE

class UserDatabase(object):

    def __init__(self):
        self.database = []

    def __getitem__(self, index):
        return self.database[index]
    
    def getlen(self):
        return len(self.database)
        
    def addUser(self, username, songtitle1, songtitle2, numberofpoints, numberofvotes):
        user = User(username, songtitle1, songtitle2, numberofpoints, numberofvotes)
        self.database.append(user)
        
    def getUserBySong(self, songtitle):
        result = ''
        for user in self.database:
            if (user.songtitle1 == songtitle) or (user.songtitle2 == songtitle):
                result = user.username
        return result
        
class User(object):
    def __init__(self, username, songtitle1, songtitle2, numberofpoints, numberofvotes):
        self.username = username
        self.songtitle1 = songtitle1
        self.songtitle2 = songtitle2
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
    
    def addSong(self, interpret, songtitle, numberofvotes):
        song = Song(interpret, songtitle, numberofvotes)
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
    def __init__(self, interpret, songtitle, numberofvotes):
        self.interpret = interpret
        self.songtitle = songtitle
        self.numberofvotes = numberofvotes
        
    def toStrI(self):
        return '{self.title} aus dem Album {self.album}; Laenge: {self.length}'.format(self=self)
    
    def toStrA(self):
        return 'Vom Interpreten {self.interpret} {self.title}; Laenge: {self.length}'.format(self=self)    


##SERVER


from libavg import avg,AVGApp
import sys,thread
 
from twisted.internet import reactor
from twisted.python import log
 
from autobahn.websocket import WebSocketServerFactory, \
                               WebSocketServerProtocol, \
                               listenWS

###THIS CLASS SIMPLY HOLDS THE CONNECTED CLIENT IPS####
class IPStorage():
    def __init__(self):
        self._ipList=dict({})
        
    def addNewClient(self,ip,connection): ##adds a new Client to the Dictionary
        self._ipList[ip]=connection 
    
    def dropConnection(self,ip):##removes Connection out of Dict
        del self._ipList[ip]
        
    def getAllCurrentConnections(self):#returns all currently active Connections
        return self._ipList
    
    def getConnectionForIp(self,ip):##returns a Connection to a Client with a certain IP
        return self._ipList[ip]
    
    def updateAll(self,msg): #sends Message to all connected Clients
        for key in self._ipList:
            self._ipList[key].sendMessage(msg)
        

###WEBSOCKETPROTOCOL USED FOR COMMUNICATION####
class EchoServerProtocol(WebSocketServerProtocol):
    
    def onClose(self,wasClean,code,reason):
        print "Client left"
        ips.dropConnection(self.peer.host) ##Drop Connection out of IPStorage when Client disconnects
        ips.updateAll("Client with IP "+self.peer.host+" has disconnected")#Update all
        
    def onOpen(self):
        ips.addNewClient(self.peer.host, self) ##adds current Connection and Client IP to the Storage
        ips.updateAll("New Client with IP "+self.peer.host+" has joined")
              
    def onMessage(self, msg, binary):
        print "sending echo:", msg ##print incoming message
        
        ##adds user
        
        if (msg[0:10] == 'USERNAME: '):
            oberegrenze = len(msg)
            userdb.addUser(msg[10:oberegrenze],'','',0,3)
            self.sendMessage('hallo', binary)##send back message to initiating client
            print (userdb[0].username+" "+userdb[0].songtitle1+" "+userdb[0].songtitle2+" "+str(userdb[0].numberofpoints)+" "+str(userdb[0].numberofvotes))
            
        ##adds song

        if (msg[0:6] == 'SONG: '):
            oberegrenze = len(msg)
            songelems = msg[6:oberegrenze].split('##')
            songdb.addSong(songelems[0],songelems[1],int(songelems[2]))
            self.sendMessage('##'.join(songelems), binary)##send back message to initiating client
            print songdb[0].interpret+" "+songdb[0].songtitle+" "+str(songdb[0].numberofvotes)

        
        ##applies vote
        
        if (msg[0:6] == 'VOTE: '):
            print('ye')
            oberegrenze = len(msg)
            userandsong = msg[6:oberegrenze].split('##')
            user = userandsong[0]
            song = userandsong[1]
            userdblen = userdb.getlen()
            songdblen = songdb.getlen()
            
            for i in range(0,userdblen):
                if (user == userdb[i].username):
                    if (userdb[i].numberofvotes == 0):
                        break ##TODO:BREAK SECOND LOOP##
                    userdb[i].numberofvotes -= 1
                    print str(userdb[i].numberofvotes)
                    break
            for i in range(0,songdblen):
                if (song == songdb[i].songtitle):
                    songdb[i].numberofvotes += 1
                    j = i-1
                    while j>=0: ##sorts songarray!
                        if (songdb[i].numberofvotes <= songdb[j].numberofvotes):
                            break
                        
                        songdb[j],songdb[i] = songdb[i],songdb[j]
                        j -= 1
                    break
            for i in range(0,songdblen):
                print songdb[i].interpret+" "+songdb[i].songtitle+" "+str(songdb[i].numberofvotes)
            for j in range(0,userdblen):
                print userdb[j].username+" "+userdb[j].songtitle1+" "+userdb[j].songtitle2+" "+str(userdb[j].numberofpoints)+" "+str(userdb[j].numberofvotes)

class libAvgAppWithRect (AVGApp): ##Main LibAVG App that uses WebSockets
    def __init__(self): ##Create one WordsNode for the Text and RectNode to send to a certain Client and set player, canvas,..
        self.player=avg.Player.get()
        self.canvas=self.player.createMainCanvas(size=(310,310))
        self.rootNode=self.canvas.getRootNode()

        self.rectadd = avg.RectNode(size=(250,30),pos=(30,125),parent=self.rootNode,color="2EFE2E",fillcolor="58FA58", fillopacity=1)
        self.rectrej1 = avg.RectNode(size=(250,30),pos=(30,170),parent=self.rootNode,color="FE9A2E",fillcolor="FAAC58", fillopacity=1)
        self.rectrej2 = avg.RectNode(size=(250,30),pos=(30,215),parent=self.rootNode,color="FE642E",fillcolor="FA8258", fillopacity=1)
        self.rectrej3 = avg.RectNode(size=(250,30),pos=(30,260),parent=self.rootNode,color="FE2E2E",fillcolor="FA5858", fillopacity=1)
        #self.currentsong = avg.WordsNode(pos=(50,155),parent=self.rootNode,fontsize=15,color="ffffff",text="Aktueller Vorschlag")
        #self.help = avg.WordsNode(pos=(130,180),parent=self.rootNode,fontsize=15,color="ffffff",text="Help")

        self.divadd = avg.DivNode(pos=(30,125),size=(250,30),parent=self.rootNode)
        self.divrej1 = avg.DivNode(pos=(30,170),size=(250,30),parent=self.rootNode)
        self.divrej2 = avg.DivNode(pos=(30,215),size=(250,30),parent=self.rootNode)
        self.divrej3 = avg.DivNode(pos=(30,260),size=(250,30),parent=self.rootNode)
        
        self.texadd =avg.WordsNode(pos=(10,5),parent=self.divadd,color="088A08",text="Vorschlag annehmen")
        self.textrej1 = avg.WordsNode(pos=(10,5),parent=self.divrej1,color="8A4B08",text="Doppelt")
        self.textrej2 = avg.WordsNode(pos=(10,5),parent=self.divrej2,color="8A2908",text="Nicht vorhanden")
        self.textrej3 = avg.WordsNode(pos=(10,5),parent=self.divrej3,color="8A0808",text="Passt nicht")
        #self.rectWhite=avg.RectNode(size=(200,200),pos=(200,140),parent=self.rootNode,color="ffffff",fillcolor="ffffff", fillopacity=1)
        #self.rectWhite.connectEventHandler(avg.CURSORDOWN, avg.MOUSE, self.rectWhite, self.onWhiteRectClick)
        #thread.start_new_thread(self.initializeWebSocket, ()) ##start the WebSocket in new Thread
        
            
    #def onWhiteRectClick(self,event):##send Message "Hello there" to First Client in IPStorage
    #   if (ips.getAllCurrentConnections()):
    #      ips.getAllCurrentConnections()[ips.getAllCurrentConnections().keys()[0]].sendMessage("Hello there")
        
            
    def initializeWebSocket(self):##Starts the WebSocket
        log.startLogging(sys.stdout)##Create a logfile (not necessary)
        self.factory = WebSocketServerFactory("ws://localhost:9023", debug = False)
        self.factory.protocol = EchoServerProtocol ##assign our Protocol to send/receive Messages
        listenWS(self.factory)
        reactor.run(installSignalHandlers=0)##"installSignalHandlers=0" Necessary for Multithreading
        
            
if __name__ == '__main__':
    rcv=libAvgAppWithRect()
    ips=IPStorage()
    songdb = SongDatabase()
    userdb = UserDatabase()
    requestlist = ListNode(["Testinterpret - Testsong"], 2, size=(300, 100), pos=(5, 5), crop=True, elementoutlinecolor="333333", parent=rcv.player.getRootNode())
    rcv.player.play()