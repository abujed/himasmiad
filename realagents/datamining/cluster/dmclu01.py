#!/usr/bin/python
# -*- coding: utf-8 -*-
import spade, sys, subprocess, socket

hostname=(socket.getfqdn())

class Receiver( spade.Agent.Agent ):
        class dmclu01( spade.Behaviour.Behaviour ):
                """This behaviour will receive only messages of the 'arff' ontology"""
                def _process( self ):
                        self.msg = None
                        self.msg = self._receive( True )
                        if self.msg:
                                print "Datamining '%s' with cobweb clusterer" % self.msg.content 
                                subprocess.call(['./dm.cluster.cobweb.01.script.sh', str(self.msg.content)])
                                print "Finished running '%s' through cobweb clusterer" % self.msg.content 


        def _setup(self):
                pcap_template = spade.Behaviour.ACLTemplate()
                pcap_template.setOntology( "arff" )
                mt = spade.Behaviour.MessageTemplate( pcap_template )
                ab = self.dmclu01()
                self.addBehaviour( ab, mt )                                

if __name__ == "__main__":
        a = Receiver( "dmclu01@"+hostname, "secret" )
        a.start()
