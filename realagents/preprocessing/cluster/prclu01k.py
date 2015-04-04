#!/usr/bin/python
# -*- coding: utf-8 -*-
import spade, os, sys, subprocess, socket
sys.path.append('../../dropoff')
import prall01k
outputdir = "./output"
hostname=(socket.getfqdn())

class Receiver( spade.Agent.Agent ):
        class prclu01( spade.Behaviour.Behaviour ):
                """This behaviour will receive only messages of the 'pcap' ontology"""
                def _process( self ):
                        self.msg = None
                        self.msg = self._receive( True )
                        if self.msg:
                                print "Copying '%s' to local directory" % self.msg.content 
                                subprocess.call(['./preprocess.cluster.01a.copy2local.script.sh', str(self.msg.content)])
                                print "Finished copying '%s' to /output" % self.msg.content 
                                print "Prepping '%s' for the Clustering algorithms" % self.msg.content 
                                subprocess.call(['./preprocess.cluster.02.prep.script.sh', str(self.msg.content)])
                                print "Arff '%s' is ready for data mining with a clusterer" % self.msg.content 

                                # read the directory for the new file
                                files2 = sorted(os.listdir(outputdir), key=lambda x: os.path.getctime(os.path.join(outputdir, x)))
                                newest = files2[-1]

                                dmclu01 = spade.AID.aid(name="dmclu01@"+hostname, addresses=["xmpp://dmclu01@"+hostname])
                                dmclu02 = spade.AID.aid(name="dmclu02@"+hostname, addresses=["xmpp://dmclu02@"+hostname])
                                b = prall01k.Sender("prclu01@"+hostname, "secret", "arff", [dmclu01,dmclu02],  str(newest))
                                print "Sending arff to clusterers"
                                b.start()
                                print "Done sending"

        def _setup(self):
                pcap_template = spade.Behaviour.ACLTemplate()
                pcap_template.setOntology( "pcap" )
                mt = spade.Behaviour.MessageTemplate( pcap_template )
                ab = self.prclu01()
                self.addBehaviour( ab, mt )                                

if __name__ == "__main__":
        a = Receiver( "prclu01@"+hostname, "secret" )
        a.start()

