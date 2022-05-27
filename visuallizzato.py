
from flask import Blueprint, render_template, request
from scraping import Scraping

visualizza= Blueprint("visualizza",__name__)

@visualizza.route("/home", methods=["GET","POST"])
def home():
    scraping=Scraping()
    scraping.GetData()
    
    if request.method == "POST" and request.form.get("search-bar") != "":
        name = request.form.get("search-bar")
    else:
        name=""

    title=open("txtdata/data_film_title.txt","r")
    image=open("txtdata/data_img.txt","r")
    link=open("txtdata/data_film_link.txt","r")

    title_l=title.readlines()
    image_l=image.readlines()
    link_l = link.readlines()
    return render_template("home.html", scraping=scraping,name=name, title=title_l,image=image_l,link=link_l)