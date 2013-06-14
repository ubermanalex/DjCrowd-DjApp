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
                               
class ListNode(DivNode):

    def __init__ (self, slist, scount, **kwargs):
        super(ListNode, self).__init__(**kwargs)
        
        self.slist  = []
        
        for string in slist:
            self.slist.append(string)
         
        self.scount = scount
        self.listlength = len(slist) 
        
        self.window = avg.DivNode(id="window", size=(300, len(slist)*20), pos =(0,0), parent= self)
        self.i = 0 
        self.p = 0 
        self.node = slist
        for string in slist:
            self.node[self.i] = WordsNode(id = str(self.i), text= str(string), color="FFFFFF", pos=(5,self.p), parent=self.window)
            self.node[self.i].setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click)
            self.p = self.p+20
            self.i = self.i +1
            
            
        self.captureHolder = None
        self.dragOffsetY = 0
        self.setEventHandler(avg.CURSORDOWN, avg.MOUSE | avg.TOUCH, self.startScroll)
        self.setEventHandler(avg.CURSORMOTION, avg.MOUSE | avg.TOUCH, self.doScroll)
        self.setEventHandler(avg.CURSORUP, avg.MOUSE | avg.TOUCH, self.endScroll)
        self.setEventHandler(avg.CURSOROUT, avg.MOUSE | avg.TOUCH, self.outofDiv)
        self.SelectedString = ""
        self.node_old = 0
        self.current_event = None
            
    def click(self, event):
        self.current_event = event
        self.selectString()
        
    def selectString(self):
        event = self.current_event
        if (event.node.id != self.node_old):
            nodeid = rcv.player.getElementByID(str(self.node_old))
                      
            nodeid.color = "FFFFFF"
            event.node.color = "F4FA58"
            
            rcv.rectadd.color="2EFE2E"
            rcv.rectrej1.color="FE9A2E"
            rcv.rectrej2.color="FE642E"
            rcv.rectrej3.color="FE2E2E"
            rcv.rectadd.fillcolor="58FA58"
            rcv.rectrej1.fillcolor="FAAC58"
            rcv.rectrej2.fillcolor="FA8258"
            rcv.rectrej3.fillcolor="FA5858"
            rcv.textadd.color="088A08"
            rcv.textrej1.color="8A4B08"
            rcv.textrej2.color="8A2908"
            rcv.textrej3.color="8A0808"
        
        else:
            pass
        self.node_old = event.node.id
        
        
        
    def addEle(self, elem):
        i = len(self.slist)
        
        self.node.append("")
        self.slist.append(elem)
        #pdb.set_trace()
        node =  WordsNode(id = str(i), text= str(elem), color="FFFFFF", pos=(5,self.p), parent=self.window)
        self.node[i] = node
        self.node[i].setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click)

        self.p = self.p+20
        
        self.window.size = (avg.Point2D(self.window.size.x, self.window.size.y + 20))
        
        
                      
    def removEle(self):
        
        if (rcv.rectadd.color=="A4A4A4"):
            return 0
        
        event = self.current_event
        e = rcv.player.getElementByID(str(event.node.id))
        counter = int(event.node.id)+1
        iterend = len(self.node)
        
        #print ('ITER: '+str(counter)+" "+str(iterend))
        #print ('DELID: '+str(e.id))
        
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
        #print (self.slist)
        #print (self.node)
            
        rcv.rectadd.color="A4A4A4"
        rcv.rectrej1.color="A4A4A4"
        rcv.rectrej2.color="A4A4A4"
        rcv.rectrej3.color="A4A4A4"
        rcv.rectadd.fillcolor="BDBDBD"
        rcv.rectrej1.fillcolor="BDBDBD"
        rcv.rectrej2.fillcolor="BDBDBD"
        rcv.rectrej3.fillcolor="BDBDBD"
        rcv.textadd.color="424242"
        rcv.textrej1.color="424242"
        rcv.textrej2.color="424242"
        rcv.textrej3.color="424242"
        
        self.current_event = None
        self.node_old = 0
        self.p = self.p-20
        
        return rettext
        
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
        if (msg[0:4] == 'BACK'):
            self.sendMessage(msg[4:len(msg)], binary)##send back message to initiating client
        ##adds user
        
        if (msg[0:10] == 'USERNAME: '):
            oberegrenze = len(msg)
            userdb.addUser(userdb.getlen(),msg[10:oberegrenze],0,3)
            userstr = ('ID: '+str(userdb[userdb.getlen()-1].userid)+'\n'+
                   'NAME: '+str(userdb[userdb.getlen()-1].username)+'\n'+
                   'SONG1: '+str(userdb[userdb.getlen()-1].song1.interpret)+" - "+str(userdb[userdb.getlen()-1].song1.songtitle)+
                   str(userdb[userdb.getlen()-1].song1.status)+'\n'+
                   'SONG2: '+str(userdb[userdb.getlen()-1].song2.interpret)+" - "+str(userdb[userdb.getlen()-1].song2.songtitle)+
                   str(userdb[userdb.getlen()-1].song2.status)+'\n'+
                   'POINTS: '+str(userdb[userdb.getlen()-1].numberofpoints)+'\n'+
                   'VOTES: '+str(userdb[userdb.getlen()-1].numberofvotes))
            self.sendMessage(userstr, binary)##send back message to initiating client
            print(userstr)
            
        ##adds song

        if (msg[0:6] == 'SONG: '):
            oberegrenze = len(msg)
            songelems = msg[6:oberegrenze].split('##')
            interpret = songelems[0]
            songtitle = songelems[1]
            
            for userobj in userdb:
                if (userobj.username == songelems[2]):
                    print userobj.userid
                    if (userobj.song1.interpret == "LE##ER"):
                        print ("CHANGE s1")
                        userobj.song1.interpret = interpret
                        userobj.song1.songtitle = songtitle
                        userobj.song1.status = 0
                    elif (userobj.song2.interpret == "LE##ER"):
                        userobj.song2.interpret = interpret
                        userobj.song2.songtitle = songtitle
                        userobj.song2.status = 0
                        print ("CHANGE s1")
                    else:
                        return 0

            userstr = ('ID: '+str(userdb[userdb.getlen()-1].userid)+'\n'+
                   'NAME: '+str(userdb[userdb.getlen()-1].username)+'\n'+
                   'SONG1: '+str(userdb[userdb.getlen()-1].song1.interpret)+" - "+str(userdb[userdb.getlen()-1].song1.songtitle)+
                   str(userdb[userdb.getlen()-1].song1.status)+'\n'+
                   'SONG2: '+str(userdb[userdb.getlen()-1].song2.interpret)+" - "+str(userdb[userdb.getlen()-1].song2.songtitle)+
                   str(userdb[userdb.getlen()-1].song2.status)+'\n'+
                   'POINTS: '+str(userdb[userdb.getlen()-1].numberofpoints)+'\n'+
                   'VOTES: '+str(userdb[userdb.getlen()-1].numberofvotes))
            print(userstr)
            

            rcv.player.setTimeout(0, lambda : requestlist.addEle(interpret+" ~~~ "+songtitle))
            
        ##applies vote
        
        if (msg[0:6] == 'VOTE: '):
            oberegrenze = len(msg)
            userandsong = msg[6:oberegrenze].split('##')
            user = userandsong[0]
            song = userandsong[1]
            userdblen = userdb.getlen()
            songdblen = songdb.getlen()
            
            for i in range(0,userdblen):
                if (user == userdb[i].username):
                    if (userdb[i].numberofvotes == 0):
                        return 0
                    userdb[i].numberofvotes -= 1
                    print ('USERVOTES: '+str(userdb[i].numberofvotes))
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
            print('Interpret: '+str(songdb[0].interpret)+'\n'+
                  'Songtitel: '+str(songdb[0].songtitle)+'\n'+
                  'Voteanzahl: '+str(songdb[0].numberofvotes)+'\n'+
                  'Von User: '+str(songdb[0].fromuser))

            
