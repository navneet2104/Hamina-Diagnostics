from flask import Flask,render_template,request
import mysql.connector
import os
import numpy as np
import pickle

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("home.html")

@app.route('/h')
def h1():
    return render_template("form1.html")

@app.route('/hi')
def h3():
    return render_template("result.html")


@app.route('/regu',methods=["POST"])
def h2():
    name = str(request.form['fname'])
    name1 = str(request.form['lname'])
    email = str(request.form['email'])
    phone = str(request.form['phone'])
    Pass = str(request.form['psw'])


    con = mysql.connector.connect(host="localhost",user="root",password="",db="heart")

    cur = con.cursor()
    cur.execute("insert into table1 values ('"+name+"','"+name1+"','"+email+"','"+phone+"','"+Pass+"')")
    con.commit()

    return render_template("result.html")

#prediction function
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1,13)
    loaded_model = pickle.load(open("model/heart_model.pkl","rb"))
    result = loaded_model.predict(to_predict)
    return result[0]
   


@app.route('/result',methods = ['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list=list(to_predict_list.values())
        to_predict_list = list(map(int, to_predict_list))
        result = ValuePredictor(to_predict_list)
        
        if int(result)==1:
            prediction='ABNORMAL'
        else:
            prediction='NORMAL'
        from keras import backend as K
        K.clear_session()
            
        return render_template("result1.html",prediction=prediction)

if __name__ == '__main__':
    app.run()
