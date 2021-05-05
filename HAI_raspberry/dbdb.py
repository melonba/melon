import sqlite3
import csv
import os
import pandas as pd


def dbcon():
    return sqlite3.connect('mydb.db')


def create_table():
    try:
        db = dbcon()
        c = db.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users(Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
               Username TEXT NOT NULL, Weight TEXT NOT NULL, Height TEXT NOT NULL 
              );''')
        db.commit()
    except Exception as e:
        print('db error (create_table) : ', e)
    finally:
        db.close()


def export_csv():
    try:
        db = dbcon()
        c = db.cursor()
        c.execute('SELECT * from users')
        rows = c.fetchall()

        print("Exporting data into CSV.....")
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "userInfo.csv")
        with open(path, 'w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow([i[0] for i in c.description])
            print(rows)
            csv_writer.writerow([rows[-1][0], rows[-1][1], rows[-1][2], rows[-1][3]])
#           DB 내용 전체 CSV 변환 코드
#            for i, row in enumerate(rows):
#                print(rows)
#                csv_writer.writerow([row[0], row[1], row[2], row[3]])

        dirpath = os.getcwd() + "/userInfo.csv"
        print("data exported Successfully into {}".format(dirpath))
    except Exception as e:
        print('db error (export_csv) : ', e)
    finally:
        db.close()


def insert_data(username, weight, height):
    try:
        db = dbcon()
        c = db.cursor()
        setdata = (username, weight, height)
        c.execute('''INSERT INTO users(Username, Weight, Height) VALUES(?, ?, ?);''', setdata)
        db.commit()
    except Exception as e:
        print('db error (insert_data) : ', e)
    finally:
        db.close()


def select_all():
    ret = list()
    try:
        db = dbcon()
        c = db.cursor()
        c.execute('SELECT * FROM users')
        ret = c.fetchall()
    except Exception as e:
        print('db error (select_all) : ', e)
    finally:
        db.close()
        return ret


