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

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)


@app.route('/download')
def downloadFile ():
    from datetime import date, timedelta,datetime

    
    c_day = date.today()
    first_date = datetime(c_day.year, c_day.month, 1)
    print(" c_day.month---", c_day.month)
    if c_day.month!=12:
        last_date = datetime(c_day.year, c_day.month + 1, 1) + timedelta(days=-1)
    else:
        last_date = datetime(c_day.year+1,  1, 1) + timedelta(days=-1)
        
    start_dt = date(first_date.year,first_date.month,first_date.day)
    print(start_dt)
    end_dt = date(last_date.year,last_date.month,last_date.day)
    print(end_dt)
    lst=list()
    for dt in daterange(start_dt, end_dt):
        if dt.strftime("%A")!="Sunday":
            lst.append(dt.strftime("%d-%m-%Y %A"))
            lst.append(" ")
        else:
            lst.append(" ")
        
    df=pd.DataFrame(columns=lst)
    df.head()
    #file_name=dt.strftime("%m-%Y worsheet dates.xlsx")
    today = datetime.today()
    file_name=today.strftime("%m-%Y worsheet dates.xlsx")
    

    df.to_excel(file_name, encoding='utf8')  
    """
    c_day = date.today()
    first_date = datetime(c_day.year, c_day.month, 1)
    if c_day.month!=12:
        last_date = datetime(c_day.year, c_day.month + 1, 1) + timedelta(days=-1)
    else:
        last_date = datetime(c_day.year+1,  1, 1) + timedelta(days=-1)
            
    start_dt = date(first_date.year,first_date.month,first_date.day)
    print(start_dt)
    end_dt = date(last_date.year,last_date.month,last_date.day)
    print(end_dt)
    lst=list()
    for dt in daterange(start_dt, end_dt):
        if dt.strftime("%A")!="Sunday":
            lst.append(dt.strftime("%d-%m-%Y %A"))
            lst.append(" ")
        else:
            lst.append(" ")
        
    df=pd.DataFrame(columns=lst)
    today = datetime.today()
    yr=str(today.year)
    month=str( today.month)
    file_name=today.strftime("%m-%Y worsheet dates.xlsx")
    #file_name=yr+" "+month+" worsheet dates.xlsx"

    df.to_excel(file_name, encoding='utf8')  

        #For windows you need to use drive name [ex: F:/Example.pdf]
    #path = "C:/Downloads/"+file_name+".xlsx"
    #send_from_directory(directory=app.config['/'], filename=file_name)
    """    
    return send_file(file_name, as_attachment=True)
    

if __name__ == "__main__":
    app.run(debug=True)
    


