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

sql_getProvinces 	= "SELECT id, name_en FROM provinces"
sql_getDistricts 	= "SELECT d.id, d.name_en FROM provinces p, districts d where p.id=d.province_id AND p.id={0}"
sql_getCities 		= "SELECT c.id, c.name_en, c.postcode, c.latitude, c.longitude FROM districts d, cities c where d.id=c.district_id AND d.id={0}"

print("Accessing database...")

mycursor.execute(sql_getProvinces)
provinces = mycursor.fetchall()

province_list = []

for prv in provinces:
	print("Printing the province {0} of ID {1}...".format(prv[1], prv[0]))
	mycursor.execute(sql_getDistricts.format(prv[0]))
	districts = mycursor.fetchall()
	disct_list = []
	for district in districts:
		mycursor.execute(sql_getCities.format(district[0]))
		cities = mycursor.fetchall()
		city_list = []
		for city in cities:
			city_list.append({'id': city[0],'city': city[1], 'details' : {'postalcode': city[2], 'latitude': str(city[3]), 'longitude': str(city[4])}})
		disct_list.append({'id': district[0], 'district': district[1], 'cities': city_list})
	province = {'id': prv[0], 'province' : prv[1], 'districts' : disct_list}
	province_list.append(province)
	province_json = json.dumps(province)
	jsonFile = open(str(prv[0])+"_"+str(prv[1])+".json", "w")
	jsonFile.write(province_json)
	jsonFile.close()
	print("Printed {0}".format(prv[1]))
print("Printing AllProvinces...")
provinces_json = json.dumps(province_list)
jsonFile = open("AllProvinces.json", "w")
jsonFile.write(provinces_json)
jsonFile.close()
print("Operation Successful")
print("Exiting...")





             