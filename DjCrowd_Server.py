'''
Created on 12.06.2013

@author: Alex
'''
import pdb
import sys,thread
from libavg import *
#import listnode
import databases
from twisted.internet import reactor
from twisted.python import log
from autobahn.websocket import WebSocketServerFactory, \
                               WebSocketServerProtocol, \
                               listenWS

global hostip
hostip = "ws://localhost:9034"

##LISTNODE
##TODO:Auslagern
##TODO:Timer
##TODO:Dj kann Lied editieren, wenn er es annimmt (Typos beheben etc)
                               
class ListNode(DivNode):

    def __init__ (self, idindex, slist, scount, **kwargs):
        super(ListNode, self).__init__(**kwargs)
        
        self.slist  = []
        
        for string in slist:
            self.slist.append(string)
         
        self.scount = scount
        
        self.window = avg.DivNode(id=listwindowid, size=(300, 20), pos =(0,0), parent= self)
        self.i = 0
        self.idindex = idindex
        self.p = 0 
        self.node = slist
        for string in slist:
            
            self.node[self.i] = WordsNode(id = str(self.idindex), text= str(string), color="FFFFFF", pos=(5,self.p), parent=self.window)
            self.node[self.i].setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click)
            self.p = self.p+20
            self.idindex = self.idindex+1
            self.i = self.i +1
            
            
        self.captureHolder = None
        self.dragOffsetY = 0
        self.setEventHandler(avg.CURSORDOWN, avg.MOUSE | avg.TOUCH, self.startScroll)
        self.setEventHandler(avg.CURSORMOTION, avg.MOUSE | avg.TOUCH, self.doScroll)
        self.setEventHandler(avg.CURSORUP, avg.MOUSE | avg.TOUCH, self.endScroll)
        self.setEventHandler(avg.CURSOROUT, avg.MOUSE | avg.TOUCH, self.outofDiv)
        self.SelectedString = ""
        self.node_old = idindex
        self.current_event = None
            
    def click(self, event):
        self.current_event = event
        self.selectString()
        
    def selectString(self):
        event = self.current_event
        if (event.node.id != self.node_old):
            
            if self.node_old >= 0:
                nodeid = rcv.player.getElementByID(str(self.node_old))      
                nodeid.color = "FFFFFF"
            
            if (int(event.node.id) < 5000):
            
                event.node.color = "F4FA58"
            
                rcv.rectadd.color="2EFE2E"
                rcv.rectrej1.color="FE9A2E"
                rcv.rectrej2.color="FE642E"
                rcv.rectrej3.color="FE2E2E"
                rcv.rectblockuser.color="FF0000"
                rcv.rectadd.fillcolor="58FA58"
                rcv.rectrej1.fillcolor="FAAC58"
                rcv.rectrej2.fillcolor="FA8258"
                rcv.rectrej3.fillcolor="FA5858"
                rcv.rectblockuser.fillcolor="FE2E2E"
                rcv.textadd.color="088A08"
                rcv.textrej1.color="8A4B08"
                rcv.textrej2.color="8A2908"
                rcv.textrej3.color="8A0808"
                rcv.textblockuser.color="8A0808"
                
            elif (int(event.node.id) == 5000):
                if len(songdb.topseven) == 0:
                    return 0
                
                event.node.color = "FF0000"
                
                rcv.rectsongplayed.fillcolor="FE2E2E"
                rcv.rectsongplayed.color="FF0000"
                rcv.textsongplayed.color="8A0808"
            else:
                rcv.rectsongplayed.fillcolor="BDBDBD"
                rcv.rectsongplayed.color="A4A4A4"
                rcv.textsongplayed.color="424242"
        
        else:
            pass
        
        
        self.node_old = event.node.id
        
        
        
    def addEle(self, elem):
        i = len(self.slist)
        
        self.node.append("")
        self.slist.append(elem)
        #pdb.set_trace()
        node =  WordsNode(id = str(self.idindex), text= str(elem), color="FFFFFF", pos=(5,self.p), parent=self.window)
        self.node[i] = node
        self.node[i].setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click)
        
        self.idindex+=1
        self.p = self.p+20
        
        self.window.size = (avg.Point2D(self.window.size.x, self.window.size.y + 20))
        
        
                      
    def removEle(self):
        
        if (rcv.rectadd.color=="A4A4A4"):
            return 0
        
        event = self.current_event
        e = rcv.player.getElementByID(str(event.node.id))
        counter = int(event.node.id)+1
        iterend = len(self.node)
        
        rettext = e.text
        
        self.node.remove(e)#remove
        self.window.removeChild(e)
        self.slist.remove(e.text)
        
        while counter < iterend:
            f = rcv.player.getElementByID(str(counter))
            
            (x,y) = f.pos
            y -= 20
            c = f.color
            t = f.text
        
            self.window.removeChild(f)
            self.node[counter-1] = WordsNode(id = str(counter-1), text= t, color=c, pos=(x,y), parent=self.window)
            self.node[counter-1].setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click)
            
            counter+= 1
            
        self.window.size = (avg.Point2D(self.window.size.x, self.window.size.y - 20))
            
        rcv.rectadd.color="A4A4A4"
        rcv.rectrej1.color="A4A4A4"
        rcv.rectrej2.color="A4A4A4"
        rcv.rectrej3.color="A4A4A4"
        rcv.rectblockuser.color="A4A4A4"
        rcv.rectadd.fillcolor="BDBDBD"
        rcv.rectrej1.fillcolor="BDBDBD"
        rcv.rectrej2.fillcolor="BDBDBD"
        rcv.rectrej3.fillcolor="BDBDBD"
        rcv.rectblockuser.fillcolor="BDBDBD"
        rcv.textadd.color="424242"
        rcv.textrej1.color="424242"
        rcv.textrej2.color="424242"
        rcv.textrej3.color="424242"
        rcv.textblockuser.color="424242"
        
        self.current_event = None
        if len(self.slist) == 0:
            self.node_old = -1
        else:
            self.node_old = 0
        self.p = self.p-20
        
        self.idindex -= 1
        
        return rettext
        
    def update(self, songlist, idindex):
        self.window.pos = avg.Point2D(0,0)
        i = 0
        idind = idindex
        lsl = len(self.slist)
        while i < len(self.slist):
            e = rcv.player.getElementByID(str(idind))
            e.text = ""
            i = i + 1
            idind += 1
        p = 0
        s = 0
        ii = 0
        iidind = idindex
        node = songlist
        l1 = songlist[0:lsl-1]
        l2 = songlist[lsl:len(songlist)-1]
        if len(songlist) < lsl:
            for string in l1:
                e = rcv.player.getElementByID(str(iidind))
                e.text = string
                ii = ii +1
                iidind += 1
                p = p+20
            while s < (lsl - len(songlist)):
                self.window.size = (avg.Point2D(self.window.size.x, self.window.size.y - 20))
                s = s+1
        elif len(songlist) > lsl:
            for string in l1:
                e = rcv.player.getElementByID(str(iidind))
                e.text = string
                ii = ii +1
                iidind += 1
                p = p+20
            for string in l2:
                ii = ii +1
                iidind += 1
                node[ii] = WordsNode(id = str(iidind), text= str(string), color="79CDCD", pos=(5,p), parent=self.window)
                node[ii].setEventHandler(avg.CURSORDOWN, avg.MOUSE, self.selectString)
                self.window.size = (avg.Point2D(self.window.size.x, self.window.size.y + 20))
                p = p+20
        else:
            for string in songlist:
                e = rcv.player.getElementByID(str(iidind))
                e.text = string
                ii = ii +1
                iidind += 1
        self.slist = songlist

    
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



