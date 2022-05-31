import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
from datetime import timedelta, date

from flask import send_file
import pandas as pd

"""
if __name__ == '__main__':
    app.run(port=5000,debug=True) 
"""

app = Flask(__name__) #Initialize the flask App
model = pickle.load(open('./models/lin_reg_model_v1.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    
    car_age=int(request.form.get("car_age"))
    km=int(request.form.get("car_age"))
    final_features = np.array([np.array([km,car_age])])
    car_price = model.predict(final_features)

    output = round(car_price[0], 2)

    return render_template('index.html', prediction_text='Car price should be  {}'.format(output))


def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)


@app.route('/download')
def downloadFile ():
    
    start_dt = date(2022, 6, 1)
    end_dt = date(2022, 6, 30)
    lst=list()
    for dt in daterange(start_dt, end_dt):
        if dt.strftime("%A")!="Sunday":
            lst.append(dt.strftime("%d-%m-%Y %A"))
            lst.append(" ")
        else:
            lst.append(" ")
        
    df=pd.DataFrame(columns=lst)
    file_name=dt.strftime("%m-%Y worsheet dates.xlsx")
    df.to_excel(file_name)  

        #For windows you need to use drive name [ex: F:/Example.pdf]
    #path = "C:/Downloads/"+file_name+".xlsx"
    #send_from_directory(directory=app.config['/'], filename=file_name)
    return send_file(file_name, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)