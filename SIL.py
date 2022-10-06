from flask import Flask, render_template,request, redirect, url_for
import numpy as np
import pickle

app = Flask(__name__)

with open("standard_scaler.pickle", "rb") as input_file:
    scaler = pickle.load(input_file) 

with open("random_forest.pickle", "rb") as input_file:
    rd = pickle.load(input_file) 


@app.route("/", methods=["POST", "GET"]) 
def home():
    if request.method == "POST":
        #Get input
        Gender = request.form["Gender"]
        Maried = request.form["Married"]
        dependents = request.form["dependents"]
        Graduate = request.form["Graduate"]
        Employed = request.form["Employed"]
        applicant_income = request.form["applicant_income"]
        coapplicant_income = request.form["coapplicant_income"]
        loan_amount = request.form["loan_amount"]
        loan_amountt_term = request.form["loan_amountt_term"]
        property_area = request.form["property_area"]

        #Encoding
        Gender = encoding_gender(Gender)
        Maried = encoding_bool(Maried)
        dependents = encoding_dependents(dependents)
        Graduate = encoding_graduate(Graduate)
        Employed = encoding_bool(Employed)
        applicant_income = convert_to_dolar(applicant_income)
        coapplicant_income = convert_to_dolar(coapplicant_income)
        loan_amount = convert_loan_amount(loan_amount)
        loan_amountt_term = float(loan_amountt_term)
        property_area = encoding_property(property_area)
        
        #Make nparray
        
        array = np.array([Gender, Maried, dependents, Graduate, Employed, applicant_income
                        ,coapplicant_income,loan_amount,loan_amountt_term, property_area])
        
        array = array.reshape(1,-1)

        test =  scaler.transform(array)
        
        y_pred = rd.predict(test)
        
        Loan_Status = int(np.squeeze(y_pred))

        Status = ""
        if(Loan_Status == 0):
            Status = "No"
        else:
            Status = "Yes" 
            
        print(y_pred)
        return redirect(url_for("value", status = Status))
    else:	
        return render_template("SIL.html") 

@app.route("/<status>")
def value(status):
    return render_template("tes.html", content = [status])

def convert_to_dolar(Rp):
    value = int(Rp)/14500
    return round(float(value),3)

def convert_loan_amount(loan_amount):
    value = int(loan_amount)/14500000
    return round(float(value),3)

def encoding_gender(gender):
    if gender == "Female":
        return float(0)
    else:
        return float(1)

def encoding_bool(boolean):
    if boolean == "No":
        return float(0)
    else:
        return float(1)

def encoding_dependents(dependets):
    if dependets == "3+":
        return float(3)
    else:
        return float(dependets)

def encoding_bool(boolean):
    if boolean == "No":
        return float(0)
    else:
        return float(1)

def encoding_graduate(graduate):
    if graduate == "Undergraduate":
        return float(0)
    else:
        return float(1)

def encoding_property(property):
    if property == "Rural":
        return float(0)
    elif property == "Semiurban":
        return float(1)
    else:
        return float(2)


if __name__ == "__main__":
    app.run()