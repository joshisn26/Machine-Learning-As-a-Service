from flask import Flask, render_template, request, session, redirect, url_for
from forms import predictionForm
from forms import classificationForm
import json
import urllib.request


app = Flask(__name__)
app.secret_key = "mysec-key"

def linear(body, output):
	#Linear Regression
	url = 'https://ussouthcentral.services.azureml.net/workspaces/7a01f9d6cb9b4df09ebc6b306c3a06f0/services/2a4594c77fb147ef9876506f4dc66e9d/execute?api-version=2.0&format=swagger'
	api_key = 'JhBn9dZ907p1ZbJHk+UflP7pDvANyha/8aOH6sk+T06wJwU+bcXdtW+bH4B7c8CKo+ivDtsH+m4cpXUAoMVh2A==' 
	headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

	req = urllib.request.Request(url, body, headers)

	try:
		response = urllib.request.urlopen(req)

		result = response.read()
		response_dict = json.loads(result)
		output.append(response_dict['Results']['output1'][0]["Scored Labels"])
		est_int_rate = response_dict['Results']['output1'][0]["Scored Labels"]
		print("Interest rate using linear regression: ", est_int_rate)
	except urllib.error.HTTPError as error:
		print("The request failed with status code: " + str(error.code))

		# Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
		print(error.info())
		print(json.loads(error.read().decode("utf8", 'ignore')))
				
def random_forest(body, output):
	#Random Forest
	url = 'https://ussouthcentral.services.azureml.net/workspaces/7a01f9d6cb9b4df09ebc6b306c3a06f0/services/0a8caca2172f484db41147b2fc11b1e8/execute?api-version=2.0&format=swagger'
	api_key = 'pJe/ZBkwkI9qdrrSJYaCG28QOQTYot3STfGdXqY0ewJr4nSTk8hJa16JelDGvi4vv7QKwdiCB336Y+FH/zWomw==' # Replace this with the API key for the web service
	headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
	req = urllib.request.Request(url, body, headers)

	try:
		response = urllib.request.urlopen(req)
		result = response.read()
		response_dict = json.loads(result)
		output.append(response_dict['Results']['output1'][0]["Scored Label Mean"])
		est_int_rate = response_dict['Results']['output1'][0]["Scored Label Mean"]
		print("Interest rate using random forest: ", est_int_rate)
	except urllib.error.HTTPError as error:
		print("The request failed with status code: " + str(error.code))

		# Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
		print(error.info())
		print(json.loads(error.read().decode("utf8", 'ignore')))
	
def Neural_net(body, output):
	#Neural Network
	url = 'https://ussouthcentral.services.azureml.net/workspaces/7a01f9d6cb9b4df09ebc6b306c3a06f0/services/c945809ba42c402694e09f804d1cdce9/execute?api-version=2.0&format=swagger'
	api_key = 'lo37PdM3tV+SuONo7etDvYldNN7ApcD0GHcqTCtFXAb71ZG5/qcBuDwO6BrzL5EZGa0d5U3H8c/0pH2R+c513A==' # Replace this with the API key for the web service
	headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
	req = urllib.request.Request(url, body, headers)

	try:
		response = urllib.request.urlopen(req)
		result = response.read()
		response_dict = json.loads(result)
		output.append(response_dict['Results']['output1'][0]["Scored Labels"])
		est_int_rate = response_dict['Results']['output1'][0]["Scored Labels"]
		print("Interest rate using Neural Network: ", est_int_rate)
	except urllib.error.HTTPError as error:
		print("The request failed with status code: " + str(error.code))
		# Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
		print(error.info())
		print(json.loads(error.read().decode("utf8", 'ignore')))
        
