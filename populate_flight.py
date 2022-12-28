import mysql.connector
import random

cnx = mysql.connector.connect(user='root', host = 'localhost',database='traveldbms',password='793164')
cursor = cnx.cursor()
add_hotel = ("INSERT INTO flights(flight_number,flight_name,src,dest,fareperperson) VALUES (%s, %s ,  %s, %s, %s)")

flightnames=["Air Asia","Indigo","Jet Airways","Spice Jet"]
src = ["Chennai","Bengaluru","Delhi","Chennai","Bengaluru","Delhi","Chennai","Bengaluru","Delhi","Bengaluru"]
dest = ["Delhi","Delhi","Bengaluru","Bengaluru","Delhi","Chennai","Delhi","Delhi","Bengaluru","Chennai"]
prices = [8500 , 7500 , 8000 , 9000 , 7600 ,8500 , 7500 , 8000 , 9000 , 7600 ]

for i in range(0,10):
  data_hotel = ("f"+str(i),random.choice(flightnames)+" "+src[i][0:3]+"-"+dest[i][0:3],src[i],dest[i],prices[i])
  cursor.execute(add_hotel, data_hotel)

cnx.commit()
cursor.close()
cnx.close()