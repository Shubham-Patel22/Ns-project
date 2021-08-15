import sys,socket,ssl

if sys.argv[1] == '-c':
#TCP Connection
	ipaddr = socket.gethostbyname(sys.argv[2])
	c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	print('The chat client\nConnecting to the server:ip='+ipaddr)
	al = socket.getaddrinfo(ipaddr,886)
	c.connect(al[0][4])
	print('\nTCP Connection established.\n')
	c.send(b'chat_hello')
	init = c.recv(1024)
	if init.decode() == 'chat_reply':
		c.send(b'chat_STARTTLS')
		m = c.recv(1024).decode()
		if m == 'chat_STARTTLS_ACK':
		#Load Alice(Client) Certificate & private key
		#TLS Connection
			acont = ssl.SSLContext(ssl.PROTOCOL_TLS)
			acont.options = (ssl.OP_NO_TLSv1_3)
			acont.load_verify_locations('/root/cert_data/Rootcert.pem')
			#load your certificate chain & the private key of the leaf certificate.
			acont.load_cert_chain('/root/cert_data/alicecert_chain.pem','/root/keys/alice_private.key','ns11003')	 
			acont.verify_mode = ssl.CERT_REQUIRED
			alice = acont.wrap_socket(socket.socket())
			alice.connect(al[1][4])
			#Closing the TCP only connection.
			c.close()
			print('TLSv1.3 Connection established.\n') 
			while True :
			#TLS1.3 Communication
				chat = input()
				alice.send(chat.encode('utf-8'))
				if chat == 'chat_close':
					alice.close()
					break
				cr = alice.recv(1024).decode()
				if cr == 'chat_close':
					alice.close()
					break
				else:
					print('\n'+cr+'\n')
		elif m == 'chat_STARTTLS_NOT_SUPPORTED':
			while True :
				chat = input()
				c.send(chat.encode('utf-8'))
				if chat == 'chat_close':
					c.close()
					break
				crs = c.recv(1024).decode()
				if crs == 'chat_close':
					c.close()
					break
				else:
					print('\n'+crs+'\n')

elif sys.argv[1] == '-s':
	ipaddr = socket.gethostbyname('bob1')
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	#For address reuse.
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	print('Binding to IP address: '+ipaddr)
	al = socket.getaddrinfo(ipaddr,886)
	s.bind(al[0][4])
	print('The Chat Server\n')
	s.listen(10)
	conn, addr = s.accept()
	print('TCP Connection established with client:ip='+addr[0])
	init = conn.recv(1024)
	if init.decode() == 'chat_hello':
		conn.send(b"chat_reply")
	init = conn.recv(1024)
	if init.decode() == 'chat_STARTTLS':
		conn.send(b"chat_STARTTLS_ACK")
	#Load Bob(Server) Certificate & private key
	#TLS Connection
		bcont = ssl.SSLContext(ssl.PROTOCOL_TLS,server_side=True)
		bcont.options = (ssl.OP_NO_TLSv1_3)
		bcont.load_verify_locations('/root/cert_data/Rootcert.pem')
		#load your certificate chain & the private key of the leaf certificate.
		bcont.load_cert_chain('/root/cert_data/bobcert_chain.pem','/root/keys/bob_private.key','ns11004')
		bcont.verify_mode = ssl.CERT_NONE
		bob = bcont.wrap_socket(socket.socket())
		#For address reuse.
		bob.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		#Closing the TCP only connection.
		conn.close()
		bob.bind(al[0][4])
		bob.listen(10)
		tlsconn,taddr = bob.accept()
		#verify other side's certificate & provide yours
		print('TLSv1.3 Connection established with client:ip='+taddr[0])
		while True :
		#TLS1.3 Communication
			ch = tlsconn.recv(1024).decode()
			if ch == 'chat_close':
				tlsconn.close()
				break
			print('\n'+ch+'\n')
			res = input()
			tlsconn.send(res.encode('utf-8'))
			if res == 'chat_close':
				tlsconn.close()
				break
	else:
		while True :
		#TCP Communication without any TLS or SSL.
			ch = conn.recv(1024).decode()
			if ch == 'chat_close':
				conn.close()
				break
			print('\n'+ch+'\n')
			res = input()
			conn.send(res.encode('utf-8'))
			if crs == 'chat_close':
				conn.close()
				break
