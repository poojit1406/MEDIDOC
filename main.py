import os
import numpy as np
import mysql.connector

from flask import Flask, render_template,redirect,request,session,flash,url_for

from tensorflow.keras.models import load_model
from tensorflow.keras.applications.imagenet_utils import preprocess_input


from PIL import Image
from datetime import timedelta



app = Flask(__name__)



app.secret_key = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=5)

conn = mysql.connector.connect(host="localhost", user="root",password="9MZtQaMPCAFGLVgG", database="users")
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


@app.route("/malaria", methods=['GET', 'POST'])
def malariaPage():
    return render_template('malaria.html')

@app.route("/pneumonia", methods=['GET', 'POST'])
def pneumoniaPage():
    return render_template('pneumonia.html')

@app.route("/brain", methods=['GET', 'POST'])
def brainPage():
    return render_template('brain.html')




@app.route("/malariapredict", methods = ['POST', 'GET'])
def malariapredictPage():
    if request.method == 'POST':
        try:
            if 'image' in request.files:
                img = Image.open(request.files['image'])
                img = img.resize((36,36))
                img = np.asarray(img)
                img = img.reshape((1,36,36,3))
                img = img.astype(np.float64)
                model = load_model("models/malaria.h5")
                preds = np.argmax(model.predict(img)[0])
        except:
            message = "Please upload an Image"
            return render_template('malaria.html', message = message)
    return render_template('malaria_predict.html', preds = preds)

@app.route("/pneumoniapredict", methods = ['POST', 'GET'])
def pneumoniapredictPage():
    if request.method == 'POST':
        try:
            if 'image' in request.files:
                img = Image.open(request.files['image']).convert('L')
                img = img.resize((36,36))
                img = np.asarray(img)
                img = img.reshape((1,36,36,1))
                img = img / 255.0
                model = load_model("models/pneumonia.h5")
                pred = np.argmax(model.predict(img)[0])
        except:
            message = "Please upload an Image"
            return render_template('pneumonia.html', message = message)
    return render_template('pneumonia_predict.html', pred = pred)

model = load_model(r'C:\Users\Poojit\Desktop\new\models\tumor_prediction.h5', compile=False)

@app.route("/brainpredict", methods = ['POST', 'GET'])
def brainpredictPage():

    if request.method == 'POST' and 'image' in request.files:

        img = Image.open(request.files['image'])
        img = img.resize((224,224))
        img = np.expand_dims(img, axis=0)
        img_data= preprocess_input(img)
        preds = model.predict(img_data)

        if preds[0][0] >= 0.9:
            prediction = 'This MRI Scan does not have Brain Tumor.'
        elif preds[0][0] < 0.9:
            prediction = 'This MRI Scan is predicted to have Brain Tumor, Please Consult to the Doctor.'

        return render_template('brain_predict.html', prediction=prediction)

    else:
        message = "Please upload an image"
        return render_template('brain.html', message=message)


@app.route('/doctors_list')
def doctorsPage():
    return render_template('doctors.html')

@app.route('/hospitals_list')
def hospitalsPage():
    return render_template('hospitals.html')

@app.route('/contact')
def contactPage():
    return render_template('contact_us.html')

@app.route('/connect_doctor')
def connect_doctorPage():
    return render_template('connect_doctor.html')

@app.route('/about_us')
def about_usPage():
    return render_template('about_us.html')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')



if __name__ == '__main__':
    app.run()
