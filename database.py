import mysql.connector as mc

mydb = mc.connect(
    host="localhost",
    user="root",
    password="",
    database="examsystem"

)

mycursor = mydb.cursor()


def registered_canditates():
    mycursor.execute(
        "CREATE OR REPLACE TABLE registered_candidates (regno VARCHAR(255) PRIMARY KEY NOT NULL, name VARCHAR(255) NOT NULL,examcardno VARCHAR(40) NOT NULL,unitcode VARCHAR(20) NOT NULL,session VARCHAR(15) NOT NULL,course VARCHAR(40) NOT NULL)")

def create_table():
        mycursor.execute(
            "CREATE OR REPLACE TABLE users (username VARCHAR(255), password VARCHAR(255))")
            
def add_user():
        username = input("New username: ")
        password = input("New password: ")
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        value = (username, password)

        mycursor.execute(query, value)

        mydb.commit()
def exam_form():
    mycursor.execute(
        "CREATE OR REPLACE TABLE examination_form (regno VARCHAR(255) PRIMARY KEY NOT NULL, examcardno VARCHAR(10) NOT NULL,bookletno VARCHAR(15) NOT NULL,unitcode VARCHAR(7) NOT NULL,phonenumber VARCHAR(10) NOT NULL, examdate VARCHAR(10)NOT NULL,course VARCHAR(40) NOT NULL)")

registered_canditates()
create_table()
exam_form()
add_user()
