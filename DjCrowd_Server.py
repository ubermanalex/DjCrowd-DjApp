'''
Created on 12.06.2013

@author: Alex
'''
import pdb
import sys,thread
import time
from libavg import *
#import listnode
import databases
from twisted.internet import reactor
from twisted.python import log
from autobahn.websocket import WebSocketServerFactory, \
                               WebSocketServerProtocol, \
                               listenWS

global hostip, pysend, pysend2, pyclient
hostip = "ws://localhost:9034"

##LISTNODE
##TODO:Auslagern
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
        self.dragOffsetX = 0
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
                
#             elif (int(event.node.id) == 5000):
#                 if len(songdb.topseven) == 0:
#                     return 0
#                 
#                 event.node.color = "FF0000"
#                 
#                 rcv.rectsongplayed.fillcolor="FE2E2E"
#                 rcv.rectsongplayed.color="FF0000"
#                 rcv.textsongplayed.color="8A0808"
#             else:
#                 rcv.rectsongplayed.fillcolor="BDBDBD"
#                 rcv.rectsongplayed.color="A4A4A4"
#                 rcv.textsongplayed.color="424242"
        
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
            #TODO: horizontal scrollbar
            self.dragOffsetX = self.window.pos.x - event.pos.x
    
    
    
    def doScroll(self, event):
        if self.window.size.y > event.node.size.y:
            if event.cursorid == self.captureHolder:
                self.window.pos = avg.Point2D(self.window.pos.x, event.pos.y + self.dragOffsetY)
        #TODO: horizontal scrollbar
        if self.window.size.x > event.node.size.x:
            if event.cursorid == self.captureHolder:
                self.window.pos = avg.Point2D(event.pos.x + self.dragOffsetX, self.window.pos.y)
    
    
                
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
        for user in userdb:
            if self.peer.host == user.userip:
                self.sendMessage("USEREXI"+user.username)
                self.sendMessage("ACTVOTE"+str(user.numberofvotes))
                if user.song1.interpret == "LE##ER" and user.song2.interpret == "LE##ER":
                    x = 2
                elif user.song1.interpret == "LE##ER" or user.song2.interpret == "LE##ER":
                    x = 1
                else:
                    x = 0
                self.sendMessage("ACTSUGG"+str(x))
                self.sendMessage("POINTCO"+str(user.numberofpoints))
                return 0
        ips.addNewClient(self.peer.host, self) ##adds current Connection and Client IP to the Storage
        ips.updateAll("New Client with IP "+self.peer.host+" has joined")
        
    def onMessage(self, msg, binary):
        print "received:", msg ##print incoming message
                    
        ##adds user
        
        #TODO:PYCLIENT IP
        if (msg[0:10] == 'PYCLIENT: '):
            msglen = len(msg)
            global pyclient
            pyclient = self.peer.host
            
        if (msg[0:10] == 'USERNAME: '):
            msglen = len(msg)
            usern = msg[10:msglen]
            for user in userdb:
                if user.username.upper() == usern.upper():
                    self.sendMessage('NAMUSED')
                    return 0
            self.sendMessage('NAMFREE')
            userdb.addUser(userdb.getlen(),self.peer.host,msg[10:msglen],0,3)
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
            msglen = len(msg)
            songelems = msg[6:msglen].split('##')
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
            
            for song in rejdb.database:
                interp = song.interpret.upper()
                songtit = song.songtitle.upper()
                if interp == testinterpret and testsongtitle == songtit:
                    push = "SONGINR"+song.interpret+" - "+song.songtitle
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
                        if (userobj.song2.interpret == "LE##ER"):
                            self.sendMessage('ACTSUGG1')
                        else:
                            self.sendMessage('ACTSUGG0')
                    elif (userobj.song2.interpret == "LE##ER"):
                        userobj.song2.interpret = interpret
                        userobj.song2.songtitle = songtitle
                        userobj.song2.status = 0
                        if (userobj.song1.interpret == "LE##ER"):
                            self.sendMessage('ACTSUGG1')
                        else:
                            self.sendMessage('ACTSUGG0')
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
            msglen = len(msg)
            userandsong = msg[6:msglen].split('##')
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
                    x = True
                    for song in songdb:
                        if song.interpret == interpret and song.songtitle == songtitle:
                            x = False
                            break
                    if x:
                        return 0
                    userdb[i].numberofvotes -= 1
                    self.sendMessage('ACTVOTE'+str(userdb[i].numberofvotes))
                    userdb[i].votedfor.append(interpret+'##'+songtitle)
                    #print ('USERVOTES: '+str(userdb[i].numberofvotes))
                    break
            for i in range(0,songdblen):
                if (songtitle == songdb[i].songtitle and interpret == songdb[i].interpret):
                    songdb[i].numberofvotes += 1
                    j = i-1
                    k = i
                    while j>=0: ##sorts songarray!
                        if (songdb[k].numberofvotes <= songdb[j].numberofvotes):
                            break
                        songdb[j].interpret,songdb[k].interpret = songdb[k].interpret,songdb[j].interpret
                        songdb[j].songtitle,songdb[k].songtitle = songdb[k].songtitle,songdb[j].songtitle
                        songdb[j].numberofvotes,songdb[k].numberofvotes = songdb[k].numberofvotes,songdb[j].numberofvotes
                        songdb[j].fromuser,songdb[k].fromuser = songdb[k].fromuser,songdb[j].fromuser
                        
                        j -= 1
                        k -= 1
                    break
                
            #TODO: Neue SongDB an alle Clients schicken
            
            topseven.update(songdb.tolist(songdb.topseven),5000)
            x = songdb.tolist(songdb.topseven)
            global pysend
            pysend = ""
            for y in x:
                a = y.split(' / ')
                if len(a)==1:
                    pysend+=' ## ##0!#!'
                else:
                    pysend += (a[0])[3:len(a[0])]+'##'+(a[1])+'##'+(a[2])[2:len(a[2])]+'!#!'
                        
            pysend = pysend[0:len(pysend)-3]
                       
            print pysend
            #print('Interpret: '+str(songdb[0].interpret)+'\n'+
            #      'Songtitel: '+str(songdb[0].songtitle)+'\n'+
            #      'Voteanzahl: '+str(songdb[0].numberofvotes)+'\n'+
            #      'Von User: '+str(songdb[0].fromuser))

            
