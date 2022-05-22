"""
Questo file __init__.py ha due funzioni:
1) rendere la cartella website un package/module e quindi importabile
2) far si che quando si esegua l'import venga eseguito ciò che c'è definito in questo file e quini la creazione dell'app

una caratteristica che implica rendere website un package è il fatto che tutti gli import dovranno essere fatti in percorso relativo rispetto a questa cartella quindi from . import  askdjfa

"""
from flask import Flask, render_template ,redirect,request,flash
from scraping import Scraping
import hashlib
from login  import CustomLogin

def crea_app():
    #server per svuotare i file
    open("website/txtdata/data_film_link.txt", "w").close()
    open("website/txtdata/data_film_title.txt", "w").close()
    open("website/txtdata/data_img.txt", "w").close()
    
    search = Scraping()
    search.GetData()
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'


    #importo le varie Blueprint create negli altri file
    from visuallizzato import visualizza
    from autenticazione import autentica

    #aggiungo le Blueprint nell'app (i prefissi metto solo la backslash altrimenti implicherebbe la creazione di url inutilmente lunghi per accedere a delle pagine web)
    app.register_blueprint(visualizza,url_prefix="/") 
    app.register_blueprint(autentica,url_prefix="/")

    scraping=Scraping()
    @app.route("/", methods=["GET","POST"])
    def fpage():
        if request.method == 'POST':
            username= request.form.get("username")
            print(username)
            password=request.form.get("password")
            password=(hashlib.md5(password.strip().encode())).hexdigest()
            user= CustomLogin(username,password)
            
            if len(password) < 7 and len(password) != 0:
                flash('Password sbagliata', category='error')
            elif not(user.verifica()):
                #verifico questo in quanto sennò viene continuamente segnalato un messaggio anche se non viene inserito nulla come input
                if len(username)==0:
                    pass
                else:
                    flash("Nome utente non esistente. Prova con uno diverso",category='error')
            else:
                if user.validate():
                    flash("Dati corretti!")
                    return  redirect("/home")

        return render_template("login.html")

    return app

if __name__ =="__main__":
    app = crea_app()
    app.run(debug=True)
