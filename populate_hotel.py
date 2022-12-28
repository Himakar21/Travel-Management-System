import mysql.connector
import random

cnx = mysql.connector.connect(user='root', host = 'localhost',database='traveldbms',password='793164')
cursor = cnx.cursor()
add_hotel = ("INSERT INTO hotels(hotel_id,hotel_name,city,priceperperson) VALUES (%s, %s ,%s, %s)")

hotelnames=["Umaid Bhawan","Oberoi Udaivillaa","The Leela Palace","The Taj Palace","ITC Maurya","The Lodhi",
            "JW Marriott","Sofitel Legend","Royal Orchid","ITC Gardenia"]
cities = ["Chennai","Bengaluru","Delhi","Chennai","Bengaluru","Delhi","Chennai","Bengaluru","Delhi","Bengaluru"]


for i in range(0,10):
  data_hotel = ("h"+str(i),hotelnames[i],cities[i],10*(i+1)**2)
  cursor.execute(add_hotel, data_hotel)


cnx.commit()
cursor.close()
cnx.close()