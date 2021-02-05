import tkinter as t
import smtplib
import time
from pyowm.owm import OWM
import requests
import datetime
import csv


def current_situation_d(temp, w, ws):
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
    log_details.config(state='normal')
    log_details.insert(t.INSERT, 'density: ' + str(P) + ' kg/m^3\n')
    log_details.config(state='disabled')
    if ws < 12:
        time.sleep(1)
        log_details.config(state='normal')
        log_details.insert(t.INSERT, 'Wind speed is not suitable for Energy Production.....\n')
        time.sleep(1)
        log_details.insert(t.INSERT, 'Stopping Wind Turbines.....\n')
        log_details.config(state='disabled')
        time.sleep(1)

    elif 12 <= ws <= 50:
        time.sleep(1)
        log_details.config(state='normal')
        log_details.insert(t.INSERT, 'Energy production possible..... \n')
        time.sleep(1)
        log_details.insert(t.INSERT, 'Starting Wind Turbines.....\n')
        r = 58  # average blade length 58 meters
        n = 40  # efficiency in percentage

        power = (1.57 * (r ** 2) * (w ** 3) * P * n) / 100
        time.sleep(1)
        log_details.insert(t.INSERT, 'Current output: ' + str(power) + 'W ' + str(power / 1000) + 'KW ' + str(
            power / 1000000) + 'MW' + '\n')
        log_details.config(state='disabled')
        time.sleep(2)

    else:
        time.sleep(1)
        log_details.config(state='normal')
        log_details.insert(t.INSERT, 'Wind speed exceeding limit.....\n')
        time.sleep(1)
        log_details.insert(t.INSERT, 'Turning off Wind Turbine.....\n')
        log_details.config(state='disabled')
        time.sleep(1)


def prediction(t_s_list, c_t, w_mps_list, w_kps_list, p_d_power_list, len1):
    log_details.config(state='normal')
    log_details.insert(t.INSERT, '\n-------------This is prediction section-------------\n')
    log_details.config(state='disabled')
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
            log_details.config(state='normal')
            log_details.insert(t.INSERT, 'Wind speed will be optimum at ' + str(t_s_list[m]) + ' i.e. ' + str(
                w_kps_list[m]) + '\n')
            time.sleep(1)
            log_details.insert(t.INSERT, 'High Time for optimum Production.....\n')
            time.sleep(1)
            log_details.insert(t.INSERT,
                               'Predicted output: ' + str(p_d_power1) + 'W ' + str(p_d_power1 / 1000) + 'KW ' +
                               str(p_d_power1 / 1000000) + 'MW' + '\n')
            log_details.config(state='disabled')
            p_d_power_list.append(p_d_power1)

        elif w_kps_list[m] >= 50:
            time.sleep(1)
            log_details.config(state='normal')
            log_details.insert(t.INSERT, 'Over production Alert..... ! ! !\n')
            time.sleep(1)
            log_details.insert(t.INSERT, 'Stop Production and Wind Turbines..... !!!\n')

            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("karsumon131@gmail.com", "mgmpisxgmeexshzs")
            message1 = "Alert!!\nThis is an auto-generated E-mail.\nOver Production. Current Wind speed is " + \
                       str(w_kps_list[m]) + 'km/h'
            s.sendmail("karsumon131@gmail.com", "karsumon131@gmail.com", message1)
            time.sleep(1)
            log_details.insert(t.INSERT, 'E-Mail Alert Sent !! \n')
            log_details.config(state='disabled')
            s.quit()
    if count == length1:
        log_details.config(state='normal')
        log_details.insert(t.INSERT, 'Wind speed not suitable for maximum power production\nfor the '
                                     'selected time period.\n')
        time.sleep(1)
        log_details.insert(t.INSERT, 'Wind speed will be less than 20 km/h!!!\n')
        time.sleep(1)
        log_details.insert(t.INSERT, 'Low Power Production Possible !!!\n')
        log_details.config(state='disabled')
    time.sleep(1)


