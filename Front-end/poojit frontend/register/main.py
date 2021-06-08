from __future__ import division, print_function

import os
import glob
import re
import numpy as np
import mysql.connector

from werkzeug.utils import secure_filename

from flask import Flask, render_template,redirect,request,session,flash,url_for


from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image


from PIL import Image
from datetime import timedelta



app = Flask(__name__)



app.secret_key = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)

conn = mysql.connector.connect(host="localhost", user="root",password="V1RD4H8JBhQvrsF9", database="users")
cursor = conn.cursor()



@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login_validation', methods=['post'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    cursor.execute(""" SELECT * FROM  `users`  WHERE  `email` LIKE '{}' AND  `password` LIKE  '{}' """
                    .format(email,password))
    users = cursor.fetchall()

    if len(users)>0:
        session['user_id'] = users[0][0]
        session.permanent = True
        return redirect('/home')
    else:
        return redirect('/')

@app.route('/add_user', methods=['post'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')


    cursor.execute("INSERT INTO `users` (`user_id`,`FullName`,`Email`,`password`) VALUES (NULL,'{}','{}','{}')".format(name,email,password))
    conn.commit()

    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
    myuser = cursor.fetchall()
    session['user_id'] = myuser[0][0]

    flash(f"User registered successfully")
    return redirect('/home')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home', methods=['get'])
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')




model = load_model(r'C:\Users\Poojit\Desktop\register\models\model_malaria.h5', compile=False)


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(134, 131))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    ## Scaling
    #x=x/255
    x = np.expand_dims(x, axis=0)


    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    x = preprocess_input(x)

    preds = model.predict(x)
    preds=np.argmax(preds, axis=-1)
    if preds==0:
        preds="The Person is Infected With Malaria"
    else:
        preds="The Person is not Infected With Malaria"


    return preds


@app.route('/home/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        result=preds
        return result
    return None



@app.route('/doctors_list')
def doctors():
    return render_template('doctors.html')

@app.route('/hospitals_list')
def hospitals():
    return render_template('hospitals.html')

@app.route('/contact')
def contact():
    return render_template('contact_us.html')

@app.route('/connect_doctor')
def connect_doctor():
    return render_template('connect_doctor.html')

@app.route('/about_us')
def about():
    return render_template('about_us.html')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')




if __name__ == '__main__':
    app.run(debug=True)
