import socket, threading, time

alphabet = "abcdefghijklmnopqrstuvwxyzaабвгдеєжзиійклмнопрстуфхцчшщьюяа12345678901"

shutdown = False
join = False


def receving(name, sock):
    while not shutdown:
        try:
            while True:
                data, addr = sock.recvfrom(1024)

                decrypt = "";
                if choise == "+":
                    k = False
                    for i in data.decode("utf-8"):
                        if i == ":":
                            k = True
                            decrypt += i
                        elif k == False or i == " ":
                            decrypt += i
                        else:
                            decrypt += chr(ord(i) + 0)
                elif choise == "-":
                    for letter in data.decode("utf-8"):
                        position = alphabet.find(letter)
                        newposition = position - key
                        if letter in alphabet:
                            decrypt = decrypt + alphabet[newposition]
                        else:
                            decrypt = decrypt + letter
                print(decrypt)

                time.sleep(0.2)
        except:
            pass


host = socket.gethostbyname(socket.gethostname())
port = 0

server = ("192.168.1.9", 9090)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

alias = input("Name: ")

print(alias + " Hello!")

choise = input('''
encrypted text: (+)

decrypted text: (-)

Сhoice: ''')

rT = threading.Thread(target=receving, args=("RecvThread", s))
rT.start()

while shutdown == False:
    if join == False:
        s.sendto(("[" + alias + "] => приєднався до чату ").encode("utf-8"), server)
        join = True
    else:
        try:
            message = input()
            message = message.lower()
            key = 1
            crypt = ""

            for letter in message:
                position = alphabet.find(letter)
                newposition = position + key
                if letter in alphabet:
                    crypt = crypt + alphabet[newposition]
                else:
                    crypt = crypt + letter


            message = crypt

            if message != "":
                s.sendto(("[" + alias + "] :: " + message).encode("utf-8"), server)

            time.sleep(0.2)
        except:
            s.sendto(("[" + alias + "] <= left chat ").encode("utf-8"), server)
            shutdown = True

rT.join()
s.close()