def current_weather():
    api_key = '3ee50f44c4e30cacbd795358f1c6531d'

    cityText = cityE.get()
    countryText = countryE.get()

    if cityText == '' and countryText == '':
        log_details.config(state='normal')
        log_details.insert(t.INSERT, 'Enter Your Location First !!!\n')
        log_details.config(state='disabled')
        time.sleep(4)

    else:
        city_entry = cityText
        country_entry = countryText
        owm = OWM(api_key)
        mgr = owm.weather_manager()
        loc = city_entry + ', ' + country_entry
        observation = mgr.weather_at_place(loc)

        current_data_header = ['Time', 'Location', 'Temperature', 'Wind Speed', 'Description', 'Pressure']
        current_data = []
        # current weather section...................................................................................
        data = []
        curr_time = datetime.datetime.now()
        current_time = curr_time.strftime("%H:%M:%S")
        curr_date = str(curr_time.day) + '/' + str(curr_time.month) + '/' + str(curr_time.year)
        curr_time_stamp = str(current_time) + ' on ' + curr_date
        data.append(curr_time_stamp)
        data.append(loc)
        temperature = observation.weather.temperature('celsius')['temp']  # temperature
        data.append(temperature)
        wind = observation.weather.wind()['speed']  # speed in mps
        data.append(wind)
        windSpeed = wind * 3.6  # speed in kps
        weather = observation.weather
        status = weather.detailed_status  # status
        data.append(status)
        pressure = observation.weather.pressure['press']  # atmospheric pressure
        data.append(pressure)
        current_data.append(data)
        log_details.config(state='normal')
        log_details.insert(t.INSERT, '\n\n-------------Current Weather Section-------------\n')
        time.sleep(1)
        log_details.insert(t.INSERT, str(city_entry) + ', ' + str(country_entry) + '\n')
        time.sleep(2)
        log_details.insert(t.INSERT, 'Date:  ' + str(curr_date) + '\n')
        time.sleep(2)
        log_details.insert(t.INSERT, 'Time:  ' + str(current_time) + '\n')
        time.sleep(1)
        log_details.insert(t.INSERT, 'Current Temperature: ' + str(temperature) + ' degree C\n')
        time.sleep(1)
        log_details.insert(t.INSERT, 'Current Wind Speed in mps: ' + str(wind) + ' m/s\n')
        time.sleep(1)
        log_details.insert(t.INSERT, 'Current Wind Speed in kph:  ' + str(windSpeed) + ' km/h\n')
        time.sleep(1)
        log_details.insert(t.INSERT, 'Current Atmospheric Pressure:  ' + str(pressure) + '\n')
        time.sleep(1)
        log_details.insert(t.INSERT, 'Current Status: ' + str(status) + '\n')
        log_details.config(state='disabled')
        time.sleep(1)
        with open('current_weather_data.csv', 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(current_data_header)
            csv_writer.writerows(current_data)

        current_situation_d(temperature, wind, windSpeed)
        time.sleep(1)
    choice_enter.delete(0, 'end')


def hourly_forecasting():
    # hourly forecast section...............................................................................

    cityText = cityE.get()
    countryText = countryE.get()

    if cityText == '' and countryText == '':
        log_details.config(state='normal')
        log_details.insert(t.INSERT, 'Enter Your Location First !!!\n')
        log_details.config(state='disabled')
        time.sleep(4)

    else:
        api_key = '3ee50f44c4e30cacbd795358f1c6531d'
        city_entry = cityText
        country_entry = countryText
        wind_mps_list = []
        wind_kps_list = []
        c_temp = []
        f_temp = []
        time_stamp_list = []
        description_list = []
        prediction_power_list = []
        header = ['Date', 'Location', 'Temperature', 'Wind Speed', 'Description']
        total_data_hourly = []
        log_details.config(state='normal')
        log_details.insert(t.INSERT, '\n\nHourly Forecast.....!!!\n')
        log_details.config(state='disabled')

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
        log_details.config(state='normal')
        log_details.insert(t.INSERT, 'Gathering Forecast.....\n')
        log_details.insert(t.INSERT, str(location) + '\n')
        log_details.config(state='disabled')
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
            wind_kps_list.append(wind_kps)  # adding wind speeds in km/s to list
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
        prediction(time_stamp_list, c_temp, wind_mps_list, wind_kps_list, prediction_power_list, length)
    forecast_choice_enter.delete(0, 'end')


def three_hourly_forecasting():
    # three hourly forecast section.........................................................................

    cityText = cityE.get()
    countryText = countryE.get()
    if cityText == '' and countryText == '':
        log_details.config(state='normal')
        log_details.insert(t.INSERT, 'Enter Your Location First !!!\n')
        log_details.config(state='disabled')

    else:
        api_key = '3ee50f44c4e30cacbd795358f1c6531d'
        city_entry = cityText
        country_entry = countryText
        wind_mps_list = []
        wind_kps_list = []
        c_temp = []
        f_temp = []
        time_stamp_list = []
        description_list = []
        prediction_power_list = []
        header = ['Date', 'Location', 'Temperature', 'Wind Speed', 'Description']
        total_data_3hourly = []

        log_details.config(state='normal')
        log_details.insert(t.INSERT, '\n\nThree Hourly Forecast.....!!!\n')
        log_details.config(state='disabled')
        api_call = 'https://api.openweathermap.org/data/2.5/forecast?appid=' + api_key  # for three hourly
        url_call = api_call + '&q=' + city_entry  # for three hourly for five days
        json_data = requests.get(url_call).json()
        loc = city_entry + ',' + country_entry

        log_details.config(state='normal')
        log_details.insert(t.INSERT, 'Gathering Forecast.....\n')
        time.sleep(1)
        log_details.insert(t.INSERT, str(loc) + '\n')
        log_details.config(state='disabled')

        current_date = ''

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
    forecast_choice_enter.delete(0, 'end')


def decision():
    main_choice = choice_enter.get()
    forecast_choice = forecast_choice_enter.get()
    cityText = cityE.get()
    countryText = countryE.get()
    if cityText == '' and countryText == '':
        log_details.config(state='normal')
        log_details.insert(t.INSERT, 'Enter Your Location First !!!\n')
        log_details.config(state='disabled')
    else:
        if main_choice == '':
            log_details.config(state='normal')
            log_details.insert(t.INSERT, 'Choose any option !!!\n')
            log_details.config(state='disabled')
        elif main_choice == '1':
            if forecast_choice == 'H' or forecast_choice == 'h':
                hourly_forecasting()
            elif forecast_choice == '3H' or forecast_choice == '3h':
                three_hourly_forecasting()
            elif forecast_choice == '':
                log_details.config(state='normal')
                log_details.insert(t.INSERT, 'Choose any Forecast Type !!!\n')
                log_details.config(state='disabled')
            else:
                log_details.config(state='normal')
                log_details.insert(t.INSERT, 'Invalid Forecast Type !!!\n')
                log_details.config(state='disabled')
        elif main_choice == '2':
            current_weather()
        else:
            log_details.config(state='normal')
            log_details.insert(t.INSERT, 'Invalid Choice !!!\n')
            log_details.config(state='disabled')


def reset():
    choice_enter.delete(0, 'end')
    forecast_choice_enter.delete(0, 'end')
    cityE.delete(0, 'end')
    countryE.delete(0, 'end')


main = t.Tk()
main.title('WinPS-1')
main.geometry("1200x550+100+80")
main.configure(bg='#a2e146')

back_img = t.PhotoImage(file='weather.png')
main_back = t.Label(main, image=back_img)
main_back.place(x=0, y=0)

city = t.Label(main, text="ENTER LOCATION", fg='white', bg='#6a0490', width=50)
city.place(x=40, y=20)
city.config(font=('courier', 14))

city = t.Label(main, text="City: ", fg='black', bg='yellow')
city.place(x=100, y=60)
city.config(font=('courier', 12))
country = t.Label(main, text="Country: ", fg='black', bg='yellow')
country.place(x=100, y=100)
country.config(font=('courier', 12))

cityE = t.Entry(main)
cityE.place(x=210, y=57, height=30, width=252)
countryE = t.Entry(main)
countryE.place(x=210, y=97, height=30, width=252)

head = t.Label(main, text='TYPE YOUR CHOICE FROM THE OPTIONS BELOW: ->', fg='white', bg='#197e62', width=50)
head.place(x=40, y=140)
head.config(font=('courier', 14))

choice1 = t.Label(main, text='1. FORECAST (Enter 1)', bg='light green', width=30)
choice1.place(x=80, y=180)

choice2 = t.Label(main, text='2. CURRENT WEATHER (Enter 2)', bg='orange', width=30)
choice2.place(x=80, y=210)

choice_label = t.Label(main, text='Enter your choice here: ', fg='white', bg='#9330f1')
choice_label.place(x=50, y=240)
choice_label.config(font=('courier', 12))

choice_enter = t.Entry(main)
choice_enter.place(x=310, y=237, height=30, width=252)

forecast_choice_label = t.Label(main, text='ENTER YOUR FORECAST METHOD: ->', fg='black', bg='pink', width=50)
forecast_choice_label.place(x=50, y=290)
forecast_choice_label.config(font=('courier', 14))

forecast_choice1 = t.Label(main, text='1. TWO DAYS HOURLY (Enter H)', fg='black', bg='#50c51d', width=35)
forecast_choice1.place(x=80, y=330)

forecast_choice2 = t.Label(main, text='2. FIVE DAYS THREE HOURLY (Enter 3H)', fg='black', bg='#c8b10f', width=35)
forecast_choice2.place(x=80, y=360)

choice_label_forecast = t.Label(main, text='Enter your choice here: ', fg='white', bg='#9330f1')
choice_label_forecast.place(x=50, y=395)
choice_label_forecast.config(font=('courier', 12))

forecast_choice_enter = t.Entry(main)
forecast_choice_enter.place(x=310, y=392, height=30, width=252)

start = t.Button(main, text='Start', fg='white', bg='green', width=15, command=decision)
start.place(x=240, y=450)

stop = t.Button(main, text='Stop', fg='white', bg='red', width=15, command=exit)
stop.place(x=440, y=450)

reset = t.Button(main, text='Reset', fg='white', bg='#5f101c', width=15, command=reset)
reset.place(x=5, y=482)

log_details_label = t.Label(main, text='LOG DETAILS', fg='black', bg='#17deb4', width=30)
log_details_label.place(x=770, y=10)
log_details_label.config(font=('courier', 12))

log_details = t.Text(main)
log_details.place(x=700, y=40, height=500, width=450)
log_details.config(state='disabled')

main.mainloop()