##SERVER

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
        print "received:", msg ##print incoming message
                    
        ##adds user
        
        if (msg[0:10] == 'USERNAME: '):
            oberegrenze = len(msg)
            usern = msg[10:oberegrenze]
            for user in userdb:
                if user.username.upper() == usern.upper():
                    self.sendMessage('NAMUSED')
                    return 0
            self.sendMessage('NAMFREE')
            userdb.addUser(userdb.getlen(),self.peer.host,msg[10:oberegrenze],0,3)
            #userstr = ('ID: '+str(userdb[userdb.getlen()-1].userid)+'\n'+
            #       'NAME: '+str(userdb[userdb.getlen()-1].username)+'\n'+
            #       'SONG1: '+str(userdb[userdb.getlen()-1].song1.interpret)+" - "+str(userdb[userdb.getlen()-1].song1.songtitle)+
            #       str(userdb[userdb.getlen()-1].song1.status)+'\n'+
            #       'SONG2: '+str(userdb[userdb.getlen()-1].song2.interpret)+" - "+str(userdb[userdb.getlen()-1].song2.songtitle)+
            #       str(userdb[userdb.getlen()-1].song2.status)+'\n'+
            #       'POINTS: '+str(userdb[userdb.getlen()-1].numberofpoints)+'\n'+
            #       'VOTES: '+str(userdb[userdb.getlen()-1].numberofvotes))
            #self.sendMessage(userstr, binary)##send back message to initiating client
            #print(userstr)
            
        ##adds song

        if (msg[0:6] == 'SONG: '):
            oberegrenze = len(msg)
            songelems = msg[6:oberegrenze].split('##')
            interpret = songelems[0]
            songtitle = songelems[1]
            
            testinterpret = interpret.upper()
            testsongtitle = songtitle.upper()
            
            
            #check if song already in songdb or requestlist
            for song in songdb.database:
                interp = song.interpret.upper()
                songtit = song.songtitle.upper()
                if interp == testinterpret and testsongtitle == songtit:
                    push = "SONGIND"+song.interpret+" - "+song.songtitle
                    self.sendMessage(str(push))
                    return 0
                
            for song in requestlist.slist:
                intandtit = song.split(' / ')
                interp = intandtit[0].upper()
                songtit = intandtit[1].upper()
                if interp == testinterpret and testsongtitle == songtit:
                    push = "SONGINP"+intandtit[0]+" - "+intandtit[1]
                    self.sendMessage(str(push))
                    return 0
            
            for userobj in userdb:
                if (userobj.username == songelems[2]):
                    #print userobj.userid
                    if (userobj.song1.interpret == "LE##ER"):
                        #print ("CHANGE s1")
                        userobj.song1.interpret = interpret
                        userobj.song1.songtitle = songtitle
                        userobj.song1.status = 0
                    elif (userobj.song2.interpret == "LE##ER"):
                        userobj.song2.interpret = interpret
                        userobj.song2.songtitle = songtitle
                        userobj.song2.status = 0
                        #print ("CHANGE s2")
                    else:
                        self.sendMessage('MAXSONG')
                        return 0

            #userstr = ('ID: '+str(userdb[userdb.getlen()-1].userid)+'\n'+
            #       'NAME: '+str(userdb[userdb.getlen()-1].username)+'\n'+
            #       'SONG1: '+str(userdb[userdb.getlen()-1].song1.interpret)+" - "+str(userdb[userdb.getlen()-1].song1.songtitle)+
            #       str(userdb[userdb.getlen()-1].song1.status)+'\n'+
            #       'SONG2: '+str(userdb[userdb.getlen()-1].song2.interpret)+" - "+str(userdb[userdb.getlen()-1].song2.songtitle)+
            #       str(userdb[userdb.getlen()-1].song2.status)+'\n'+
            #       'POINTS: '+str(userdb[userdb.getlen()-1].numberofpoints)+'\n'+
            #       'VOTES: '+str(userdb[userdb.getlen()-1].numberofvotes))
            #print(userstr)
            

            rcv.player.setTimeout(0, lambda : requestlist.addEle(interpret+" / "+songtitle))
            
        ##applies vote
        
        if (msg[0:6] == 'VOTE: '):
            oberegrenze = len(msg)
            userandsong = msg[6:oberegrenze].split('##')
            user = userandsong[0]
            interpret = userandsong[1]
            songtitle = userandsong[2]
            
            userdblen = userdb.getlen()
            songdblen = songdb.getlen()
            
            for i in range(0,userdblen):
                if (user == userdb[i].username):
                    if (userdb[i].numberofvotes == 0):
                        self.sendMessage('MAXVOTE')
                        return 0
                    userdb[i].numberofvotes -= 1
                    userdb[i].votedfor.append(interpret+'##'+songtitle)
                    #print ('USERVOTES: '+str(userdb[i].numberofvotes))
                    break
            for i in range(0,songdblen):
                if (songtitle == songdb[i].songtitle and interpret == songdb[i].interpret):
                    songdb[i].numberofvotes += 1
                    j = i-1
                    while j>=0: ##sorts songarray!
                        if (songdb[i].numberofvotes <= songdb[j].numberofvotes):
                            break

                        songdb[j].interpret,songdb[i].interpret = songdb[i].interpret,songdb[j].interpret
                        songdb[j].songtitle,songdb[i].songtitle = songdb[i].songtitle,songdb[j].songtitle
                        songdb[j].numberofvotes,songdb[i].numberofvotes = songdb[i].numberofvotes,songdb[j].numberofvotes
                        songdb[j].fromuser,songdb[i].fromuser = songdb[i].fromuser,songdb[j].fromuser

                        j -= 1
                    break
                
            #TODO: Neue SongDB an alle Clients schicken
            
            topsevenold = []
            for song in topsevenold:
                topsevenold.append(song)
            if (songdb.checktopseven(topsevenold)):
                    #TODO:songdb.topseven an Python-Client schicken
                    topseven.update(songdb.tolist(songdb.topseven),5000)
                
                
            #print('Interpret: '+str(songdb[0].interpret)+'\n'+
            #      'Songtitel: '+str(songdb[0].songtitle)+'\n'+
            #      'Voteanzahl: '+str(songdb[0].numberofvotes)+'\n'+
            #      'Von User: '+str(songdb[0].fromuser))

            