class libAvgAppWithRect (AVGApp): ##Main LibAVG App that uses WebSockets
    
    def sendtopy(self):
        time.sleep(30)  #updates top7 on screen every 30sec
        #global pysend,pysend2
        #TODO:PYSEND
        #ips.getConnectionForIp(pyclient).sendMessaage(pysend)
        #ips.getConnectionForIp(pyclient).sendMessaage(pysend2)
        print pysend
        print pysend2
        self.sendtopy()
            
    def clickstart(self,events):
        thread.start_new_thread(self.countdown,(0,2))
        #TODO:send topseven, top3, startsignal
        #ips.getConnectionForIp(pyclient).sendMessaage(pysend)
        #ips.getConnectionForIp(pyclient).sendMessaage(pysend2)
        #ips.getConnectionForIp(pyclient).sendMessaage("START")
        rcv.divstart.removeChild(self.textstart)
        rcv.divstart.removeChild(self.rectstart)
        rcv.rootNode.removeChild(self.divstart)
        thread.start_new_thread(self.sendtopy,())
            
    def confirm(self,x):
        
        rcv.rectrej1.fillopacity=0
        rcv.rectrej1.opacity=0
        rcv.textrej1.opacity=0
        
        rcv.rectblockuser.fillopacity=0
        rcv.rectblockuser.opacity=0
        rcv.textblockuser.opacity=0
        #TODO:FARBEN
        self.divask = avg.DivNode(id = "ask",pos=(30,125),size=(250,150),parent=self.rootNode)
        self.divyes = avg.DivNode(id = "yes",pos=(30,215),size=(250,150),parent=self.rootNode)
        self.divno = avg.DivNode(id = "no",pos=(30,260),size=(250,150),parent=self.rootNode)
        
        self.rectask = avg.RectNode(size=(250,30),pos=(0,0),parent=self.divask,color="2EFE2E",fillcolor="58FA58", fillopacity=1)
        self.rectyes = avg.RectNode(size=(250,30),pos=(0,0),parent=self.divyes,color="FE642E",fillcolor="FA8258", fillopacity=1)
        self.rectno = avg.RectNode(size=(250,30),pos=(0,0),parent=self.divno,color="FE2E2E",fillcolor="FA5858", fillopacity=1)
        
        self.textask = avg.WordsNode(pos=(10,5),parent=self.divask,color="088A08",text="Bist Du dir sicher?")
        self.textyes = avg.WordsNode(pos=(10,5),parent=self.divyes,color="8A2908",text="Ja")
        self.textno = avg.WordsNode(pos=(10,5),parent=self.divno,color="8A0808",text="Nein")
            
        self.divno.setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.no)
        if x == 1:
            self.divyes.setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click3s)
        if x == 0:
            self.divyes.setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click2s)
            
    def click3(self,events):
        if (rcv.rectadd.color=="A4A4A4"):
                return 0
        self.confirm(1)
    
    def no(self,events):
            rcv.rootNode.removeChild(self.divask)
            rcv.rootNode.removeChild(self.divno)
            rcv.rootNode.removeChild(self.divyes)

            rcv.rectrej1.fillopacity=1
            rcv.rectrej1.opacity=1
            rcv.textrej1.opacity=1
        
            rcv.rectblockuser.fillopacity=1
            rcv.rectblockuser.opacity=1
            rcv.textblockuser.opacity=1
        
    def click3s(self,events):
            rcv.rootNode.removeChild(self.divask)
            rcv.rootNode.removeChild(self.divno)
            rcv.rootNode.removeChild(self.divyes)

            rcv.rectrej1.fillopacity=1
            rcv.rectrej1.opacity=1
            rcv.textrej1.opacity=1
        
            rcv.rectblockuser.fillopacity=1
            rcv.rectblockuser.opacity=1
            rcv.textblockuser.opacity=1
        
            
            #thread.start_new_thread(self.confirm,(500,))
            #return 0
            text = requestlist.removEle()
            newsong = text.split(' / ')
            interpret = newsong[0]
            songtitle = newsong[1]
            user = userdb.getUser(interpret,songtitle)
            receiver = user.userip
            print user.username, "blockiert."
            user.song1.interpret = "BLO##CKED"
            user.song1.songtitle = "BLO##CKED"
            user.song2.interpret = "BLO##CKED"
            user.song2.songtitle = "BLO##CKED"
            push = "SONGBLO"+interpret+" - "+songtitle
            ips.getConnectionForIp(receiver).sendMessage(str(push))
                
        
    def click2(self,events):
        if (rcv.rectsongplayed.color=="A4A4A4"):
                return 0
        if songdb.getlen() == 0:
                rcv.rectsongplayed.fillcolor="BDBDBD"
                rcv.rectsongplayed.color="A4A4A4"
                rcv.textsongplayed.color="424242"
                return 0
        self.confirm(0)
            
    def click2s(self,events):
            rcv.rootNode.removeChild(self.divask)
            rcv.rootNode.removeChild(self.divno)
            rcv.rootNode.removeChild(self.divyes)

            rcv.rectrej1.fillopacity=1
            rcv.rectrej1.opacity=1
            rcv.textrej1.opacity=1
        
            rcv.rectblockuser.fillopacity=1
            rcv.rectblockuser.opacity=1
            rcv.textblockuser.opacity=1

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
            top3 = []
            i = 0
            if songdb.getlen() < 3:
                k = songdb.getlen()
            else:
                k = 3
            while i < k:
                songele = []
                interpret = songdb[i].interpret
                songtitle = songdb[i].songtitle
                numberofvotes = songdb[i].numberofvotes
                fromuser = songdb[i].fromuser
                song = interpret+'##'+songtitle
                songele.append(interpret)
                songele.append(songtitle)
                songele.append(numberofvotes)
                songele.append(fromuser)
                songele.append(song)
                top3.append(songele)
                i+=1
                
            i = 0
            
            pointgrow = []
            
            while i < k:
                songdb.database.remove(songdb[0])
                songdb.addSong(top3[i][0],top3[i][1],0,top3[i][3])

                for user in userdb:
                    if top3[i][3] == user.userid:
                        c = top3[i][2] * 10
                        user.numberofpoints += c
                        z = True
                        for x in pointgrow:
                            if x[0] == user.userip and x[2] == user.username:
                                x[1] += c
                                z = False
                                
                        if z:
                            pointgrow.append([user.userip,c,user.username])
                        
                    while True:
                    #print user.votedfor
                        z = True
                        if top3[i][4] in user.votedfor:
                            user.votedfor.remove(top3[i][4])
                            user.numberofpoints += 10
                            for x in pointgrow:
                                if x[0] == user.userip and x[2] == user.username:
                                    x[1] += 10
                                    z = False
                            if z:    
                                pointgrow.append([user.userip,10,user.username])
                        else:
                            break
                    
                i+=1
                
            for user in pointgrow:
                push = "POINTGR"+str(user[1])
                ips.getConnectionForIp(user[0]).sendMessage(push)
            
            #sorts users
            userdb.database = userdb.mergeSortc()
            global pysend2
            pysend2 = ""
            i = 0
            while i < 3:
                if i >= userdb.getlen():
                    pysend2 += ' ##0!#!'
                else:
                    pysend2 += userdb[i].username+'##'+str(userdb[i].numberofpoints)+'!#!'
                i+=1
            pysend2 = pysend2[0:len(pysend2)-3]
            print pysend2
            
            #updates topseven
            topseven.update(songdb.tolist(songdb.database[0:6]),5000)
            
            #update pysend
            x = songdb.tolist(songdb.topseven)
            global pysend
            pysend = ""
            for y in x:
                a = y.split(' / ')
                if len(a)==1:
                    pysend+=' ## ##0!#!'
                else:
                    pysend += (a[0])[3:len(a[0])]+'##'+(a[1])+'##'+(a[2])[2:len(a[2])]+'!#!'
            pysend = pysend[0:len(pysend)-3]
            print pysend
            
            #changes button color back to grey
            rcv.rectsongplayed.fillcolor="BDBDBD"
            rcv.rectsongplayed.color="A4A4A4"
            rcv.textsongplayed.color="424242"
            
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
                    x = songdb.tolist(songdb.topseven)
                    
                    global pysend
                    pysend = ""
                    for y in x:
                        a = y.split(' / ')
                        if len(a)==1:
                            pysend+=' ## ##0!#!'
                        else:
                            pysend += (a[0])[3:len(a[0])]+'##'+(a[1])+'##'+(a[2])[2:len(a[2])]+'!#!'
                        
                    pysend = pysend[0:len(pysend)-3]
                    
                    #print pysend
            
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
                rejdb.addSong(interpret,songtitle,0,-1)
                
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
                    
                push = "SONGRE2"+interpret+" - "+songtitle
                ips.getConnectionForIp(receiver).sendMessage(str(push))
                rejdb.addSong(interpret,songtitle,0,-1)
            
            elif eventid == "rej3":
                print('Abgelehnt (unpassend): '+text)
                usersong = text.split(' / ')
                userrej = userdb.getUser(usersong[0],usersong[1])
                if userrej.song1.interpret == usersong[0] and userrej.song1.songtitle == usersong[1] and userrej.song1.status == 0:
                    userrej.song1.interpret = 'LE##ER'
                    userrej.song1.songtitle = 'LE##ER'
                if userrej.song2.interpret == usersong[0] and userrej.song2.songtitle == usersong[1] and userrej.song2.status == 0:
                    userrej.song2.interpret = 'LE##ER'
                    userrej.song2.songtitle = 'LE##ER'
                
                push = "SONGRE3"+interpret+" - "+songtitle
                ips.getConnectionForIp(receiver).sendMessage(str(push))
                
                rejdb.addSong(interpret,songtitle,0, -1)
    
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
        self.textsongplayed =avg.WordsNode(pos=(10,5),parent=self.divsongplayed,color="424242",text="Top 3 gespielt")
        self.divsongplayed.setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click2)
        
        self.timer=avg.WordsNode (pos=(400,250), color="FFFFFF", font="arial", variant="Bold", text="60:00", fontsize=40, parent=self.rootNode)
        
        self.divstart = avg.DivNode(id = "start",pos=(340,215),size=(250,30),parent=self.rootNode)
        self.rectstart = avg.RectNode(size=(250,30),pos=(0,0),parent=self.divstart,color="FF0000",fillcolor="FE2E2E", fillopacity=1)
        self.textstart =avg.WordsNode(pos=(10,5),parent=self.divstart,color="8A0808",text="Start")
        self.divstart.setEventHandler(avg.CURSORDOWN, avg.MOUSE, self.clickstart)
        
        thread.start_new_thread(self.initializeWebSocket, ()) ##start the WebSocket in new Thread        
                      
        log.startLogging(sys.stdout)##Create a logfile (not necessary)
        
    def initializeWebSocket(self):##Starts the WebSocket
        self.factory = WebSocketServerFactory(hostip, debug = False)
        self.factory.protocol = EchoServerProtocol ##assign our Protocol to send/receive Messages
        listenWS(self.factory)
        
        reactor.run(installSignalHandlers=0)##"installSignalHandlers=0" Necessary for Multithreading
        
    def countdown(self,m,s):
            
        def MsToSecs(m,s):
            return m*60 + s

        def secsToMs(secs):
            mins = secs//60
            secs -= mins*60
            mins = str(mins)
            secs = str(secs)
            return mins,secs
            
        seconds = MsToSecs(m,s)
        while seconds >= 0:
            (mint,sect)=secsToMs(seconds)
            if int(mint) == 0 and int(sect) == 0:
                rcv.rectsongplayed.fillcolor="FE2E2E"
                rcv.rectsongplayed.color="FF0000"
                rcv.textsongplayed.color="8A0808" 
            if int(sect) < 10 and int(mint) < 10:
                self.timer.text="0"+mint + ":" + "0"+sect
            elif int(sect) < 10:
                self.timer.text=mint+":"+"0"+sect
            elif int(mint) < 10:
                self.timer.text="0"+mint+":"+sect
            else:
                self.timer.text=mint + ":" +sect
            time.sleep(1)
            seconds -= 1
            if seconds ==-1:
                seconds = 3599
            
             
if __name__ == '__main__':
    rcv=libAvgAppWithRect()
    ips=IPStorage()
    songdb = databases.SongDatabase()
    userdb = databases.UserDatabase()
    rejdb = databases.SongDatabase()
    
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