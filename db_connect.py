import mariadb
import os
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    return mariadb.connect(
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST"),
        port=3306,
        database=os.getenv("DATABASE"),
    )


def get_students():
    try:
        conn = mariadb.connect(
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
            port=3306,
            database=os.getenv("DATABASE"),
        )
        cur = conn.cursor()
        cur.execute("SELECT id, student_name, date_of_birth, email FROM student")
        rows = cur.fetchall()
        return [
            {"id": row[0], "name": row[1], "dob": row[2], "email": row[3]}
            for row in rows
        ]
    except mariadb.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if "conn" in locals():
            conn.close()


def get_student_by_id(student_id):
    try:
        conn = mariadb.connect(
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST"),
            port=3306,
            database=os.getenv("DATABASE"),
        )
        cur = conn.cursor()
        cur.execute(
            "SELECT id, student_name, date_of_birth, email FROM student WHERE id = ?",
            (student_id,),
        )
        row = cur.fetchone()
        if row:
            return {"id": row[0], "name": row[1], "dob": row[2], "email": row[3]}
        else:
            return None
    except mariadb.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        if "conn" in locals():
            conn.close()
