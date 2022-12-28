import mysql.connector
import random

cnx = mysql.connector.connect(user='root', host = 'localhost',database='traveldbms',password='793164')
cursor = cnx.cursor()
add_user = ("INSERT INTO user VALUES (%s, %s)")

k = 123456
# Insert new user
for i in range(0,10):
  data_user = (k+i,str(random.randint(10000,11000)))
  cursor.execute(add_user, data_user)

cnx.commit()
cursor.close()
cnx.close()