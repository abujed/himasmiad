#!/usr/bin/python
# -*- coding: utf-8 -*-
import spade, os, sys, subprocess, socket
sys.path.append('../../dropoff')
import prall01k
outputdir = "./output"
hostname=(socket.getfqdn())

class Receiver( spade.Agent.Agent ):
        class prcla01( spade.Behaviour.Behaviour ):
                """This behaviour will receive only messages of the 'pcap' ontology"""
                def _process( self ):
                        self.msg = None
                        self.msg = self._receive( True )
                        if self.msg:
                                print "Copying '%s' to local directory" % self.msg.content 
                                subprocess.call(['./preprocess.classify.01a.copy2local.script.sh', str(self.msg.content)])
                                print "copied '%s' to /output" % self.msg.content 
                                print "Running markey pcapmod on '%s' " % self.msg.content 
                                subprocess.call(['./preprocess.classify.01.markey.pcapmod.oneoff.script.sh', str(self.msg.content)])
                                print "Arff '%s' is ready for data mining with a classifier" % self.msg.content 
 
                                # read the directory for the new file
                                files2 = sorted(os.listdir(outputdir), key=lambda x: os.path.getctime(os.path.join(outputdir, x)))
                                newest = files2[-1]

                                dmcla01 = spade.AID.aid(name="dmcla01@"+hostname, addresses=["xmpp://dmcla01@"+hostname])
                                dmcla02 = spade.AID.aid(name="dmcla02@"+hostname, addresses=["xmpp://dmcla02@"+hostname])
                                dmcla03 = spade.AID.aid(name="dmcla03@"+hostname, addresses=["xmpp://dmcla03@"+hostname])
                                b = prall01k.Sender("prcla01@"+hostname, "secret", "arff", [dmcla01,dmcla02,dmcla03],  str(newest))
                                print "Sending arff to classifiers"
                                b.start()
                                print "Done sending"

        def _setup(self):
                pcap_template = spade.Behaviour.ACLTemplate()
                pcap_template.setOntology( "pcap" )
                mt = spade.Behaviour.MessageTemplate( pcap_template )
                ab = self.prcla01()
                self.addBehaviour( ab, mt )                                

if __name__ == "__main__":
        a = Receiver( "prcla01@"+hostname, "secret" )
        a.start()
