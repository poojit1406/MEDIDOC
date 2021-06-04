import os
import mysql.connector
from flask import Flask, render_template,redirect,request,session,flash


app = Flask(__name__)
app.secret_key = os.urandom(24)

conn = mysql.connector.connect(host="localhost", user="root",password="Z@ZJ[u@5X*piS2BU", database="users")
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
        return redirect('/home')
    else:
        return redirect('/')

@app.route('/add_user', methods=['post'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')


    cursor.execute("INSERT INTO `users` (`user_id`,`name`,`email`,`password`) VALUES (NULL,'{}','{}','{}')".format(name,email,password))
    conn.commit()

    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
    myuser = cursor.fetchall()
    session['user_id'] = myuser[0][0]

    flash(f"User registered successfully")
    return redirect('/home')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

@app.route('/disease')
def disease():
    return render_template('disease.html')

@app.route('/doctors_list')
def doctors():
    return render_template('doctors.html')

@app.route('/hospitals_list')
def hospitals():
    return render_template('hospitals.html')

if __name__ == '__main__':
    app.run(debug=True)
