# module necesare
import socket
import threading 


Host = '127.0.0.1' # ip ul serverului
Port = 1234 # portul pe care va opera serverul
ListnerLimit = 5 # numarul de persoane care se pot conecta simultan la server 
active_clients= [] # lista clientilor activi



#functia care trimite un messaj la un singur client 
def send_message_single(client,message):
    
    # trimite mesajele mai departe si le econdeaza 
    # nu mai specificam tipul de encodare deoarece 
    # uft-8 este folosit ca si valoare default 
      
    client.sendall(message.encode())



# functia care trimite mesajele noi la toti clientii conectati
def send_message_all(form_username, message):
    
    for user in active_clients:
        
        #user[1] este utilizatorul, user[0] este usernameul  
        send_message_single (user[1], message)
        
        
        
# functia care se va ocupa de client 
def client_handler(client):
    
    # serverul va ascula dupa mesaje care contin username
    
    while True:
        
        # recv = recive si marimea mesajului maxim care poate fi ascultat
        # utf-8 encodarea mesajelor cand sunt trasformate in bytes 
        username = client.recv(2048).decode('utf-8')
        
        #daca lista de clienti nu este goala
        if username != ' ' :
            
            active_clients.append(username,client)
            break;
         
        else:
            
            print ("client username is empty") 
    threading.Thread(target=listen_for_message, args=(client, username,)).start()



# functia care asculta mesaje noi de la clienti
def listen_for_message(client):
    
    username = " "
    message = " "
    
    while True:
        
        response = client.recv(2048).decode('utf-8')
        
        if response != '':
            
            # mesajul final este prelucrat 
            final_msg = username + '~' + message 
            send_message_all(final_msg)
           
            
        else:
            print(f"Messages sent from client {username} is empty")



def main():

    # soclu de comunicare pe partea serverlui 
    # AF_INET = IPv4
    # SOCK_STREAM = TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    try:
        
        #ii dam serverului adresa sub forma de 
        server.bind((Host,Port)) 
        
        print(f"Runing the server on port {Port}")
        
    except:

        print(f"Unable to bind to host {Host} and port {Port}")

    # limita de persoane care 
    server.listen(ListnerLimit)
    
    # server ul continua in continuare sa asculte dupa mesaje
    while True :
        
        client,addres = server.accept()
        print(f"Successfully connected to client {addres[0]} on port {addres[1]}")
        
        threading.Thread(target=client_handler, args=(client, )).star()

if __name__ == '__main__':
    main()