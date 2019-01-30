from flask import Flask, render_template, request, redirect, url_for
import sys
import sqlite3 as sql
app = Flask(__name__)


@app.route("/")
def login():
    return render_template("login.html")


@app.route('/login', methods=['POST', 'GET'])
def loggedin():
   if request.method == 'POST':
      user = request.form['nm']
      return render_template("home.html")
      #return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))


@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name


@app.route("/template")
def template():
    return render_template("template.html")


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/enternew')
def enternew():
    return render_template('student.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            pin = request.form['pin']
            conn = sql.connect('test.db')
            print("Opened database successfully");

            print(nm + "-" + addr + " " + pin + " " +city)
            data =(nm,addr,city,pin)
            sql_statement ='INSERT INTO students (name,addr,city,pin) VALUES(?,?,?,?)'
            with sql.connect("test.db") as con:
                cur = con.cursor()
                print(cur)
                cur.execute(sql_statement,data)
                con.commit()
            msg = "Record successfully added"
        except Exception as e:
            print(e)
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg=msg)
            con.close()



@app.route('/list')
def list():
    con = sql.connect("test.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall();
    return render_template("list.html", rows=rows)

if __name__ == "__main__":
    app.run()