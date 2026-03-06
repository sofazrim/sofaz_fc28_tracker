
from flask import Flask, render_template, request
from datetime import datetime
import math

app = Flask(__name__)

def calcul_fc28(resistance, age):
    return resistance * (28 / age) ** 0.5

@app.route("/")
def home():
    return render_template("index_fr.html")

@app.route("/en")
def home_en():
    return render_template("index_en.html")

@app.route("/fc28_fr", methods=["GET","POST"])
def fc28_fr():

    result=None

    if request.method=="POST":

        date=request.form["date"]
        age=float(request.form["age"])
        resistance=float(request.form["resistance"])
        fc28=float(request.form["fc28"])

        res_28=calcul_fc28(resistance,age)

        conforme=res_28>=fc28

        result={
            "res_28":round(res_28,2),
            "fc28":fc28,
            "conforme":conforme
        }

    return render_template("fc28_fr.html",result=result)


@app.route("/fc28_en", methods=["GET","POST"])
def fc28_en():

    result=None

    if request.method=="POST":

        age=float(request.form["age"])
        resistance=float(request.form["resistance"])
        fc28=float(request.form["fc28"])

        res_28=calcul_fc28(resistance,age)

        conforme=res_28>=fc28

        result={
            "res_28":round(res_28,2),
            "fc28":fc28,
            "conforme":conforme
        }

    return render_template("fc28_en.html",result=result)


if __name__=="__main__":
    app.run(host="0.0.0.0",port=10000)
