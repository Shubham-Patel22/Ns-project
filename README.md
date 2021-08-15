## NS assignment 3
### Task1

* In task 1 we need CA, alice,bob
* Using openssl command create rsa key 
* Extarct public key 
* using public key genrate certificate rootcartificate,alice cerficate,bob certificate.
* vm to container using lxc file push alice.csr alice1/root
* container to container  exchange cerfitificate using lxc shell alice1 
*   send alice cerificate,bob certificate,public key of bob and alice to Root CA container
* Root CA verify both certificate and signed it
* send to alice and bob container.

### task 2

*First, we start the server in Bob side by typing:-
	python3 secure_chat_app.py -s
*Then, on alice side we type:-
	python3 secure_chat_app.py -c bob1
