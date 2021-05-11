from flask import Flask,request,render_template,redirect
import os
import sqlite3
import random
import string
import hashlib
currentlocation=os.path.dirname(os.path.abspath(__file__))

myapp=Flask(__name__)

@myapp.route("/")
def homepage():
    return render_template("homepage.html")

@myapp.route("/", methods = ['POST'])
def checklogin():
    UN=request.form['username']
    PW=request.form['password']
    currentUser = hashlib.sha256(UN.encode('utf-8')).hexdigest()
    currentHash = hashlib.sha256(PW.encode('utf-8')).hexdigest()

    sqlconnnection=sqlite3.Connection(currentlocation+"\login.db")
    cursor=sqlconnnection.cursor()
    query1="SELECT password FROM users WHERE username='{un}'".format(un=currentUser)

    rows=cursor.execute(query1)
    rows=rows.fetchone()
    if len(rows)==1:
        fetechedHash=rows[0]
        if fetechedHash==currentHash:
            return render_template("loggedin.html")
        else:
            print("User not found! Please register") 
    else:
        print("User not found! Please register")

def gen_user(username):
    return username[0:3]+str(random.randint(10000,99999))
def gen_pwd():
    password_characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(password_characters) for i in range(8))
    return password
@myapp.route("/register", methods = ["GET","POST"])
def registerpage():

    if request.method=="POST":
        nam=request.form['name']
        contact=request.form['contact']
        dUN=gen_user(nam)
        dPW=gen_pwd()
        currentUser = hashlib.sha256(dUN.encode('utf-8')).hexdigest()
        currentPassword = hashlib.sha256(dPW.encode('utf-8')).hexdigest()
        result="user name:"+dUN+"\n"+" Password:"+dPW
        Uemail=request.form['useremail']
        print("ok")
        sqlconnnection=sqlite3.Connection(currentlocation+"\login.db")
        cursor=sqlconnnection.cursor()
        query1="INSERT INTO users VALUES('{n}','{c}','{u}','{p}','{e}')".format(u=currentUser,p=currentPassword,e=Uemail,n=nam,c=contact)
        cursor.execute(query1)
        sqlconnnection.commit()
        return render_template("homepage.html", data=result)
    return render_template("register.html")



if __name__=="__main__":
    myapp.run()
