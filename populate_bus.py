import mysql.connector
import random

cnx = mysql.connector.connect(user='root', host = 'localhost',database='traveldbms',password='793164')
cursor = cnx.cursor()
add_hotel = ("INSERT INTO bus(bus_number,bus_name,src,dest,priceperperson) VALUES (%s, %s ,  %s, %s, %s)")

busnames=["Indra","Garuda","Iravat","SRS","Orange","SRS","Indra","Garuda","Iravat","Orange"]
src = ["Chennai","Bengaluru","Delhi","Chennai","Bengaluru","Delhi","Chennai","Bengaluru","Delhi","Bengaluru"]
dest = ["Delhi","Chennai","Bengaluru","Bengaluru","Delhi","Chennai","Bengaluru","Chennai","Bengaluru","Chennai"]


for i in range(0,10):
  data_hotel = ("b"+str(i),busnames[i]+" "+src[i][0:3]+"-"+dest[i][0:3],src[i],dest[i],10*((i+1)*2))
  cursor.execute(add_hotel, data_hotel)


cnx.commit()
cursor.close()
cnx.close()