#!/usr/bin/python
import spade, os, shutil, datetime, socket

class Sender( spade.Agent.Agent ):
        class InformBehav( spade.Behaviour.OneShotBehaviour ):
                def _process( self ):
                        # Second, build the message
                        self.msg = spade.ACLMessage.ACLMessage()
                        self.msg.setPerformative( "inform" )
                        self.msg.setOntology( self.myAgent.myOntology)
                        self.msg.setLanguage( "english" )
                        for rec in self.myAgent.myReceivers:
                            self.msg.addReceiver(rec)
                        self.msg.setContent( self.myAgent.myContent )
                        self.myAgent.send( self.msg )
        def _setup(self):
                print "Alerting follow on processes that a new file is ready for pickup . . ."
                b = self.InformBehav()
                self.addBehaviour( b, None )

        def __init__(self, agentID, password, senderOntology, senderReceivers, senderContent):
                spade.Agent.Agent.__init__(self, agentID, password)
                self.myOntology = senderOntology
                self.myReceivers = []
                self.myReceivers = senderReceivers
                self.myContent = senderContent

if __name__ == "__main__":
        dropdir = "./box"

        files = sorted(os.listdir(dropdir), key=lambda x: os.path.getctime(os.path.join(dropdir, x)))
        hostname=(socket.getfqdn())
        oldest = files[1] # files[0] would be "the oldest" but have to +1 to account for the archive dir
        newest = files[-1]
        # First, form the receiver AID
        prass01 = spade.AID.aid(name="prass01@"+hostname, addresses=["xmpp://prass01@"+hostname])
        prcla01 = spade.AID.aid(name="prcla01@"+hostname, addresses=["xmpp://prcla01@"+hostname])
        prclu01 = spade.AID.aid(name="prclu01@"+hostname, addresses=["xmpp://prclu01@"+hostname])
        a = Sender( "prall01@"+hostname, "secret", "pcap", [prass01,prcla01,prclu01], str(oldest) )
#        a = Sender( "prall01@"+hostname, "secret", "pcap", [prass01,prcla01,prclu01], "zeus-sample-2.pcap" )
        a.start()

