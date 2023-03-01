import mysql.connector
import json

print("Operation started")
print("Connecting to database...")

db = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="",
	database="srilanka"
	)  

mycursor = db.cursor()

print("Database connected")

sql_getProvinces 	= "SELECT name_en FROM provinces"
sql_getDistricts 	= "SELECT d.name_en, p.name_en FROM provinces p, districts d where p.id=d.province_id"
sql_getCities 		= "SELECT c.name_en, c.postcode, c.latitude, c.longitude, d.name_en FROM districts d, cities c where d.id=c.district_id"

print("Accessing database...")

mycursor.execute(sql_getProvinces)
provinces = mycursor.fetchall()

mycursor.execute(sql_getDistricts)
districts = mycursor.fetchall()

mycursor.execute(sql_getCities)
cities_temp = mycursor.fetchall()

cities = []
for city in cities_temp:
	item = [city[0],city[1],float(str(city[2])),float(str(city[3])),city[4]]
	cities.append(item)

jsonFile = open("AllProvinces.json", "w")
jsonFile.write(json.dumps(provinces))
jsonFile.close()

jsonFile = open("AllDistricts.json", "w")
jsonFile.write(json.dumps(districts))
jsonFile.close()

jsonFile = open("AllCities.json", "w")
jsonFile.write(json.dumps(cities))
jsonFile.close()
             
print("Completed")