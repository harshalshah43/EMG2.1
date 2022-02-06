import pandas as pd
import sqlite3
import csv
import datetime

def clean_data(file_name):
    df1 = pd.read_csv(file_name)
    # df1['Date'] = df1['Date'].apply(lambda x:x.replace('/','-'))
    df1['Date'] = df1['Date'].apply(lambda x: pd.to_datetime(x))
    # print(df1['Date'])
    df1['Date'] = pd.to_datetime(df1['Date'],format = '%Y-%m-%d')
    print(df1['Date'])
    df1.to_csv("chunk.csv",index = False)
    print("cleaning complete")

# def clean_data2(filename):
#     format = "%Y-%m-%d"
#     with open(filename,"r") as f:
#         print(f.readline())
#         for line in f:
#             date = line.split(",")[0]
#             date = datetime.datetime.strptime(date,format)
#             print(date)
        

def flood(file_name):
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    a_file = open(file_name,"r")
    rows = csv.reader(a_file)
    header = next(rows)
    # query1 = cur.execute("Select * from enquiry_enquiry")
    # print(cur.fetchall())
    query2 = cur.executemany("INSERT INTO enquiry_enquiry (date_posted,party,item_code,qty,brand,cust_type,media) VALUES (?,?,?,?,?,?,?)",rows)
    print("insertion complete")
    con.commit()
    con.close()

def merge(filename1,filename2):
    df_old = pd.read_csv(filename1)
    df_new = pd.read_csv(filename2)
    df_old = pd.concat([df_old,df_new],axis = 0)
    df_old.to_csv("Enquiry_data.csv",index=False)
    print("merging complete")


if __name__ == '__main__':
    clean_data('chunk.csv')
    # flood("chunk.csv")
    # merge("Enquiry_data.csv","chunk.csv")
    # clean_data2("chunk.csv")