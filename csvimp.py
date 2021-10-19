#add required songs to Source.csv file and execute this first before running FindTune


import csv
import mysql.connector as mys

mycon = mys.connect(host='localhost', user='root', passwd='root', charset='utf8')     #MySQL database connect
cur = mycon.cursor() 

with open('Source.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

query1 = "CREATE DATABASE music"
cur.execute(query1)
cur.execute("use music;")
cur.execute('DROP TABLE IF EXISTS Source_master;')
print('Creating table....')
cur.execute("create table if not exists Source_master(SNo int NOT NULL PRIMARY KEY, Title varchar(40), Artist varchar(40), Genre varchar(40))")
print("Source_master table is created....")
 
for i in range (1,len(data)):
    query = "insert ignore into Source_master values({},'{}','{}','{}');".format(data[i][0], data[i][1], data[i][2], data[i][3])
    cur.execute(query)
    mycon.commit()

finalq = "select * from Source_master;"    
cur.execute(finalq)
sqldata = cur.fetchall()
rc = cur.rowcount()

if len(data)-1 == rc:
    print("all records inserted")

mycon.close() 