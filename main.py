from datetime import datetime
import pickle
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__, template_folder='html', static_folder='AllCss')
app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'M$8ni3y0'
app.config['MYSQL_DB'] = 'new_schema'

mysql = MySQL(app)

model = pickle.load(open('models/XGBOOST_model.pkl', 'rb'))


@app.route('/')
@app.route('/html/index.html')
def index():
    return render_template('index.html')


@app.route('/html/login.html', methods=['GET', 'POST'])
def login():
    global msg
    msg = ''
    print(request.method)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_information WHERE email = % s AND password = % s', (email, password,))
        record = cursor.fetchone()
        if record:
            session['patient_id'] = record['patient_id']
            session['TIME_DATE'] = str(record['TIME_DATE'])
            return redirect(url_for('page'))
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/html/register.html', methods=['GET', 'POST'])
def register():
    msg = ''
    print(request.method)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_information WHERE email = % s', (email,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', password):
            msg = 'Username must contain only characters and numbers !'
        elif not email or not password:
            msg = 'Please fill out the form ! 1'
        else:
            cursor.execute('INSERT INTO user_information VALUES (NULL, % s, % s, %s, NULL)',
                           (email, password, datetime.now()))
            mysql.connection.commit()

            cursor.execute('SELECT * FROM user_information WHERE email = % s', (email,))
            record = cursor.fetchone()
            print(record)
            sql = "UPDATE user_information SET id = {} WHERE patient_id = {}".format(record['patient_id'],
                                                                                     record['patient_id'])
            cursor.execute(sql)
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    return render_template('register.html', msg=msg)


@app.route('/html/history.html', methods=["GET", "POST"])
def history():
    print("history#########")
    print(request.method)
    print(session['patient_id'])
    global listOfPatientDates
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = 'SELECT * FROM results WHERE ID = {}'.format(session['patient_id'])
        cursor.execute(sql)
        record = cursor.fetchall()
        listOfPatientDates = []
        listOfPatientResults = []
        for i in range(len(record)):
            print(record[i]['time_date'])
            date_only = str(pd.to_datetime(record[i]['time_date'], format='%Y-%m-%d')).split(' ')[0]
            listOfPatientDates.append(date_only)

            listOfPatientResults.append(record[i]['result'])
    elif request.method == "POST":
        print(request.form['dd'])
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = "SELECT result FROM results WHERE ID = {} AND time_date = '{}'".format(session['patient_id'],
                                                                                     request.form['dd'].strip())
        print(sql)
        cursor.execute(sql)
        record = cursor.fetchall()
        print(record[0]['result'])
        return render_template('history.html', listOfPatientDates=listOfPatientDates, result=record[0]['result'])
    print(listOfPatientDates)
    return render_template('history.html', listOfPatientDates=listOfPatientDates)


@app.route('/html/page.html')
def page():
    return render_template('page.html')


@app.route('/html/symptoms.html')
def symptoms():
    return render_template('symptoms.html')


@app.route('/html/blood_test_form.html', methods=["GET", "POST"])
def blood_test():
    list_ = []
    global age
    global sex
    global on_thyroxine
    global query_on_thyroxine
    global on_antithyroid_meds
    global sick
    global pregnant
    global thyroid_surgery
    global I131_treatment
    global query_hypothyroid
    global query_hyperthyroid
    global lithium
    global goitre
    global tumor
    global hypopituitary
    global psych
    global TSH
    global T3
    global TT4
    global T4U
    global FTI
    global diseaseNames
    print(request.method)
    if request.method == "GET":
        return render_template('blood_test_form.html')
    elif request.method == 'POST':
        age = int(request.form['age'])
        sex = int(request.form['sex'])
        on_thyroxine = int(request.form['on_thyroxine'])
        query_on_thyroxine = int(request.form['query_on_thyroxine'])
        on_antithyroid_meds = int(request.form['on_antithyroid_meds'])
        sick = int(request.form['sick'])
        pregnant = int(request.form['pregnant'])
        thyroid_surgery = int(request.form['thyroid_surgery'])
        I131_treatment = int(request.form['I131_treatment'])
        query_hypothyroid = int(request.form['query_hypothyroid'])
        query_hyperthyroid = int(request.form['query_hyperthyroid'])

        lithium = int(request.form['lithium'])
        goitre = int(request.form['goitre'])
        tumor = int(request.form['tumor'])
        hypopituitary = int(request.form['hypopituitary'])
        psych = int(request.form['psych'])
        TSH = float(request.form['TSH'])
        T3 = float(request.form['T3'])
        TT4 = float(request.form['TT4'])
        T4U = float(request.form['T4U'])
        FTI = float(request.form['FTI'])

        list_.append(age)
        list_.append(sex)
        list_.append(on_thyroxine)
        list_.append(query_on_thyroxine)
        list_.append(on_antithyroid_meds)
        list_.append(sick)
        list_.append(pregnant)
        list_.append(thyroid_surgery)
        list_.append(I131_treatment)
        list_.append(query_hypothyroid)
        list_.append(query_hyperthyroid)
        list_.append(lithium)
        list_.append(goitre)
        list_.append(tumor)
        list_.append(hypopituitary)
        list_.append(psych)
        list_.append(TSH)
        list_.append(T3)
        list_.append(TT4)
        list_.append(T4U)
        list_.append(FTI)
        k = np.array([list_])
        x = model.predict(k)
        if x == [0]:
            diseaseNames = "negative"
        elif x == [1]:
            diseaseNames = "hyperthyroid"
        elif x == [2]:
            if 4.75 < k[0][16] <= 10:
                diseaseNames = "subclinical hypothyroid"
            elif 10 < k[0][16] <= 25:
                diseaseNames = "moderate hypothyroid"
            elif k[0][16] > 25:
                diseaseNames = "severe hypothyroid"
        diseaseNames = "severe hypothyroid"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = "INSERT INTO results VALUES ({}, '{}', '{}', NULL)".format(session['patient_id'], diseaseNames,
                                                                         datetime.now().date(), )
        cursor.execute(sql)
        mysql.connection.commit()
    return render_template('blood_test_form.html',
                           age=age,
                           sex=sex,
                           on_thyroxine=on_thyroxine,
                           query_on_thyroxine=query_on_thyroxine,
                           on_antithyroid_meds=on_antithyroid_meds,
                           sick=sick,
                           pregnant=pregnant,
                           thyroid_surgery=thyroid_surgery,
                           I131_treatment=I131_treatment,
                           query_hypothyroid=query_hypothyroid,

                           query_hyperthyroid=query_hyperthyroid,
                           lithium=lithium,
                           goitre=goitre,
                           tumor=tumor,
                           hypopituitary=hypopituitary,
                           psych=psych,
                           TSH=TSH,
                           T3=T3,
                           TT4=TT4,
                           T4U=T4U,
                           FTI=FTI,
                           diseaseNames=diseaseNames
                           )


if __name__ == "__main__":
    app.run()
