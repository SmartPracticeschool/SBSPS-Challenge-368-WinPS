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
         g. tKinter
     iii. Make sure the system is installed with python3 interpreter.
     
--------------------------------------------------------
DETAILED STEPS FOR THE OPERATIONS
--------------------------------------------------------

Step 1:
Click on any one of the buttons:
- Physical Address, for entering city name and country name.
- Co-ordinates, for entering latitude and longitude.

Step 2:
Choose any one of the authority emails from the drop down list.

Step 3:
Enter options:
- 1 for Forecasting.
- 2 for Current Weather.

Step 4:
If option in the previous step entered is 1 for Forecasting then,
In the Forecast choice:
- Enter 'H' or 'h' for Hourly forecasting.
- Enter '3H' or '3h' for Three Hourly forecasting.

If option in the previous step entered is 2, No need to type anything in the Forecast choice.

Step 5:
Click on the Start button to run.
Click on the Reset button to Reset the Entry fields.
Click on the Stop button to close the application.

Step 6:
How to Add Emails to the list?
- In the Right Bottom corner Enter the new authority Email-ID correctly.
- Click on the ADD button.
- The system will ask to Restart the application to reflect the newly added Email in the list.
