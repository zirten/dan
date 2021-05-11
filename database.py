from flask import Flask,request,render_template,redirect
import os
import sqlite3

currentlocation=os.path.dirname(os.path.abspath(__file__))
myapp=Flask(__name__)

@myapp.route("/")

def homepage():
    return render_template("homepage.html")

@myapp.route("/", methods = ['POST'])
def checklogin():
    UN=request.form['username']
    PW=request.form['password']

    sqlconnnection=sqlite3.Connection(currentlocation+"\login.db")
    cursor=sqlconnnection.cursor()
    query1="SELECT username, password FROM users WHERE username={un} AND password={pw}".format(un=UN,pw=PW)

    rows=cursor.execute(query1)
    rows=rows.fetchall()
    if len(rows)==1:
        return render_template("loggedin.html")
    else:
        return redirect("/register")

@myapp.route("/register", methods = ["GET","POST"])
def registerpage():
    if request.method=="POST":
        dUN=request.form['username']
        dPW=request.form['password']
        Uemail=request.form['useremail']

        sqlconnnection=sqlite3.Connection(currentlocation+"\login.db")
        cursor=sqlconnnection.cursor()
        query1="INSERT INTO users VALUES( '{u}','{p}'.'{e}')".format(u=dUN,p=dPW,e=Uemail)
        cursor.execute(query1)
        sqlconnnection.commit()
        return redirect("/")
    return render_template("register.html)



if __name__="main.py":
    myapp.run()
        