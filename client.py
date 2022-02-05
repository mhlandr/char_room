# module necesare

import socket
import threading

Host = '127.0.0.1'
Port = 1234



#functia care va asculta dupa mesajele trimie de alti clienti pe server
def listen_to_messange_from_server(client):
    
    while True:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            # username ul este primit la index 0 si mesajul la index 1
            username = message.split("~")[0]
            content = message.split("~")[1]
            
            print(f"[{username}]: {content}")
            
        else: 
            print("Message recived from client is empty")



# functia care va trimite mesaje serverului
def sed_message_to_server(client):
    
    while True:
        message = input("Message: ")
        
        if message !='':
            
            client.sendall(message.encode())
            
        else:
            print("Empty message !")
            exit(0)
    



# functia care va comunica cu serverul 
def communicate_to_server(client):
    
    username = input("Enter your username: ")
    if username != '': 
    
        client.sendall(username.encode())
    
    else :
     
        print("Username can't be empty ! ")
        exit(0)
        
    # functia listen_to_message_from_server va fi chemata incontinu de catre thread 
    # in cazul in care server ul va trimite un mesaj 
    threading.Thread(target=listen_to_messange_from_server,args=(client, )).start()
    
    sed_message_to_server(client)



def main():
    
    #soclu de comunicare pe partea clientuli
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        
        client.connect((Host,Port))
        print(f"Successfuly connected to server {Host}")
    
    except:
        
        print(f"Unable to connect to server {Host} on port {Port}")
        
    communicate_to_server(client)
    
    
    
if __name__ == '__main__':
    main()
    