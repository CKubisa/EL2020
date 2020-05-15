#Import libraries as needed
from flask import Flask, render_template, jsonify, Response
import time
import sqlite3 as sql
import json
import RPi.GPIO as GPIO
import Adafruit_DHT

#Globals
app = Flask(__name__)

#Connects with website to register button press and turn off alarm
@app.route("/button")
def button():
	alarmPin=27
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(alarmPin,GPIO.OUT)
	print ("Alarm Deactivated")
	GPIO.output(alarmPin,False)
	time.sleep()

@app.route("/")
def index():
	return render_template('final.html')

#Connects database to website
@app.route("/sqlData")
def chartData():
	con = sql.connect('../log/finalData.db')
	cur = con.cursor()
	con.row_factory = sql.Row
	cur.execute("SELECT * FROM finalData")
	dataset = cur.fetchall()

	print (dataset)
	chartData = []

	for row in dataset:
		chartData.append({"Sensor":row[0],"myTime": row[1]})
	return Response(json.dumps(chartData), mimetype='application/json')

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=2020, debug=True)
