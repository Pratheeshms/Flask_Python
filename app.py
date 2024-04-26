from flask import Flask, render_template, redirect, request, url_for
import psycopg2

app = Flask(__name__)

app.config["POSTGRES_HOST"] = "localhost"
app.config["POSTGRES_USER"] = "postgres"
app.config["POSTGRES_PASSWORD"] = "postgres"
app.config["POSTGRES_DB"] = "postgres"


def get_db_connection():
    conn = psycopg2.connect(
        host=app.config["POSTGRES_HOST"],
        user=app.config["POSTGRES_USER"],
        password=app.config["POSTGRES_PASSWORD"],
        dbname=app.config["POSTGRES_DB"]
    )
    return conn


@app.route("/deleteUser/<string:id>", methods=["GET", "POST"])
def deleteUser(id):
    con = get_db_connection().cursor()
    sql = "delete from person where id=%s"
    con.execute(sql, [id])
    get_db_connection().commit()
    con.close()
    return redirect(url_for("home"))


@app.route("/editUser/<string:id>", methods=["GET", "POST"])
def editUser(id):
    con = get_db_connection().cursor()
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        gender = request.form["Gender"]
        city = request.form["city"]
        sql = "update person set name=%s, age=%s, gender=%s, city=%s where id=%s"
        con.execute(sql, [name, age, gender, city, id])
        get_db_connection().commit()
        con.close()
        return redirect(url_for("home"))
    sql = "select * from person where id=%s"
    con.execute(sql, [id])
    res = con.fetchone()
    con.close()
    return render_template("editUser.html", data=res)


@app.route("/addUser", methods=["GET", "POST"])
def addUser():
    if request.method == "GET":
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        city = request.form['city']
        con = get_db_connection().cursor()
        sql = "INSERT INTO person (name, age, gender, city) values(%s, %s, %s, %s);"
        sql ='select * from person;'
        con.execute(sql, (name, age, gender, city))
        get_db_connection().commit()
        con.close()
        return redirect(url_for("home"))
    return render_template("addUser.html")


@app.route("/")
def home():
    con = get_db_connection().cursor()
    sql = "select * from person"
    con.execute(sql)
    res = con.fetchall()
    con.close()
    return render_template("home.html", datas=res)


if __name__ == '__main__':
    app.run(debug=True)
