import smtplib
import time
import pyowm
import requests
import datetime
import csv
from pip._vendor.distlib.compat import raw_input


def current_situation(temp, w, ws, r_status):
    # p is air density
    if 5.00 <= temp <= 9.00:
        P = 1.268
    elif 10.00 <= temp <= 14.00:
        P = 1.246
    elif 15.00 <= temp <= 19.00:
        P = 1.225
    elif 20.00 <= temp <= 24.00:
        P = 1.204
    elif 25.00 <= temp <= 29.00:
        P = 1.184
    elif 30.00 <= temp <= 39.00:
        P = 1.164
    elif 40.00 <= temp <= 49.00:
        P = 1.127
    elif temp >= 50.00:
        P = 1.093
    else:
        P = 1.2  # default air density
    time.sleep(1)
    print('density: {} kg/m^3'.format(P))
    if ws < 12:
        time.sleep(1)
        print('Wind speed is not suitable for Energy Production........')
        if r_status:
            time.sleep(1)
            print('Stopping Wind Turbines.............')
            time.sleep(1)

    elif 12 <= ws <= 50:
        time.sleep(1)
        print('Energy production possible...... ')
        time.sleep(1)
        print('Starting Wind Turbines........')
        r = 58  # average blade length 58 meters
        n = 40  # efficiency in percentage

        power = (1.57 * (r ** 2) * (w ** 3) * P * n) / 100
        time.sleep(1)
        print('Current output: {} W / {} KW / {} MW'.format(power, power / 1000, power / 1000000))
        time.sleep(2)

    else:
        time.sleep(1)
        print('Wind speed exceeding limit......... ')
        time.sleep(1)
        print('Turning off Wind Turbine.........')
        time.sleep(1)
        r_status = False


def prediction(t_s_list, c_t, w_mps_list, w_kps_list, p_d_power_list, len1):
    print('\n----------------------------This is prediction section----------------------------\n')
    time.sleep(1)
    length1 = len1
    radius1 = 53
    efficiency1 = 40
    count = 0
    for m in range(length1):
        if w_kps_list[m] < 20:
            count = count + 1
        elif 20 <= w_kps_list[m] < 50:

            if 5.00 <= c_t[m] <= 9.00:
                den = 1.268
            elif 10.00 <= c_t[m] <= 14.00:
                den = 1.246
            elif 15.00 <= c_t[m] <= 19.00:
                den = 1.225
            elif 20.00 <= c_t[m] <= 24.00:
                den = 1.204
            elif 25.00 <= c_t[m] <= 29.00:
                den = 1.184
            elif 30.00 <= c_t[m] <= 39.00:
                den = 1.164
            elif 40.00 <= c_t[m] <= 49.00:
                den = 1.127
            elif c_t[m] >= 50.00:
                den = 1.093
            else:
                den = 1.2  # default air density
            p_d_power1 = (1.57 * (radius1 ** 2) * (w_mps_list[m] ** 3) * den * efficiency1) / 100
            time.sleep(1)
            print('Wind speed will be optimum at {} i.e. {} km/h'.format(t_s_list[m], w_kps_list[m]))
            time.sleep(1)
            print('High Time for optimum Production..............')
            time.sleep(1)
            print(
                'Predicted output: {} W / {} KW / {} MW\n'.format(p_d_power1, p_d_power1 / 1000, p_d_power1 / 1000000))
            p_d_power_list.append(p_d_power1)
        elif w_kps_list[m] >= 50:
            time.sleep(1)
            print('Over production Alert............. ! ! !')
            time.sleep(1)
            print('Stop Production and Wind Turbines.............. \n! ! !')

            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("karsumon131@gmail.com", "mgmpisxgmeexshzs")
            message1 = "Alert!!\nThis is an auto-generated E-mail.\nOver Production. Current Wind speed is " + \
                       w_kps_list[m] + 'km/h'
            s.sendmail("karsumon131@gmail.com", "karsumon131@gmail.com", message1)
            time.sleep(1)
            print("E-Mail Alert Sent !! ")
            s.quit()
    if count == length1:
        print('Wind speed not suitable for maximum power production for the selected time period.')
        time.sleep(1)
        print('Wind speed will be less than 20 km/h!!!')
        time.sleep(1)
        print('Low Power Production Possible !!!')
    time.sleep(1)


# driver code...........................................................................................................

city_entry = raw_input('Enter City: ')
country_entry = raw_input('Enter country: ')

# contents

running_status = True

