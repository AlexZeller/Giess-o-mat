### The Giess-o-mat Project

<p align="center">
  <img src="./documentation/logo.png" alt="Size Limit CLI" width="70">
</p>

The Giess-o-mat Project (from the german verb giessen -> to water sth.) is the attempt to build and program a fully automated miniature greenhouse. Several sensors and actuators are involved to control irrigation, ventilation and lighting. The brain of the Giess-o-mat is a Raspberry Pi single-board computer combined with other micro-electronic components like relays, pumps, valves, fans and sensors. 

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

![giessomat_1](https://user-images.githubusercontent.com/34438645/200181644-4b47ddf3-a535-4924-b465-6de47d1fd0d6.JPG)
![DSC01087](https://user-images.githubusercontent.com/34438645/200181692-ce7cbb85-ae22-4ca2-97c5-2d540846577c.JPG)
![DSC01089](https://user-images.githubusercontent.com/34438645/200181700-39313afb-eb0d-4b52-a0b7-e3c7fc9943fb.JPG)
![DSC01090](https://user-images.githubusercontent.com/34438645/200181706-88bbafdd-fbc3-46e0-89de-14c7978706f5.JPG)
![DSC01091](https://user-images.githubusercontent.com/34438645/200181707-52b180f4-067e-4fbc-b676-7ab467e197d7.JPG)
![DSC01101](https://user-images.githubusercontent.com/34438645/200181717-c67bafed-8976-432a-a05e-d56ece5e5804.JPG)
![DSC01104](https://user-images.githubusercontent.com/34438645/200181730-c4046d4a-ca0e-40e1-a71b-23e79374e93b.JPG)
![DSC01106](https://user-images.githubusercontent.com/34438645/200181733-77b98a5e-b7fe-4307-a998-cf301ec57180.JPG)
![IMG_3303](https://user-images.githubusercontent.com/34438645/200181740-17384ce4-0b06-466c-9b57-22ba81490c15.PNG)
![IMG_3304](https://user-images.githubusercontent.com/34438645/200181742-c3eb1b03-8eeb-4358-944a-191545778e94.PNG)
![IMG_3305](https://user-images.githubusercontent.com/34438645/200181743-c0828b13-43f2-4ab2-851b-5d9ccc4f999c.PNG)
![IMG_3307](https://user-images.githubusercontent.com/34438645/200181746-01d8474f-8565-4325-8473-638d6a84ddcd.PNG)
![IMG_3509](https://user-images.githubusercontent.com/34438645/200181748-a78fd565-6c46-4fe3-8377-1cab320ac693.JPG)


#### Project Repositories

The project consists of 4 repositories:

- ##### [Giess-o-mat](https://github.com/AlexZeller/Giess-o-mat)
  This is the current repository and contains all the 'logic' of the Giess-o-mat. It is mostly python code that reads the sensor values, stores them in a database and controls all actuators according to the sensor values and the given settings at a specific interval.

- ##### [Giess-o-mat-Webapp](https://github.com/AlexZeller/Giess-o-mat_Webapp)
  A vue.js web application that displays all the stored data and allows to make settings and control the Giess-o-mat manually using the next two components.
  
- ##### [Giess-o-mat-Webserver](https://github.com/AlexZeller/Giess-o-mat-Webserver)
  A simple node.js webserver that provides an API to serve as an interface between the Raspberry Pi and the web application. Used to query the sensor values and settings and send new settings to the Raspberry Pi. 

- ##### [Giess-o-mat-Socketserver](https://github.com/AlexZeller/Giess-o-mat-Socketserver)
  Since some of the actuators (mainly the irrigation) require a quick response time when turning them on and off a websocket communication is also established between the web application and the Rapsberry Pi. This is used for bi-directional and fast communication to send status updates or turn on/off certain components.
