from flask import Flask, flash, redirect, render_template, request
from cs50 import SQL

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key_here"

db = SQL("sqlite:///birthdays.db")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        db.execute("INSERT INTO birthdays (name, month, day) VALUES (:name, :month, :day)",
                   name=name, month=month, day=day)

        return redirect("/")
    else:
        rows = db.execute("SELECT * FROM birthdays")
        return render_template("index.html", rows=rows)

@app.route("/edit/<int:id>", methods=["POST"])
def edit(id):
    if request.method == "POST":
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        db.execute("UPDATE birthdays SET name = :name, month = :month, day = :day WHERE id = :id",
                   name=name, month=month, day=day, id=id)

        return redirect("/")

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    db.execute("DELETE FROM birthdays WHERE id = :id", id=id)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
