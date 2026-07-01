import sqlite3
from flask import Flask, render_template, send_from_directory,request,redirect
import os

app = Flask(__name__)

MUSIC_FOLDER = "uploads/music"

def create_table():
    conn=sqlite3.connect("usersongs.db")
    cursor=conn.cursor()
    
    cursor.execute('''create table if not exists users_table(
                   fname text,
                   lname text,
                   email text,
                   password text)
                   ''')
    conn.commit()
    conn.close()

create_table()

def get_songs():
    songs = []
    for file in os.listdir(MUSIC_FOLDER):
        if file.endswith(".mp3"):
            songs.append(file)
    return songs

@app.route('/')
def home():
    return redirect('/signup')

@app.route('/signup', methods=["GET","POST"])
def signup():
    if (request.method == "GET"):
        return render_template("signup.html")
    
    elif(request.method == "POST"):

        fname=request.form['fname']
        lname=request.form['lname']
        email=request.form['email']
        password=request.form['password']

        conn=sqlite3.connect('usersongs.db')
        cursor=conn.cursor()
        cursor.execute('''SELECT email FROM users_table where email = ?''',(email,))
        user = cursor.fetchone()

        if user:
            return redirect('/login_page')

        cursor.execute('''insert into users_table(fname,lname,email,password) values(?,?,?,?)''',(fname,lname,email,password))
        conn.commit()
        conn.close()

        global name
        name=fname
        return redirect('/index')

@app.route('/login_page',methods=["GET","POST"])
def login_page():
    if (request.method == "GET"):
        return render_template("login.html")
    elif(request.method == "POST"):
        
        email=request.form['email']
        password=request.form['password']

        conn=sqlite3.connect("usersongs.db")
        cursor=conn.cursor()


        cursor.execute('''select password,fname from users_table where email = ?''',(email,))
        # output is getting in the TUPLE format for output so using like output[0]
        output = cursor.fetchone()
        conn.commit()
        conn.close()

        if output == None:
            return redirect('/signup')

        global name
        name=output[1]

        # output is getting in the TUPLE format for output so using like output[0]
        if(password == output[0]):
            return redirect('/index')
        else:
            return render_template('login.html')

@app.route('/index')
def index():
    songs = get_songs()
    return render_template("index.html", songs=songs)

@app.route('/music/<filename>')
def music(filename):
    return send_from_directory(MUSIC_FOLDER, filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",10000)))