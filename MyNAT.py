from mininet.cli import CLI
from mininet.log import lg
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.nodelib import NAT
from mininet.node import Node
class myTopo(Topo):
    	"Topology for a tree network with a given depth and fanout."
	def build( self, depth=2, fanout=2 ):
        	# Numbering:  h1..N, s1..M
        	self.hostNum = 1
        	self.switchNum = 1
       	 	# Build topology
        	self.addTree( depth, fanout )

    	def addTree( self, depth, fanout ):
        	"""Add a subtree starting with node n.
           	returns: last node added"""
        	isSwitch = depth > 0
        	if isSwitch:
            		node = self.addSwitch( 's%s' % self.switchNum )
            		self.switchNum += 1
            		for _ in range( fanout ):
                		child = self.addTree( depth - 1, fanout )
                		self.addLink( node, child )
        	else:
            		node = self.addHost( 'h%s' % self.hostNum )
            		self.hostNum += 1
        	return node
class MyNAT(NAT):
	def config( self, **params ):
		"""Configure the NAT and iptables"""
		super( NAT, self).config( **params )

		if not self.localIntf:
		    	self.localIntf = self.defaultIntf()

		if self.flush:
		    	self.cmd( 'sysctl net.ipv4.ip_forward=0' )             	#no ip forwarding function
		    	self.cmd( 'iptables -F' )				#delete all rules in filter table			
		    	self.cmd( 'iptables -t nat -F' )			#delete all rules in nat table
		    	# Create default entries for unmatched traffic
		    	self.cmd( 'iptables -P INPUT ACCEPT' )			#set default policy on input chain of filter table
		    	self.cmd( 'iptables -P OUTPUT ACCEPT' )			#set default policy on output chain of filter table
		    	self.cmd( 'iptables -P FORWARD DROP' )			#set default policy on forward chain of filter table

		# Install NAT rules
		self.cmd( 'iptables -I FORWARD',				
		          '-i', self.localIntf, '-d', self.subnet, '-j DROP' )	#-i=localIntf,-d=subnet		drop
		self.cmd( 'iptables -A FORWARD',
		          '-i', self.localIntf, '-s', self.subnet, '-j ACCEPT' )#-i=localIntf,-s=subnet		accept 		
		self.cmd( 'iptables -A FORWARD',
		          '-o', self.localIntf, '-d', self.subnet, '-j ACCEPT' )#-o=localIntf,-d=subnet		accept
		self.cmd( 'iptables -t nat -A POSTROUTING',
		          '-s', self.subnet, "'!'", '-d', self.subnet,
		          '-j MASQUERADE' )					#-s=subnet,-d=subnet 		masquerade
		
		# Instruct the kernel to perform forwarding
		self.cmd( 'sysctl net.ipv4.ip_forward=1' )

		# Prevent network-manager from messing with our interface
		# by specifying manual configuration in /etc/network/interfaces
		intf = self.localIntf
		cfile = '/etc/network/interfaces'
		line = '\niface %s inet manual\n' % intf
		config = open( cfile ).read()
		if ( line ) not in config:
		    	info( '*** Adding "' + line.strip() + '" to ' + cfile + '\n' )
		    	with open( cfile, 'a' ) as f:
		        	f.write( line )
		# Probably need to restart network-manager to be safe -
		# hopefully this won't disconnect you
		self.cmd( 'service network-manager restart' )
class MyMininet(Mininet):
	def addNAT( self, name='nat0', connect=True, inNamespace=False,
                **params):
		"""Add a NAT to the Mininet network
		   name: name of NAT node
		   connect: switch to connect to | True (s1) | None
		   inNamespace: create in a network namespace
		   params: other NAT node params, notably:
		       ip: used as default gateway address"""
		nat = self.addHost( name, cls=MyNAT, inNamespace=inNamespace,
		                    subnet=self.ipBase, **params )
		# find first switch and create link
		if connect:
		    	if not isinstance( connect, Node ):
		        	# Use first switch if not specified
		       		connect = self.switches[ 0 ]
		    	# Connect the nat to the switch
		    	self.addLink( nat, connect )
		    	# Set the default route on hosts
		    	natIP = nat.params[ 'ip' ].split('/')[ 0 ]
		    	for host in self.hosts:							#set gateway
		        	if host.inNamespace:
		            		host.setDefaultRoute( 'via %s' % natIP )
		return nat
if __name__ == '__main__':
	lg.setLogLevel( 'info')
	topo=myTopo()
	while(True):
		tmp=raw_input("add NAT or not?y/Y=yes,n/N=no,e/E=exit---------------------\n")
		if(tmp=="y" or tmp=="Y"):
			net = MyMininet(topo=topo)
		    	# Add NAT connectivity
			net.addNAT().configDefault()
			net.start()
	    		CLI( net )
	    		# Shut down NAT
    			net.stop()
		elif(tmp=='n' or tmp=='N'):
			net = MyMininet(topo=topo)
		    	# Add NAT connectivity
			net.start()
	    		CLI( net )
	    		# Shut down NAT
    			net.stop()
		elif(tmp=='e' or tmp=='E'):
			break
		else:
			continue