@app.route("/prediction", methods =["GET" , "POST"])
def prediction():
    form = predictionForm()
    if request.method == "POST":
        cn = form.id.data
        credit_score = form.credit_score.data
        first_payment_date = form.first_payment_date.data
        fthb_flag = form.fthb_flag.data
        matr_date = form.matr_date.data
        msa = form.msa.data
        mortage_insurance_pct = form.mortage_insurance_pct.data
        no_of_units = form.no_of_units.data
        occupancy_status = form.occupancy_status.data
        cltv = form.cltv.data
        dti_ratio = form.dti_ratio.data
        original_upb = form.original_upb.data

        data = {	
            "Inputs": {
                "input1":
                [
                    {
                        'credit_score': credit_score,   
                        'first_payment_date': first_payment_date,   
                        'fthb_flag': fthb_flag,   
                        'matr_date': matr_date,   
                        'msa': msa,   
                        'mortage_insurance_pct': mortage_insurance_pct,   
                        'no_of_units': no_of_units,   
                        'occupancy_status': occupancy_status,   
                        'cltv': cltv,   
                        'dti_ratio': dti_ratio,   
                        'original_upb': original_upb, 
                    }
                ],
            },
            "GlobalParameters":  {
            }
        }
        body = str.encode(json.dumps(data))
        output = []
        linear(body,output)
        random_forest(body,output)
        Neural_net(body,output)
        print("case" , cn)
        return render_template("success.html", pred_int_rate = output, caseno = cn)
    elif request.method == 'GET':
        return render_template('prediction.html',form=form)
    
def logistic(body, output):
    url = 'https://ussouthcentral.services.azureml.net/workspaces/d94007c736f1444eac6bbe2e88d68fcb/services/5eb9a74b8cbc466c8ba79b7af04ea315/execute?api-version=2.0&format=swagger'
    api_key = 'NhQPvmod33VeXkZ3KvmdAYAbIpq/PXNF9cwJ+n/3+yGQZNRgeOQeH7xA6z/kyVwMr5r2YGzxojnb9dFipmGUXw=='
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req).read().decode('utf8')

        #result = response.read()
        
        #reader = codecs.getreader("utf-8")
        response_dict = json.loads(response)
        #response_dict = req.json()
        output.append(response_dict['Results']['output1'][0]["current_int_rate"])
        int_rate = response_dict['Results']['output1'][0]["current_int_rate"]
        output.append(response_dict['Results']['output1'][0]["current_actual_upb"])
        upb = response_dict['Results']['output1'][0]["current_actual_upb"]
        output.append(response_dict['Results']['output1'][0]["Deliquent"])
        deliq = response_dict['Results']['output1'][0]["Deliquent"]
        output.append(response_dict['Results']['output1'][0]["Scored Probabilities for Class " + '"0"'])
        scored_0 = response_dict['Results']['output1'][0]["Scored Probabilities for Class " + '"0"']
        output.append(response_dict['Results']['output1'][0]["Scored Probabilities for Class " + '"1"'])
        scored_1 = response_dict['Results']['output1'][0]["Scored Probabilities for Class " + '"1"']
        output.append(response_dict['Results']['output1'][0]["Scored Labels"])
        scored_labels = response_dict['Results']['output1'][0]["Scored Labels"]
        print("Scored Labels using Logistic Regression: ", scored_labels)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))

def decision_forest(body, output):
    #Decision Forest
    url = 'https://ussouthcentral.services.azureml.net/workspaces/d94007c736f1444eac6bbe2e88d68fcb/services/c69d12716ecc4203a2f90b8d076fc64b/execute?api-version=2.0&format=swagger'
    api_key = 'DDAS5zhcE8i3Gq5XO/IGZBjpT5BDKBIw/oiwQyriKB4Dli6ksvnKFv7wnFbgJAG8R2IKpicArapjvqaVCyKgwA=='
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req).read().decode('utf8')
        #result = response.read()
        response_dict = json.loads(response)
        output.append(response_dict['Results']['output1'][0]["Scored Probabilities"])
        scored_prob = response_dict['Results']['output1'][0]["Scored Probabilities"]
        output.append(response_dict['Results']['output1'][0]["Scored Labels"])
        scored_labels = response_dict['Results']['output1'][0]["Scored Labels"]
        print("Scored Labels using Decision Forest: ", scored_labels)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))