while running_status:
    wind_mps_list = []
    wind_kps_list = []
    c_temp = []
    f_temp = []
    time_stamp_list = []
    description_list = []
    prediction_power_list = []
    header = ['Date', 'Location', 'Temperature', 'Wind Speed', 'Description']
    total_data_hourly = []
    total_data_3hourly = []
    api_key = '3ee50f44c4e30cacbd795358f1c6531d'

    owm = pyowm.OWM(api_key)
    loc = city_entry + ', ' + country_entry
    observation = owm.weather_at_place(loc)

    current_data_header = ['Time', 'Location', 'Temperature', 'Wind Speed', 'Description', 'Pressure']
    current_data = []

    time.sleep(1)
    print('---------------------------------------------MENU---------------------------------------------')
    print('1. Weather Forecasting \n2. Current Weather \n3. Exit')
    print('----------------------------------------------------------------------------------------------')
    time.sleep(1)
    print('Enter 1 to Show Forecast Weather Data or Enter 2 to Show Current Weather Data or Enter 3 to Exit......')
    time.sleep(1)
    main_choice = input('Enter your choice: ')
    if main_choice == '1':
        print('\n------------------------------Forecast Weather Section------------------------------\n')
        time.sleep(1)
        print('For two days Hourly forecast Type H, For five days Three Hourly Forecast Type 3H')
        time.sleep(1)
        forecast_choice = input('Enter your choice:-  ')

        if forecast_choice == 'H' or forecast_choice == 'h' or forecast_choice == '1':
            # hourly forecast section...................................................................................

            print('Hourly Forecast..... !!!')
            time.sleep(2)
            api_call_loc = 'https://api.openweathermap.org/data/2.5/weather?q='
            location = city_entry + ',' + country_entry
            url_call_loc = api_call_loc + location + '&appid=' + api_key
            json_data_loc = requests.get(url_call_loc).json()
            lat = str(json_data_loc['coord']['lat'])
            long = str(json_data_loc['coord']['lon'])

            api_call = 'https://api.openweathermap.org/data/2.5/onecall?lat='
            url_call = api_call + lat + '&lon=' + long + '&exclude=current,minutely,daily&appid=' + api_key
            json_data = requests.get(url_call).json()

            time.sleep(1)
            print('Gathering Forecast..............')
            time.sleep(1)

            for item in json_data['hourly']:

                data = []
                unix_time = item['dt']
                time_convert = datetime.datetime.fromtimestamp(unix_time)
                time_stamp = str(time_convert)
                next_date, hour = time_stamp.split(' ')
                date_str = ''
                current_date = ''
                if current_date != next_date:
                    current_date = next_date
                    year, month, day = current_date.split('-')
                    date = {'y': year, 'm': month, 'd': day}
                date_str = str(day + '-' + month + '-' + year)
                hour = int(hour[:2])

                # Sets the AM or PM period
                if hour < 12:
                    if hour == 0:
                        hour = 12
                    meridian = 'AM'
                else:

                    if hour > 12:
                        hour -= 12
                    meridian = 'PM'

                time_stamp = str(hour) + ' ' + meridian + ' on ' + date_str
                time_stamp_list.append(time_stamp)
                data.append(time_stamp)
                data.append(location)

                # Temperature is measured in Kelvin
                temperature = item['temp']
                celsius = temperature - 273.15
                c_temp.append(celsius)
                data.append(celsius)
                fahrenheit = temperature * 9 / 5 - 459.67
                f_temp.append(fahrenheit)

                # Wind Speed
                wind = item['wind_speed']
                wind_kps = wind * 3.6
                wind_mps_list.append(wind)  # adding wind speeds in m/s to list
                wind_kps_list.append(wind_kps)  # adding wind speeds in m/s to list
                data.append(wind)

                # Weather condition
                description = item['weather'][0]['description'],
                description_list.append(description)
                data.append(description)
                total_data_hourly.append(data)

            with open('weather_data_hourly.csv', 'w') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(header)
                csv_writer.writerows(total_data_hourly)

            length = len(time_stamp_list)
            '''for i in range(length):
                print('{}, {} km/h'.format(time_stamp_list[i], wind_kps_list[i]))'''
            prediction(time_stamp_list, c_temp, wind_mps_list, wind_kps_list, prediction_power_list, length)


        elif forecast_choice == '3H' or forecast_choice == '3h' or forecast_choice == '2':

            # three hourly forecast section.............................................................................

            print('Three Hourly Forecast..... !!!')
            api_call = 'https://api.openweathermap.org/data/2.5/forecast?appid=' + api_key  # for three hourly forecast
            url_call = api_call + '&q=' + city_entry  # for three hourly for five days
            json_data = requests.get(url_call).json()
            loc = city_entry + ',' + country_entry
            location = {
                'city_name': json_data['city']['name'],
                'country_name': json_data['city']['country']
            }

            print('{city_name}, {country_name}'.format(**location))
            current_date = ''
            time.sleep(1)
            print('Gathering Forecast................')
            time.sleep(1)

            for item in json_data['list']:

                data = []
                time_str = item['dt_txt']
                next_date, hour = time_str.split(' ')
                date_str = ''
                if current_date != next_date:
                    current_date = next_date
                    year, month, day = current_date.split('-')
                    date = {'y': year, 'm': month, 'd': day}
                    date_str = str(day + '-' + month + '-' + year)
                    # time.sleep(1)
                    # print('\n{m}/{d}/{y}'.format(**date))

                hour = int(hour[:2])

                # Sets the AM or PM period
                if hour < 12:
                    if hour == 0:
                        hour = 12
                    meridian = 'AM'
                else:

                    if hour > 12:
                        hour -= 12
                    meridian = 'PM'

                # loading time stamps  in list
                time_stamp = str(hour) + ' ' + meridian + ' ' + date_str
                time_stamp_list.append(time_stamp)
                data.append(time_stamp)

                # Temperature is measured in Kelvin
                temperature = item['main']['temp']
                celsius = temperature - 273.15
                data.append(celsius)
                c_temp.append(celsius)
                fahrenheit = temperature * 9 / 5 - 459.67
                f_temp.append(fahrenheit)

                # Wind Speed
                wind = item['wind']['speed']
                wind_kps = wind * 3.6
                wind_mps_list.append(wind)  # adding wind speeds in m/s to list
                wind_kps_list.append(wind_kps)  # adding wind speeds in m/s to list
                data.append(wind)

                # Weather condition
                description = item['weather'][0]['description'],
                description_list.append(description)
                data.append(description)
                total_data_3hourly.append(data)
            with open('weather_data_3hourly.csv', 'w') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(header)
                csv_writer.writerows(total_data_3hourly)

            length = len(time_stamp_list)
            prediction(time_stamp_list, c_temp, wind_mps_list, wind_kps_list, prediction_power_list, length)

        else:
            print('Invalid Choice..... !!!')

    elif main_choice == '2':
        # current weather section.......................................................................................
        curr_running_status = True
        while curr_running_status:
            data = []
            curr_time = datetime.datetime.now()
            current_time = curr_time.strftime("%H:%M:%S")
            curr_date = str(curr_time.day) + '/' + str(curr_time.month) + '/' + str(curr_time.year)
            curr_time_stamp = str(current_time) + ' on ' + curr_date
            data.append(curr_time_stamp)
            data.append(loc)
            weather = observation.get_weather()  # weather in a gist
            temperature = weather.get_temperature('celsius')['temp']  # temperature
            data.append(temperature)
            wind = weather.get_wind()['speed']  # speed in mps
            data.append(wind)
            windSpeed = wind * 3.6  # speed in kps
            status = weather.get_detailed_status()  # weather status
            data.append(status)
            pressure = weather.get_pressure()['press']  # atmospheric pressure
            data.append(pressure)
            current_data.append(data)
            print('\n------------------------------Current Weather Section------------------------------\n')
            time.sleep(1)
            print('{}, {}'.format(city_entry, country_entry))
            time.sleep(2)
            print('Date:  {}'.format(curr_date))
            time.sleep(2)
            print('Time:  {}'.format(current_time))
            time.sleep(1)
            print('Current Temperature: {} degree C'.format(temperature))
            time.sleep(1)
            print('Current Wind Speed in mps: {} m/s'.format(wind))
            time.sleep(1)
            print('Current Wind Speed in kph: {} km/h'.format(windSpeed))
            time.sleep(1)
            print('Current Atmospheric Pressure: {} mbar'.format(pressure))
            time.sleep(1)
            print('Current Status: {}'.format(status))
            time.sleep(1)
            with open('current_weather_data.csv', 'w') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(current_data_header)
                csv_writer.writerows(current_data)

            current_situation(temperature, wind, windSpeed, curr_running_status)
            time.sleep(1)
            choice = input('press y or Y to show current weather data again else press n or N: ')

            if choice == 'y' or choice == 'Y':
                curr_running_status = True
            elif choice == 'n' or choice == 'N':
                time.sleep(1)
                print('Exiting current weather section...................\n')
                time.sleep(1)
                curr_running_status = False
            else:
                print('Invalid Choice.... !!!')
            time.sleep(3)
    elif main_choice == '3':
        time.sleep(1)
        print('Exiting Program...................')
        time.sleep(2)
        running_status = False

        
