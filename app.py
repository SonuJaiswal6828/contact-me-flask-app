from flask import Flask, render_template, request, flash, redirect, session
import os
#=========================================================================================================
import pyrebase
config = {
  "apiKey": "",
  "authDomain": os.getenv("FB_API_KEY"),
  "projectId": "first-flask-app-dbcbf",
  "storageBucket": "first-flask-app-dbcbf.firebasestorage.app",
  "messagingSenderId": "119762745195",
  "appId": "1:119762745195:web:98b2efa22378cc9838be2e",
  "databaseURL": os.getenv("FB_DB_URL")
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

#=========================================================================================================
app =Flask(__name__)
app.secret_key = "sonu123"

@app.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        data = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message
        }
        db.child("Messages").push(data)
        flash("Your message sent successfully")
    return render_template('index.html')

@app.route('/admin')
def admin():
    if 'user' not in session:
        return redirect('/login')
    all_enteries = db.child("Messages").get()
    return render_template('admin.html', all_enteries = all_enteries)

@app.route("/response/<string:pushkey>/",methods=['GET','POST'])
def response(pushkey):
    data = db.child("Messages").child(pushkey).get().val()
    return render_template('response.html', pushkey=pushkey, data=data)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('pass')
        email = request.form.get('email')
        if password == 'password' and email == os.getenv("ADMIN_EMAIL"):
            session['user'] = email
            return redirect('/admin')
        else: 
            return redirect('/login')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('login.html')

if __name__ == '__main__':
    app.run(debug=True)