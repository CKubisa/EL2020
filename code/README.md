To use run both final.py and finalServer.py at the the same time

First Physical Setup
	1. Connect Power and Ground to the Rails
	2. Sound Sensor Module
		VCC Pin to Power Rail
		GND Pin to Ground Rail
		Out Pin to GPIO 26
	3. Vibration Sensor Module
		VCC Pin to Power Rail
                GND Pin to Ground Rail
                Out Pin to GPIO 5
	4. Infared Motion Sensor Module
		VCC Pin to Power Rail
                GND Pin to Ground Rail
                Out Pin to GPIO 23
	5. Buzzer Alarm Module
		VCC Pin to Power Rail
                GND Pin to Ground Rail
                Out Pin to GPIO 27
		2nd pin to GPIO 12 from GPIO 17
		*Optional add Red LED to GPIO 27
	6. Button (Small) (Digital Touch Senor is Broken)
		Have a resitor from power to left side of button
		Have a connection from right side of button to GPIO 15
		*Optional add Green LED between button and connection to GPIO 15


Software
	final.py
		Connects to the sensors with the GPIO
		Switches the alarm on
		Detects if it has been tripped
		Sends text if it is tripped

	finalServer.py
		Runs the web server
		Turns off Alarm through webserver
		Intercaes between server and the database

	final.html
		Shows how the Website should look and run
		Button to turn off the alarm
		Chart to show when the alarm went off with time and what sensor
		
	finalData.db
		Database that logs what sensor is used
