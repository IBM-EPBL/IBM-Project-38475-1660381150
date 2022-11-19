from flask import Flask, render_template, request
import requests
API_KEY = "ZjtjnasbVVMxbYlv_gJwkT0XaO-bc8W61Qu6I3DMcV1w"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app = Flask(__name__,template_folder='templates')

#  template_folder='templates'

@app.route('/')

def home():
    return render_template('home.html')
@app.route('/procedure.html')
def procedure():
    return render_template('procedure.html')
@app.route('/About.html')
def about():
    return render_template('About.html')
@app.route('/terms.html')
def terms():
    return render_template('terms.html')


@app.route('/home.html')
def home1():
    return render_template('home.html')
@app.route('/predict.html')
def formpg():
    return render_template('predict.html')
@app.route('/rating.html')
def rat():
    return render_template('rating.html')
@app.route('/predict.html',methods = ['POST'])
def predict():
    if request.method == "POST":
        gender = request.form['genderBox']
        married = request.form['maritalBox']
        dependents = request.form['dependents']
        education = request.form['educationBox']
        employment = request.form['employmentBackground']
        applicant_income = request.form['applicantIncomeBox']
        coapplicant_income = request.form['coApplicantIncomeBox']
        loan_amount = request.form['laonAmtBox']
        loan_amount_term = request.form['laonAmtTermBox']
        credit_history = request.form['CHBox']
        prop_area = request.form['propertyAreaBox']

        if gender == 'Male':
            gender = 1
        else:
            gender = 0

        if married == 'Yes':
            married = 1
        else:
            married = 0

        if dependents == '0':
            dependents = 0
        elif dependents == '1':
            dependents = 1
        elif dependents == '2':
            dependents = 2
        else:
            dependents = 3

        if education == 'Graduate':
            education = 0
        else:
            education = 1

        if employment == 'Yes':
            employment = 1
        else:
            employment = 0
        if credit_history=='Yes':
            credit_history=1
        else:
            credit_history=0
        if prop_area == 'Rural':
            prop_area = 0
        elif prop_area == 'Semiurban':
            prop_area = 1
        else:
            prop_area = 2

        
        x=[[gender,married,dependents, education, employment,applicant_income,coapplicant_income,loan_amount, loan_amount_term,credit_history,prop_area]]

        payload_scoring = {"input_data": [{"fields": [[gender,married,dependents, education, employment,applicant_income,coapplicant_income,loan_amount, loan_amount_term,credit_history,prop_area]], "values":x}]}
        
        
        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/baba8f25-3302-4fd0-b3f1-fe22b1475644/predictions?version=2022-11-19',
        headers={'Authorization': 'Bearer ' + mltoken})


        print("Scoring response")
        prediction=response_scoring.json()
        print(response_scoring.json())
        if(prediction=="N"):
            prediction="No"
        else :
            prediction="Yes"
            return render_template('approve.html',prediction_text ='Congratulations! '+' You are eligible for loan')
            # return render_template("predict.html", prediction_text="Congratulations Your Loan Status is {}".format(prediction))

        
    else:
         return render_template('reject.html',prediction_text ='sorry '+' You are not eligible for loan')
    

    


if __name__ == "__main__":
    app.run(debug=True)