#!/usr/bin/python
# -*- coding: utf-8 -*-
import spade, sys, subprocess, socket

hostname=(socket.getfqdn())

class Receiver( spade.Agent.Agent ):
        class dmcla02( spade.Behaviour.Behaviour ):
                """This behaviour will receive only messages of the 'arff' ontology"""
                def _process( self ):
                        self.msg = None
                        self.msg = self._receive( True )
                        if self.msg:
                                print "Datamining '%s' with J48 model 2" % self.msg.content 
                                subprocess.call(['./dm.classify.j48.02.script.sh', str(self.msg.content)])
                                print "Finished running '%s' through J48 model 2" % self.msg.content 


        def _setup(self):
                pcap_template = spade.Behaviour.ACLTemplate()
                pcap_template.setOntology( "arff" )
                mt = spade.Behaviour.MessageTemplate( pcap_template )
                ab = self.dmcla02()
                self.addBehaviour( ab, mt )                                

if __name__ == "__main__":
        a = Receiver( "dmcla02@"+hostname, "secret" )
        a.start()
