# SBSPS-Challenge-368-WinPS
The entire program is divided into two main parts:
1. Forecast Weather Section
2. Current Weather Section

Under Forecast Weather Section there are two choices:
a. Forecast for two days which gives hourly forecasts
b. Forecast for five days which gives three hourly forecasts

Forecasts include:
1. LOCATION
2. DATE AND TIME WHEN WIND ENERGY PRODUCTION IS OPTIMUM
3. WINDSPEED(in meters per second)
4. TEMPERATURE(in degree celcius) 
5. PREDICTED PRODUCTION OF OUTPUT(in Watts, Kilo Watts and Mega Watts)

Current Weather section is equipped with alarming system which sends email as alerts to the authority.

NOTE:
     i. Make sure the system is connected to the internet before running the program.
     ii. Make sure the system is installed with all the necessary libraries mentioned below.
         a. smtplib
         b. time
         c. pyowm
         d. requests
         e. datetime
         f. csv
from pip._vendor.distlib.compat import raw_input
     iii. Make sure the system is installed with python3 interpreter.
