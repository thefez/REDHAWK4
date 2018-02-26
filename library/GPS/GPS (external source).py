import os
import re
import _mysql
import datetime

#assign sensor number
sensor = "sensor1"

#define command to be run my linux terminal
gpscmd = 'sudo stty -F /dev/ttyUSB0 ispeed 4800 && timeout 5 cat < /dev/ttyUSB0'

#create array storing converted gps data to push to database
latitude = []
longitude = []

#define Regex patterns
floatingNumbers = "[0-9]*\.[0-9]*" #only allows floating number format
hemisphere = "[A-Z]"	#only allows 1 letter - presumably N, S, E, or W

#convert raw latitude data to decimal format
def latConversion(latCoord, hemisphere):
	newLat = ''
	
	if (hemisphere == "N"):
		#changes GPS dongle format from ####.#### to ##.#######
		newLat = str(latCoord[0:2] + '.' + latCoord[2:4] + latCoord[5:9])
		return float(newLat)
	else:
		#changes to ##.####### format and assigns negative value for Southern
		#hemisphere
		newLat = str('-' + latCoord[0:2] + '.' + latCoord[2:4] + latCoord[5:9])
		return newLat
		
#convert raw longitude data to decimal format
def lonConversion(lonCoord, hemisphere):
	newLon = ''
	
	if (hemisphere == "E"):
		#changes GPS dongle format from ####.#### to ##.######
		newLon = str(lonCoord[1:3] + '.' + lonCoord[3:5] + lonCoord[6:10])
		return float(newLon)
	else:
		#changes to ##.###### format and assigns negative value for Western
		#hemisphere
		newLon = str('-' + lonCoord[1:3] + '.' + lonCoord[3:5] + lonCoord[6:10])
		return float(newLon)

#reads each line of GPS output, searches for GPGGA data and parses for above
#functions to convert data. After the data is appended to respective array.
def main():
	print "Starting program"
	print "Running 5 seconds of GPS data collection."
	gpsdata = os.popen(gpscmd) #running linux terminal command above
	
	for line in gpsdata.readlines():
		if ("$GPGGA" in line): #checking for GPGGA NMEA information
			a = line.split(",") #splits CSV into array
			if ( (len(a[2]) > 0 and len(a[4]) > 0) and 	#check to make sure GPS data values are not empty
				(re.match(floatingNumbers, a[2]) and	#check to make sure data value is numbers with decimal
				re.match(floatingNumbers, a[4]) and	#check to make sure data value is numbers with decimal
				re.match(hemisphere, a[3]) and		#check to make sure data value is E/W
				re.match(hemisphere, a[5]))):		#check to make sure data value is N/S
				
				latitude.append(latConversion(a[2],a[3])) #convert raw data to desired format
				longitude.append(lonConversion(a[4],a[5])) #convert raw data to desired format

			else:
				main() #rerun if not empty

	if (len(latitude) == 0 and len(longitude) == 0):
		main()	
	else:
		return
			
main()

print "GPS conversion function complete."
print "Latitude Value: " + str(latitude[-1])
print "Longitude Value: " + str(longitude[-1])

print "Writing to receiver database"
conn =_mysql.connect(host="192.168.1.54",user="webserve", passwd="redhawk",db="RHtest") #connect to db
x = conn.cursor()
try:
   x.execute("""INSERT INTO receivers(sensorNum, time, sensorlatitude, sensorlongitude) VALUES (%s, %s,%s,%s)""",(sensor, datetime.datetime,latitude[-1],longitude[-1]))
   conn.commit()
except:
   conn.rollback()

conn.close()
print "Written to database"
