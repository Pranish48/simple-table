from flask import Flask, render_template, request, redirect
from db_connect import get_db_connection, get_students, get_student_by_id

app = Flask(__name__)


@app.route("/")
def index():
    students = get_students()
    return render_template("index.html", students=students)


@app.route("/student/<int:student_id>")
def student_detail(student_id):
    student = get_student_by_id(student_id)
    if student:
        return render_template("student_detail.html", student=student)
    else:
        return "Error"


@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/insert", methods=["POST"])
def insert_student():
    name = request.form["name"]
    dob = request.form["dob"]
    email = request.form["email"]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO student (student_name, date_of_birth, email) VALUES (?, ?, ?)",
        (name, dob, email),
    )
    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete_student(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM student WHERE id = ?", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")


@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        dob = request.form["dob"]
        email = request.form["email"]
        cur.execute(
            "UPDATE student SET name=%s, date_of_birth=%s, email=%s WHERE id=%s",
            (name, dob, email, student_id),
        )
        conn.commit()
        conn.close()
        return redirect("/")
               
    cur.execute("SELECT * FROM student WHERE id = %s", (student_id,))
    student = cur.fetchone()
    conn.close()
    return render_template("edit.html", student=student)


if __name__ == "__main__":
    app.run(debug=True)