def Neural_network(body, output):
    #Neural Network
    url = 'https://ussouthcentral.services.azureml.net/workspaces/d94007c736f1444eac6bbe2e88d68fcb/services/6070be542620413ebfe78c24dd764a4e/execute?api-version=2.0&format=swagger'
    api_key = 'IdIQCP4i4gVVxQHhfY7Qs+JQmV/5JkTHavKAjSx0SHOfPIZUx9ZQdQZu+nNXCxuwvPOTXOGdUM7I3KiYoSC8KQ=='
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req).read().decode('utf8')
        #result = response.read()
        response_dict = json.loads(response)
        output.append(response_dict['Results']['output1'][0]["Scored Probabilities"])
        scored_prob = response_dict['Results']['output1'][0]["Scored Probabilities"]
        output.append(response_dict['Results']['output1'][0]["Scored Labels"])
        scored_labels = response_dict['Results']['output1'][0]["Scored Labels"]
        print("Scored Labels using Neural Network: ", scored_labels)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))
        
@app.route("/classification", methods =["GET" , "POST"])
def classification():
    form = classificationForm()
    if request.method == "POST":
        cn = form.id.data
        month = form.month.data
        current_actual_upb = form.current_actual_upb.data
        delq_status = form.delq_status.data
        loan_age = form.loan_age.data
        rem_months = form.rem_months.data
        zero_balance_code = form.zero_balance_code.data
        zero_bal_date = form.zero_bal_date.data
        current_int_rate = form.current_int_rate.data
        current_def_upb = form.current_def_upb.data
        ddlpi = form.ddlpi.data
        mi_recoveries = form.mi_recoveries.data
        net_sales_proceeds = form.net_sales_proceeds.data
        non_mi_recoveries = form.non_mi_recoveries.data
        expenses = form.expenses.data
        legal_costs = form.legal_costs.data
        maint_pres_costs = form.maint_pres_costs.data
        taxes_ins = form.taxes_ins.data
        misc_expenses = form.misc_expenses.data
        actual_loss_calc = form.actual_loss_calc.data
        modification_cost = form.modification_cost.data
        repurchase_flag_0 = form.repurchase_flag_0.data
        repurchase_flag_N = form.repurchase_flag_N.data
        repurchase_flag_Y = form.repurchase_flag_Y.data
        modification_flag_0 = form.modification_flag_0.data
        modification_flag_Y = form.modification_flag_Y.data
        Deliquent = form.Deliquent.data

        data = {
                "Inputs": {
                        "input1":
                        [
                            {
                                    'month': month,   
                                    'current_actual_upb': current_actual_upb,   
                                    'delq_status': delq_status,   
                                    'loan_age': loan_age,   
                                    'rem_months': rem_months,   
                                    'zero_balance_code': zero_balance_code,   
                                    'zero_bal_date': zero_bal_date,   
                                    'current_int_rate':current_int_rate ,   
                                    'current_def_upb': current_def_upb,   
                                    'ddlpi': ddlpi,   
                                    'mi_recoveries': mi_recoveries,   
                                    'net_sales_proceeds': net_sales_proceeds,   
                                    'non_mi_recoveries': non_mi_recoveries,   
                                    'expenses': expenses,   
                                    'legal_costs': legal_costs,   
                                    'maint_pres_costs': maint_pres_costs,   
                                    'taxes_ins': taxes_ins,   
                                    'misc_expenses': misc_expenses,   
                                    'actual_loss_calc': actual_loss_calc,   
                                    'modification_cost': modification_cost,   
                                    'repurchase_flag_0': repurchase_flag_0,   
                                    'repurchase_flag_N': repurchase_flag_N,   
                                    'repurchase_flag_Y': repurchase_flag_Y,   
                                    'modification_flag_0': modification_flag_0,   
                                    'modification_flag_Y': modification_flag_Y,   
                                    'Deliquent': Deliquent,   
                            }
                        ],
                },
            "GlobalParameters":  {
            }
        }

        body = str.encode(json.dumps(data))
        output = []
        logistic(body,output)
        decision_forest(body,output)
        Neural_network(body,output)
        print("case" , cn)
        return render_template("submit.html", values = output, caseno = cn)
    elif request.method == 'GET':
        return render_template('classification.html',form=form)
        
@app.route("/")
def home():
    return render_template('mainpage.html', context={})


if __name__ == "__main__":
  app.run(debug=True)