class libAvgAppWithRect (AVGApp): ##Main LibAVG App that uses WebSockets
        
    def click(self,events):
            
            if (rcv.rectadd.color=="A4A4A4"):
                return 0
            text = requestlist.removEle()
            eventid = (events.node.id)
            
            if eventid == "add":
                print('Hinzugefuegt: '+text)
                newsong = text.split(' ~~~ ')
                interpret = newsong[0]
                songtitle = newsong[1]
                user = userdb.getUser(interpret,songtitle)
                
                if (user.song1.status == 0):
                    user.song1.interpret = interpret
                    user.song1.songtitle = songtitle
                    user.song1.status = 1
                elif (user.song2.status == 0):
                    user.song2.interpret = interpret
                    user.song2.songtitle = songtitle
                    user.song2.status = 1
                else:
                    return 0
                
                userstr = ('ID: '+str(userdb[userdb.getlen()-1].userid)+'\n'+
                   'NAME: '+str(userdb[userdb.getlen()-1].username)+'\n'+
                   'SONG1: '+str(userdb[userdb.getlen()-1].song1.interpret)+" - "+str(userdb[userdb.getlen()-1].song1.songtitle)+
                   str(userdb[userdb.getlen()-1].song1.status)+'\n'+
                   'SONG2: '+str(userdb[userdb.getlen()-1].song2.interpret)+" - "+str(userdb[userdb.getlen()-1].song2.songtitle)+
                   str(userdb[userdb.getlen()-1].song2.status)+'\n'+
                   'POINTS: '+str(userdb[userdb.getlen()-1].numberofpoints)+'\n'+
                   'VOTES: '+str(userdb[userdb.getlen()-1].numberofvotes))
                print(userstr)
            
                
                songdb.addSong(interpret,songtitle,0,user.userid)
                print('Interpret: '+str(songdb[songdb.getlen()-1].interpret)+'\n'+
                      'Songtitel: '+str(songdb[songdb.getlen()-1].songtitle)+'\n'+
                      'Voteanzahl: '+str(songdb[songdb.getlen()-1].numberofvotes)+'\n'+
                      'Von User: '+str(songdb[songdb.getlen()-1].fromuser))
                #rcv.factory.protocol.sendMessage("REQANS: Song hinzugefuegt.",False)
            elif eventid == "rej1":
                print('Abgelehnt (doppelt): '+text)
                #TODO:rcv.factory.protocol.send('REQANS: Song bereits in Crowdlist.')
            elif eventid == "rej2":
                print('Abgelehnt (nicht vorh.): '+text)
                #TODO:rcv.factory.protocol.send('REQANS: Song nicht vorhanden.')
            elif eventid == "rej3":
                print('Abgelehnt (unpassend): '+text)
                #TODO:rcv.factory.protocol.send('REQANS: Song passt heute nicht.')


    
    def __init__(self): ##Create one WordsNode for the Text and RectNode to send to a certain Client and set player, canvas,..
        self.player=avg.Player.get()
        self.canvas=self.player.createMainCanvas(size=(310,310))
        self.rootNode=self.canvas.getRootNode()

        self.rectadd = avg.RectNode(size=(250,30),pos=(30,125),parent=self.rootNode,color="A4A4A4",fillcolor="BDBDBD", fillopacity=1)
        self.rectrej1 = avg.RectNode(size=(250,30),pos=(30,170),parent=self.rootNode,color="A4A4A4",fillcolor="BDBDBD", fillopacity=1)
        self.rectrej2 = avg.RectNode(size=(250,30),pos=(30,215),parent=self.rootNode,color="A4A4A4",fillcolor="BDBDBD", fillopacity=1)
        self.rectrej3 = avg.RectNode(size=(250,30),pos=(30,260),parent=self.rootNode,color="A4A4A4",fillcolor="BDBDBD", fillopacity=1)

        self.divadd = avg.DivNode(id = "add",pos=(30,125),size=(250,30),parent=self.rootNode)
        self.divrej1 = avg.DivNode(id = "rej1",pos=(30,170),size=(250,30),parent=self.rootNode)
        self.divrej2 = avg.DivNode(id = "rej2",pos=(30,215),size=(250,30),parent=self.rootNode)
        self.divrej3 = avg.DivNode(id = "rej3",pos=(30,260),size=(250,30),parent=self.rootNode)
        
        self.divadd.setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click)
        self.divrej1.setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click)
        self.divrej2.setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click)
        self.divrej3.setEventHandler(avg.CURSORDOWN, avg.MOUSE,  self.click)
        
        self.textadd =avg.WordsNode(pos=(10,5),parent=self.divadd,color="424242",text="Vorschlag annehmen")
        self.textrej1 = avg.WordsNode(pos=(10,5),parent=self.divrej1,color="424242",text="Doppelt")
        self.textrej2 = avg.WordsNode(pos=(10,5),parent=self.divrej2,color="424242",text="Nicht vorhanden")
        self.textrej3 = avg.WordsNode(pos=(10,5),parent=self.divrej3,color="424242",text="Passt nicht")

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
    requestlist = ListNode([], 2, size=(300, 100), pos=(5, 5), crop=True, elementoutlinecolor="333333", parent=rcv.player.getRootNode())
    rcv.player.play()