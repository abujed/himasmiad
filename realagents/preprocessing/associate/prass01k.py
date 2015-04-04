#!/usr/bin/python
# -*- coding: utf-8 -*-
import spade, os, sys, subprocess, socket
sys.path.append('../../dropoff')
import prall01k
outputdir = "./output"
hostname=(socket.getfqdn())

class Receiver( spade.Agent.Agent ):
        class prass01( spade.Behaviour.Behaviour ):
                """This behaviour will receive only messages of the 'pcap' ontology"""
                def _process( self ):
                        self.msg = None
                        self.msg = self._receive( True )
                        if self.msg:
                                print "Copying '%s' to local directory" % self.msg.content 
                                subprocess.call(['./preprocess.associate.01a.copy2local.script.sh', str(self.msg.content)])
                                print "Converting '%s' to arff" % self.msg.content 
                                subprocess.call(['./preprocess.associate.01.pcap2arff.script.sh', str(self.msg.content)])
                                print "Prepping '%s' arff for Apriori" % self.msg.content 
                                subprocess.call(['./preprocess.associate.02.apriori.prep.script.sh', str(self.msg.content)])
                                print "Arff '%s' is ready for data mining with an associator" % self.msg.content 
                                # read the directory for the new file
                                files2 = sorted(os.listdir(outputdir), key=lambda x: os.path.getctime(os.path.join(outputdir, x)))
                                newest = files2[-1]

                                dmass01 = spade.AID.aid(name="dmass01@"+hostname, addresses=["xmpp://dmass01@"+hostname])
                                b = prall01k.Sender("prass01@"+hostname, "secret", "arff", [dmass01],  str(newest))
                                print "Sending arff to associator"
                                b.start()
                                print "Done sending"

        def _setup(self):
                pcap_template = spade.Behaviour.ACLTemplate()
                pcap_template.setOntology( "pcap" )
                mt = spade.Behaviour.MessageTemplate( pcap_template )
                ab = self.prass01()
                self.addBehaviour( ab, mt )    

if __name__ == "__main__":
        a = Receiver( "prass01@"+hostname, "secret" )
        a.start()
