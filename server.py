import socket
import threading

HOST='127.0.0.1'
PORT= 23412
LISTENER_LIMIT=5
acive_clients=[] #list of all currently connected users


#Function to listen for an upcoming message from client
def listen_for_messages(client,username):
    while 1:
        message=client.recv(2048).decode('utf-8')
        if message !='':
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)
        else:
            print("message sent from client {} is empty ".format(username))


#Function to send message to single client
def send_message_to_client(client,message):
    client.sendall(message.encode())


#Function to send messages to all clients which are currently connected to server
def send_messages_to_all(message):
    for user in acive_clients:
        send_message_to_client(user[1],message)
    


#Function to handle client
def client_handler(client):
    #server will listen for client message that will contain the username
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username!='':
            acive_clients.append((username, client))
            prompt_message = "SERVER~" + "{} added to the chat".format(username)
            send_messages_to_all(prompt_message)
            break
        else:
            print("client username is empty")

    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #binding of host and port
    try:
        server.bind((HOST, PORT))
        print("Running the server on {} {}".format(HOST, PORT))
    except:
        print("Unable to bind {} {}".format(HOST, PORT))
        pass
    #set server limit
    server.listen(LISTENER_LIMIT)

    while 1:
         client, address = server.accept()
         print("Successfully connected to {} {}".format(address[0], address[1]))


         threading.Thread(target=client_handler, args=(client, )).start()


if __name__ =='__main__':
    main()

