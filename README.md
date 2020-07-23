### The Giess-o-mat Project

The Giess-o-mat Project (from the german verb giessen -> to pour) is the attempt to build and program a fully automated miniature greenhouse. Several sensors and actuators are involved to control irrigation, ventilation and lighting. The brain of the Giess-o-mat is a Raspberry Pi single-board computer combined with other micro-electronic components like relays, pumps, valves, fans and sensors. 

All aspects of the Giess-o-mat can be monitored and controlled via a web application that runs on the Raspberry Pi. This includes the readings of sensors and their timeseries, the manual control of the functions and the change of settings. 

While the initial idea was to automate a self-build miniature greenhouse, the components and functionality can also be utilised in different scenarios and with diffent complexity. 

#### Sensorvalues

- Airtemperature- and Humidity
- Soiltemperature
- Soilmoisture
- Illuminance (Brightness)
- Waterlevel of the watertank

#### Controllable Aspects

- Irrigation
- Lighting
- Ventilation

#### Project Repositories

The project consists of 4 repositories:

- ##### Giess-o-mat
  This is the current repository and contains all the 'logic' of the Giess-o-mat. It is mostly python code that reads the sensor values, stores them in a database and controls all actuators according to the sensor values and the given settings at a specific interval.

- ##### Giess-o-mat-Webapp
  A vue.js web application that displays all the stored data and allows to make settings and control the Giess-o-mat manually using the next two components.
  
- ##### Giess-o-mat-Webserver
  A simple node.js webserver that provides an API to serve as an interface between the Raspberry Pi and the web application. Used to query the sensor values and settings and send new settings to the Raspberry Pi. 

- ##### Giess-o-mat-Socketserver
  Since some of the actuators (mainly the irrigation) require a quick response time when turning them on and off a websocket communication is also established between the web application and the Rapsberry Pi. This is used for bi-directional and fast communication to send status updates or turn on/off certain components.
