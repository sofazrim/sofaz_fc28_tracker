from flask import Flask, render_template, request
from datetime import datetime, timedelta
import pandas as pd
from fpdf import FPDF

app = Flask(__name__)

def calcul_fc28(res_jour, age):
    return res_jour * (28/age)**0.5

@app.route('/')
def home():
    return render_template('index_fr.html')

@app.route('/en')
def home_en():
    return render_template('index_en.html')

@app.route('/fc28/fr', methods=['GET','POST'])
def fc28_fr():
    result = None
    conforme = False
    if request.method=='POST':
        date_str = request.form['date']
        age = int(request.form['age'])
        res_jour = float(request.form['resistance'])
        fc28 = float(request.form['fc28'])
        res_28 = calcul_fc28(res_jour, age)
        date_test = (datetime.strptime(date_str, '%d/%m/%Y') + timedelta(days=age)).strftime('%d/%m/%Y')
        conforme = res_28 >= fc28
        result = {'date_test':date_test,'res_28':round(res_28,2),'fc28':fc28,'conforme':conforme}

        df = pd.DataFrame([{
            "Date de coulage": date_str,
            "Âge (j)": age,
            "Date du test": date_test,
            "Résistance mesurée (MPa)": res_jour,
            "Résistance estimée à 28j (MPa)": round(res_28,2),
            "Fc28 projet": fc28,
            "Conforme": "Oui" if conforme else "Non"
        }])
        try:
            old_df = pd.read_csv("historique_fc28.csv")
            df = pd.concat([old_df, df], ignore_index=True)
        except FileNotFoundError:
            pass
        df.to_csv("historique_fc28.csv", index=False)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", size=14)
        pdf.cell(200,10,"Rapport - SOFAZ Fc28 Tracker (TM)",align='C',ln=1)
        pdf.cell(200,10,"Développé par Ing. Fathi ZERRIOUH",align='C',ln=1)
        for k,v in df.iloc[-1].items():
            pdf.cell(80,10,str(k))
            pdf.cell(110,10,str(v),ln=1)
        pdf.output("rapport_fc28.pdf")
    return render_template('fc28_fr.html', result=result, conforme=conforme)

@app.route('/fc28/en', methods=['GET','POST'])
def fc28_en():
    result = None
    conforme = False
    if request.method=='POST':
        date_str = request.form['date']
        age = int(request.form['age'])
        res_jour = float(request.form['resistance'])
        fc28 = float(request.form['fc28'])
        res_28 = calcul_fc28(res_jour, age)
        date_test = (datetime.strptime(date_str, '%d/%m/%Y') + timedelta(days=age)).strftime('%d/%m/%Y')
        conforme = res_28 >= fc28
        result = {'date_test':date_test,'res_28':round(res_28,2),'fc28':fc28,'conforme':conforme}
    return render_template('fc28_en.html', result=result, conforme=conforme)

if __name__=="__main__":
    app.run(debug=True)