class libAvgAppWithRect (AVGApp): ##Main LibAVG App that uses WebSockets
    
    def confirm2(self):
        print "yo"
        check = raw_input("Zur Bestaetigung DjCrowd eingeben")
        if check != 'DjCrowd':
            return 5
        return 10
    
    def confirm(self, check):
            #check = raw_input("Zum Bestaetigen DjCrowd eingeben:")
            if check != 500:
                print "yo"
                return 0
            text = requestlist.removEle()
            newsong = text.split(' / ')
            interpret = newsong[0]
            songtitle = newsong[1]
            user = userdb.getUser(interpret,songtitle)
            print user.username, "blockiert."
            user.song1.interpret = "BLO##CKED"
            user.song1.songtitle = "BLO##CKED"
            user.song2.interpret = "BLO##CKED"
            user.song2.songtitle = "BLO##CKED"
        
            
    def click3(self,events):
            #thread.start_new_thread(self.confirm,(500,))
            #return 0
            if (rcv.rectadd.color=="A4A4A4"):
                return 0
            text = requestlist.removEle()
            newsong = text.split(' / ')
            interpret = newsong[0]
            songtitle = newsong[1]
            user = userdb.getUser(interpret,songtitle)
            receiver = user.userip
            print user.username, "blockiert."
            #TODO:PUNKTE LÖSCHEN??
            user.song1.interpret = "BLO##CKED"
            user.song1.songtitle = "BLO##CKED"
            user.song2.interpret = "BLO##CKED"
            user.song2.songtitle = "BLO##CKED"
            push = "SONGBLO"+interpret+" - "+songtitle
            ips.getConnectionForIp(receiver).sendMessage(str(push))
                
        
    def click2(self,events):    
            if (rcv.rectsongplayed.color=="A4A4A4"):
                return 0
            #self.x = 0
            #self.x = thread.start_new_thread(self.confirm2,())
            #TODO:Validierung, bei 'Song gespielt'-Klick
            #check = raw_input("Bestaetige mit 'DjCrowd'")
            #if check != "DjCrowd":
            #    return 0
            #while self.x == 0:
            #    pass
            #if self.x == 5:
            #    return 0
            interpret = songdb[0].interpret
            songtitle = songdb[0].songtitle
            numberofvotes = songdb[0].numberofvotes
            fromuser = songdb[0].fromuser
            song = interpret+'##'+songtitle
            
            songdb.topseven.remove(songdb[0])
            songdb.database.remove(songdb[0])
            songdb.addSong(interpret,songtitle,0,fromuser)
            topseven.update(songdb.tolist(songdb.topseven),5000)    
            
            for user in userdb:
                if fromuser == user.userid:
                    user.numberofpoints += numberofvotes * 10
                while True:
                    #print user.votedfor
                    if song in user.votedfor:
                        user.votedfor.remove(song)
                        user.numberofpoints += 10
                    else:
                        break
                    
            for user in userdb:
                print user.username, user.numberofpoints
            
    def click(self,events):
            
            if (rcv.rectadd.color=="A4A4A4"):
                return 0
            text = requestlist.removEle()
            eventid = (events.node.id)
            newsong = text.split(' / ')
            interpret = newsong[0]
            songtitle = newsong[1]
            user = userdb.getUser(interpret,songtitle)
            receiver = user.userip
                
            if eventid == "add":
                print('Hinzugefuegt: '+text)
                newsong = text.split(' / ')
                
                if (user.song1.status == 0 and user.song1.interpret == interpret and user.song1.songtitle == songtitle):
                    user.song1.interpret = interpret
                    user.song1.songtitle = songtitle
                    user.song1.status = 1
                elif (user.song2.status == 0 and user.song2.interpret == interpret and user.song2.songtitle == songtitle):
                    user.song2.interpret = interpret
                    user.song2.songtitle = songtitle
                    user.song2.status = 1
                else:
                    return 0
                
                #userstr = ('ID: '+str(userdb[userdb.getlen()-1].userid)+'\n'+
                #   'NAME: '+str(userdb[userdb.getlen()-1].username)+'\n'+
                #   'SONG1: '+str(userdb[userdb.getlen()-1].song1.interpret)+" - "+str(userdb[userdb.getlen()-1].song1.songtitle)+
                #   str(userdb[userdb.getlen()-1].song1.status)+'\n'+
                #   'SONG2: '+str(userdb[userdb.getlen()-1].song2.interpret)+" - "+str(userdb[userdb.getlen()-1].song2.songtitle)+
                #   str(userdb[userdb.getlen()-1].song2.status)+'\n'+
                #   'POINTS: '+str(userdb[userdb.getlen()-1].numberofpoints)+'\n'+
                #   'VOTES: '+str(userdb[userdb.getlen()-1].numberofvotes))
                #print(userstr)
            
                topsevenold = []
                for song in topsevenold:
                    topsevenold.append(song)
                songdb.addSong(interpret,songtitle,0,user.userid)
                if (songdb.checktopseven(topsevenold)):
                    topseven.update(songdb.tolist(songdb.topseven),5000)
                push = "SONGADD"+interpret+" - "+songtitle
                ips.getConnectionForIp(receiver).sendMessage(str(push))
                #print('Interpret: '+str(songdb[songdb.getlen()-1].interpret)+'\n'+
                #      'Songtitel: '+str(songdb[songdb.getlen()-1].songtitle)+'\n'+
                #      'Voteanzahl: '+str(songdb[songdb.getlen()-1].numberofvotes)+'\n'+
                #      'Von User: '+str(songdb[songdb.getlen()-1].fromuser))
                
            elif eventid == "rej1":
                print('Abgelehnt (doppelt): '+text)
                usersong = text.split(' / ')
                userrej = userdb.getUser(usersong[0],usersong[1])
                if userrej.song1.interpret == usersong[0] and userrej.song1.songtitle == usersong[1] and userrej.song1.status == 0:
                    userrej.song1.interpret = 'LE##ER'
                    userrej.song1.songtitle = 'LE##ER'
                if userrej.song2.interpret == usersong[0] and userrej.song2.songtitle == usersong[1] and userrej.song2.status == 0:
                    userrej.song2.interpret = 'LE##ER'
                    userrej.song2.songtitle = 'LE##ER'
    
                push = "SONGRE1"+interpret+" - "+songtitle
                ips.getConnectionForIp(receiver).sendMessage(str(push))
                
            elif eventid == "rej2":
                print('Abgelehnt (nicht vorh.): '+text)
                usersong = text.split(' / ')
                userrej = userdb.getUser(usersong[0],usersong[1])
                if userrej.song1.interpret == usersong[0] and userrej.song1.songtitle == usersong[1] and userrej.song1.status == 0:
                    userrej.song1.interpret = 'LE##ER'
                    userrej.song1.songtitle = 'LE##ER'
                if userrej.song2.interpret == usersong[0] and userrej.song2.songtitle == usersong[1] and userrej.song2.status == 0:
                    userrej.song2.interpret = 'LE##ER'
                    userrej.song2.songtitle = 'LE##ER'
                print user

                push = "SONGRE2"+interpret+" - "+songtitle
                ips.getConnectionForIp(receiver).sendMessage(str(push))

            
            elif eventid == "rej3":
                print('Abgelehnt (unpassend): '+text)
                usersong = text.split(' / ')
                userrej = userdb.getUser(usersong[0],usersong[1])
                print userrej.song1.interpret, userrej.song1.songtitle
                print userrej.song2.interpret, userrej.song2.songtitle
                if userrej.song1.interpret == usersong[0] and userrej.song1.songtitle == usersong[1] and userrej.song1.status == 0:
                    userrej.song1.interpret = 'LE##ER'
                    userrej.song1.songtitle = 'LE##ER'
                if userrej.song2.interpret == usersong[0] and userrej.song2.songtitle == usersong[1] and userrej.song2.status == 0:
                    userrej.song2.interpret = 'LE##ER'
                    userrej.song2.songtitle = 'LE##ER'
                print userrej.song1.interpret, userrej.song1.songtitle
                print userrej.song2.interpret, userrej.song2.songtitle
                
                push = "SONGRE3"+interpret+" - "+songtitle
                ips.getConnectionForIp(receiver).sendMessage(str(push))
                
    
    def __init__(self): ##Create one WordsNode for the Text and RectNode to send to a certain Client and set player, canvas,..
        self.player=avg.Player.get()
        self.canvas=self.player.createMainCanvas(size=(620,350))
        self.rootNode=self.canvas.getRootNode()

        self.rectadd = avg.RectNode(size=(250,30),pos=(30,125),parent=self.rootNode,color="A4A4A4",fillcolor="BDBDBD", fillopacity=1)
        self.rectrej1 = avg.RectNode(size=(250,30),pos=(30,170),parent=self.rootNode,color="A4A4A4",fillcolor="BDBDBD", fillopacity=1)
        self.rectrej2 = avg.RectNode(size=(250,30),pos=(30,215),parent=self.rootNode,color="A4A4A4",fillcolor="BDBDBD", fillopacity=1)
        self.rectrej3 = avg.RectNode(size=(250,30),pos=(30,260),parent=self.rootNode,color="A4A4A4",fillcolor="BDBDBD", fillopacity=1)
        self.rectblockuser = avg.RectNode(size=(250,30),pos=(30,305),parent=self.rootNode,color="A4A4A4",fillcolor="BDBDBD", fillopacity=1)

        self.divadd = avg.DivNode(id = "add",pos=(30,125),size=(250,30),parent=self.rootNode)
        self.divrej1 = avg.DivNode(id = "rej1",pos=(30,170),size=(250,30),parent=self.rootNode)
        self.divrej2 = avg.DivNode(id = "rej2",pos=(30,215),size=(250,30),parent=self.rootNode)
        self.divrej3 = avg.DivNode(id = "rej3",pos=(30,260),size=(250,30),parent=self.rootNode)
        self.divblockuser = avg.DivNode(id = "blockuser",pos=(30,305),size=(250,30),parent=self.rootNode)
        
        self.divadd.setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click)
        self.divrej1.setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click)
        self.divrej2.setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click)
        self.divrej3.setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click)
        self.divblockuser.setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click3)
        
        self.textadd =avg.WordsNode(pos=(10,5),parent=self.divadd,color="424242",text="Vorschlag annehmen")
        self.textrej1 = avg.WordsNode(pos=(10,5),parent=self.divrej1,color="424242",text="Doppelt")
        self.textrej2 = avg.WordsNode(pos=(10,5),parent=self.divrej2,color="424242",text="Nicht vorhanden")
        self.textrej3 = avg.WordsNode(pos=(10,5),parent=self.divrej3,color="424242",text="Passt nicht")
        self.textblockuser = avg.WordsNode(pos=(10,5),parent=self.divblockuser,color="424242",text="User blockieren")


        self.divsongplayed = avg.DivNode(id = "songplayed",pos=(340,170),size=(250,30),parent=self.rootNode)
        self.rectsongplayed = avg.RectNode(size=(250,30),pos=(0,0),parent=self.divsongplayed,color="A4A4A4",fillcolor="BDBDBD", fillopacity=1)
        self.textsongplayed =avg.WordsNode(pos=(10,5),parent=self.divsongplayed,color="424242",text="Song wurde gespielt")
        self.divsongplayed.setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click2)
        

        thread.start_new_thread(self.initializeWebSocket, ()) ##start the WebSocket in new Thread        
                      
    def initializeWebSocket(self):##Starts the WebSocket
        log.startLogging(sys.stdout)##Create a logfile (not necessary)
        self.factory = WebSocketServerFactory(hostip, debug = False)
        self.factory.protocol = EchoServerProtocol ##assign our Protocol to send/receive Messages
        listenWS(self.factory)
        
        reactor.run(installSignalHandlers=0)##"installSignalHandlers=0" Necessary for Multithreading

             
         
if __name__ == '__main__':
    rcv=libAvgAppWithRect()
    ips=IPStorage()
    songdb = databases.SongDatabase()
    userdb = databases.UserDatabase()
    
    listwindowid = "window"
    requestlist = ListNode(0, [], 2, size=(300, 100), pos=(5, 5), crop=True, elementoutlinecolor="333333", parent=rcv.player.getRootNode())
    
    listwindowid = "window2"
    topseven = ListNode(5000, ["1."], 2, size=(300, 140), pos=(315, 5), crop=True, elementoutlinecolor="333333", parent=rcv.player.getRootNode())
    topseven.addEle("2.")
    topseven.addEle("3.")
    topseven.addEle("4.")
    topseven.addEle("5.")
    topseven.addEle("6.")
    topseven.addEle("7.")
    
    rcv.player.play()