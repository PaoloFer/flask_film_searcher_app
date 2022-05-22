
from flask import Blueprint, redirect, render_template,request,flash
from login import CustomLogin
import hashlib

autentica= Blueprint("autentica",__name__)

@autentica.route("/login", methods =['GET','POST'])
def login():
    if request.method == 'POST':
        username= request.form.get("username")
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

    return render_template("index.html")

@autentica.route("/sign-up",methods =['GET','POST'])
def singin():
    if request.method == 'POST':
        username= request.form.get("username")
        password=request.form.get("password")
        password2 = request.form.get("password2")
        user= CustomLogin(username,password)

        if len(password) < 7 and len(password) != 0:
            flash('Password sbagliata', category='error')
        elif password != password2:
            flash('Password 1 diversa da Password 2', category='error')
        elif user.verifica():
            #verifico questo in quanto sennò viene continuamente segnalato un messaggio anche se non viene inserito nulla come input
            if len(username)==0:
                pass
            else:
                flash("Nome utente già esistente. Prova con uno diverso",category='error')
        else:
            with open("txtdata/data_login.txt","a") as data:
                data.write(f"\n{username} {(hashlib.md5(password.strip().encode())).hexdigest()}")
                print(f"Added correctly usernmate:{username} password:"+("*"*len(password)))

            with open(f"accountxt/{username}.txt", "w") as user:
                
                user.close()

            flash("Registrazione completata!")
            return redirect("/")

    return render_template("sign-up.html")

@autentica.route("/logout")
def logout():
    return render_template("logout.html")