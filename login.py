"""
In questo modulo sono raccolte le funzioni principali per lo svolgimento di un loggin (credo) corretto.

"""


import hashlib

class CustomLogin:
    """
    Classe Login con appoggio di un file txt dove salvare password e login
    semplice classe di login con due metodi:
        -verifica:
            verifica se l'username e la password sono presenti nella file data_login.txt, se ci sono return True altrimenti False
        -aggiunngi:
            inizialmente verifica se le creadenziali inserite non siano già presenti nel database altrimenti suggerisce all'utente un'altra procedura di login
            se non sono presenti nel database si limita ad aggiungerle
    """
    
    def __init__(self,username,password):
        self.username = username
        self.password = (hashlib.md5(password.strip().encode())).hexdigest() #codifico la password con l'algoritmo di hashing di linux
        data = open("website/txtdata/data_login.txt")
        self.datas = data.readlines() #--> uso readlines per poter ottenere le righe del file sottoforma di array in quanto voglio il formato[username,password]
        
    def _usernames(self):
        usernames=list()
        for element in self.datas:
            temp_list=list(element.split(" "))
            usernames.append(temp_list[0])
        return usernames
    
    def _passwords(self):
        passwords=list()
        for element in self.datas:
            temp_list=list(element.split(" "))
            passwords.append(temp_list[0])
        return passwords

    def validate(self):
        """
        questo metodo scorre attraverso il file per confrontarle con tutti gli utenti per vedere a quale accedere
        
        """
        for element in self.datas:
            temp_list=list(element.split(" "))
            if self.username == temp_list[0] and self.password.strip() == temp_list[1].strip():
                print(f"Benvenuto {self.username}")
                return True
            elif self.username == temp_list[0] and self.password.strip() != temp_list[1].strip():
                print("Uncorrect password.Try again")
                return True
        return False

    def verifica(self):
        """
        Questo metodo verifica che le credenzilali date non siano gia presenti nel sistema
        """
        for element in self.datas:
            if self.username in element:
                return True
        return False
    
    def aggiungi(self):
        """
        Questo metodo verifica che nel sistema non sia presente un account con le credenziali che si vogliono usare ma anche che non venga utilizzato lo stesso nome utente
        """
        if not(self.verifica()):
            with open("data_login.txt","a") as data:
                data.write(f"\n{self.username} {self.password}")
                print(f"Added correctly\nusernmate:{self.username}\npassword:{self.password}")
        else:
            print("This username already exist change it.")

    def login(self):
        if self._verifica():
            self._validate()
        else:
            print("account does not exist. Try to use other credential")

    def logout(self):
        pass


if __name__ == "__main__":           
    username = input("username: ")
    password = input("password: ")
    account = CustomLogin(username, password)
    account.aggiungi()
    account.login()
