import mysql.connector
import random
cnx = mysql.connector.connect(user='root', host = 'localhost',database='traveldbms',password='793164')
cursor = cnx.cursor()
add_userprofile = ("INSERT INTO userprofile(username,age,doorNo,street,pincode,city,uid) VALUES (%s, %s,%s, %s,%s, %s,%s)")

usernames=["John","Himakar","Charan","Hemanth","Gnan","Karthik","Jasal","Rahul","Sid","Ram"]
doornos = ["1-38","2-39","3-40","1-32","2-19","3-10","1-84","2-91","3-20","2-98"]
streets = ["Pondy Bazaar","Brigade Road","Tilak Marg","Anna Nagar","MG Road","Connaught Lane",
          "T Nagar","Avenue Street","Lodhi Road","Church street"]
pincodes = ["600001","560001","110001","600009","560008","110002","600003","560004","110005","560006"]
cities = ["Chennai","Bengaluru","Delhi","Chennai","Bengaluru","Delhi","Chennai","Bengaluru","Delhi","Bengaluru"]
uids=[i for i in range(123456,123466)]

for i in range(0,10):
  data_user = (usernames[i],random.randint(24,60),doornos[i],streets[i],pincodes[i],cities[i],uids[i])
  cursor.execute(add_userprofile,data_user)

cnx.commit()
cursor.close()
cnx.close()