import csv
import datetime
import os
import smtplib
import tkinter as t
import webbrowser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from PIL import Image
from PIL import ImageTk
from pyowm.owm import OWM
from geopy.geocoders import Nominatim
from tkinter import messagebox


def current_situation_d(temp, w, ws, press):
    # p is air density
    P = press / (287.058 * temp)
    log_details.config(state='normal')
    log_details.insert(t.INSERT, 'density: ' + str(P) + ' kg/m^3\n')
    log_details.config(state='disabled')
    if ws < 20:
        log_details.config(state='normal')
        log_details.insert(t.INSERT, 'Wind speed is not suitable for Energy Production... \n' + str(ws) + 'km/h\n')
        log_details.insert(t.INSERT, 'Stopping Wind Turbines.....\n')
        log_details.config(state='disabled')
    elif 20 <= ws <= 80:
        log_details.config(state='normal')
        log_details.insert(t.INSERT, 'Energy production possible..... \n')
        log_details.insert(t.INSERT, 'Starting Wind Turbines.....\n')
        r = 58  # average blade length 58 meters
        n = 40  # efficiency in percentage
        power = (1.314 * (r ** 2) * (w ** 3) * P * n) / 100
        log_details.insert(t.INSERT, 'Current output: ' + str(power) + 'W ' + str(power / 1000) + 'KW ' + str(
            power / 1000000) + 'MW' + '\n')
        log_details.config(state='disabled')
    elif ws >= 81:
        t.messagebox.showerror('WinPS-1.1 ALERT !!', '\nWind speed exceeding limit !')
        log_details.config(state='normal')
        log_details.insert(t.INSERT, '\nWind speed exceeding limit.....\n')
        log_details.insert(t.INSERT, '\nTurning off Wind Turbine.....\n')
        log_details.config(state='disabled')
        receiver = variable.get()
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = 'WEATHER ALERT !!'
        body = "Alert!!\nThis is an auto-generated E-mail.\nOver Production. Current Wind speed is " + str(ws) + 'km/h'
        # body = "Alert!!\nThis is an auto-generated E-mail.\nOver Production. Current Wind speed is " + str(wind_test) + 'km/h' # for testing
        msg.attach(MIMEText(body, 'plain'))
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(sender, "mgmpisxgmeexshzs")
        message = msg.as_string()
        s.sendmail(sender, receiver, message)
        s.quit()
        log_details.config(state='normal')
        log_details.insert(t.INSERT, '\nE-Mail Alert Sent !! \n')
        log_details.config(state='disabled')


def prediction(t_s_list, c_t, w_mps_list, w_kps_list, p_d_power_list, len1, pressure):
    log_details.config(state='normal')
    log_details.insert(t.INSERT, '\n-------------This is prediction section-------------\n')
    log_details.config(state='disabled')
    radius1 = 53
    efficiency1 = 40
    count = 0
    # wind_test = 90
    # w_kps_list[m]
    for m in range(len1):
        if w_kps_list[m] < 20:
            count = count + 1
            log_details.config(state='normal')
            log_details.insert(t.INSERT, '\nWind speed not suitable at ' + str(t_s_list[m]) + ' i.e. \n' + str(
                w_kps_list[m]) + 'km/h\n')
            log_details.config(state='disabled')
        elif 20 <= w_kps_list[m] < 80:
            den = pressure / (287.058 * c_t[m])
            p_d_power1 = (1.314 * (radius1 ** 2) * (w_mps_list[m] ** 3) * den * efficiency1) / 100
            log_details.config(state='normal')
            log_details.insert(t.INSERT, '\nWind speed will be optimum at ' + str(t_s_list[m]) + ' i.e. \n' + str(
                w_kps_list[m]) + 'km/h\n')
            log_details.insert(t.INSERT, '\nHigh Time for optimum Production.....\n')
            log_details.insert(t.INSERT,
                               '\nPredicted output: \n' + str(p_d_power1) + 'W \n' + str(p_d_power1 / 1000) + 'KW \n' +
                               str(p_d_power1 / 1000000) + 'MW' + '\n')
            log_details.config(state='disabled')
            p_d_power_list.append(p_d_power1)
        elif w_kps_list[m] >= 81:
            t.messagebox.showerror('WinPS-1.1 ALERT !!', '\nWind speed exceeding limit !')
            log_details.config(state='normal')
            log_details.insert(t.INSERT, '\nOver production Alert..... ! ! !\n' + 'Speed= ' + str(w_kps_list[m]))
            log_details.insert(t.INSERT, '\nStop Production and Wind Turbines..... !!!\n')
            AgentEmail = variable.get()
            email_entry = AgentEmail
            receiver = email_entry
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = 'ALERT !!'
            body = "Alert!!\nThis is an auto-generated E-mail.\nOver Production. Current Wind speed is " + \
                   str(w_kps_list[m]) + 'km/h'
            # body = "Alert!!\nThis is an auto-generated E-mail.\nOver Production. Current Wind speed is " + str(wind_test) + 'km/h' # for testing
            msg.attach(MIMEText(body, 'plain'))
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("karsumon131@gmail.com", "mgmpisxgmeexshzs")
            message = msg.as_string()
            s.sendmail(sender, receiver, message)
            s.quit()
            log_details.config(state='normal')
            log_details.insert(t.INSERT, 'E-Mail Alert Sent !! \n')
            log_details.config(state='disabled')
    if count == len1:
        t.messagebox.showinfo('WinPS-1.1 INFO!!', 'Wind speed will be less than 20 km/h\nfor the selected time period.!')
        log_details.config(state='normal')
        log_details.insert(t.INSERT,
                           '\nWind speed not suitable for maximum power production\nfor the selected time period.\n')
        log_details.insert(t.INSERT, '\nWind speed will be less than 20 km/h!!!\n')
        log_details.insert(t.INSERT, '\nLow Power Production Possible !!!\n')
        log_details.config(state='disabled')


def current_weather():
    api_key = '3ee50f44c4e30cacbd795358f1c6531d'
    city_entry = cityE.get()
    country_entry = countryE.get()
    lat = latitudeE.get()
    lon = longitudeE.get()
    current_data_header = []
    current_data = []
    geo_locator = Nominatim(user_agent="WinPS")
    if city_entry != '' and country_entry != '':
        owm = OWM(api_key)
        mgr = owm.weather_manager()
        loc = city_entry + ', ' + country_entry
        observation = ''
        try:
            observation = mgr.weather_at_place(loc)
        except:
            t.messagebox.showinfo('WinPS-1.1 INFO!!', 'Something bad Happened.\nCheck your Internet connection and make sure location is entered correctly.!')
            log_details.config(state='normal')
            log_details.insert(t.INSERT, '\nSomething bad Happened.\n')
            log_details.insert(t.INSERT,
                               '\nCheck your Internet connection and make sure location is entered correctly !!\n')
            log_details.config(state='disabled')
        current_data_header = ['Time', 'Location', 'Temperature', 'Wind Speed', 'Description', 'Pressure']
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
    elif lat != '' and lon != '':
        owm = OWM(api_key)
        mgr = owm.weather_manager()
        location = geo_locator.reverse(lat + "," + lon)
        address = location.raw['address']
        city_name = address.get('city', '')
        if city_name == '':
            city_name = address.get('town', '')
        country_name = address.get('country', '')
        loc = str(city_name) + ', ' + str(country_name)
        observation = ''
        try:
            observation = mgr.weather_at_coords(float(lat), float(lon))
        except:
            t.messagebox.showinfo('WinPS-1.1 INFO!!',
                                  'Something bad Happened.\nCheck your Internet connection and make sure location is entered correctly.!')
            log_details.config(state='normal')
            log_details.insert(t.INSERT, '\nSomething bad Happened.\n')
            log_details.insert(t.INSERT,
                               '\nCheck your Internet connection and make sure location is entered correctly !!\n')
            log_details.config(state='disabled')
        current_data_header = ['Time', 'Location', 'Temperature', 'Wind Speed', 'Description', 'Pressure']
        # current weather section...................................................................................
        data = []
        curr_time = datetime.datetime.now()
        current_time = curr_time.strftime("%H:%M:%S")
        curr_date = str(curr_time.day) + '/' + str(curr_time.month) + '/' + str(curr_time.year)
        curr_time_stamp = str(current_time) + ' on ' + curr_date
        data.append(curr_time_stamp)
        data.append(str(loc))
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
    log_details.insert(t.INSERT, str(loc) + '\n')
    log_details.insert(t.INSERT, 'Date:  ' + str(curr_date) + '\n')
    log_details.insert(t.INSERT, 'Time:  ' + str(current_time) + '\n')
    log_details.insert(t.INSERT, 'Current Temperature: ' + str(temperature) + ' degree C\n')
    log_details.insert(t.INSERT, 'Current Wind Speed in mps: ' + str(wind) + ' m/s\n')
    log_details.insert(t.INSERT, 'Current Wind Speed in kph:  ' + str(windSpeed) + ' km/h\n')
    log_details.insert(t.INSERT, 'Current Atmospheric Pressure:  ' + str(pressure) + '\n')
    log_details.insert(t.INSERT, 'Current Status: ' + str(status) + '\n')
    log_details.config(state='disabled')
    if not os.path.isfile('current_weather_data.csv'):
        try:
            with open('current_weather_data.csv', 'w', encoding="UTF8", newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(current_data_header)
                csv_writer.writerows(current_data)
        except PermissionError:
            t.messagebox.showerror('WinPS-1.1', 'Permission Denied to entry data.\nMake Sure The data file is closed.')
            log_details.config(state='normal')
            log_details.insert(t.INSERT,
                               '\nPermission Denied to entry data.\n\nMake Sure The data file is closed.\n\n')
            log_details.config(state='disabled')
    else:
        if os.stat('current_weather_data.csv').st_size == 0:
            try:
                with open('current_weather_data.csv', 'w', encoding="UTF8", newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(current_data_header)
                    csv_writer.writerows(current_data)
            except PermissionError:
                t.messagebox.showerror('WinPS-1.1',
                                       'Permission Denied to entry data.\nMake Sure The data file is closed.')
                log_details.config(state='normal')
                log_details.insert(t.INSERT,
                                   '\nPermission Denied to entry data.\n\nMake Sure The data file is closed.\n')
                log_details.config(state='disabled')
        else:
            try:
                with open('current_weather_data.csv', 'a', encoding="UTF8", newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerows(current_data)
            except PermissionError:
                t.messagebox.showerror('WinPS-1.1',
                                       'Permission Denied to entry data.\nMake Sure The data file is closed.')
                log_details.config(state='normal')
                log_details.insert(t.INSERT,
                                   '\nPermission Denied to entry data.\n\nMake Sure The data file is closed.\n')
                log_details.config(state='disabled')
    current_situation_d(temperature, wind, windSpeed, pressure)
    choice_enter.delete(0, 'end')


def hourly_forecasting():
    # hourly forecast section...............................................................................
    pressure = ''
    url_call = ''
    api_key = '3ee50f44c4e30cacbd795358f1c6531d'
    city_entry = cityE.get()
    country_entry = countryE.get()
    lat = latitudeE.get()
    lon = longitudeE.get()
    wind_mps_list = []
    wind_kps_list = []
    c_temp = []
    f_temp = []
    time_stamp_list = []
    description_list = []
    prediction_power_list = []
    header = ['Date', 'Location', 'Temperature', 'Wind Speed', 'Description', 'Pressure']
    total_data_hourly = []
    log_details.config(state='normal')
    log_details.insert(t.INSERT, '\n\nHourly Forecast.....!!!\n')
    log_details.config(state='disabled')
    geo_locator = Nominatim(user_agent="WinPS")
    if city_entry != '' and country_entry != '':
        api_call_loc = 'https://api.openweathermap.org/data/2.5/weather?q='
        location = city_entry + ',' + country_entry
        url_call_loc = api_call_loc + location + '&appid=' + api_key

        try:
            json_data_loc = requests.get(url_call_loc).json()
        except:
            t.messagebox.showinfo('WinPS-1.1 INFO!!',
                                  'Something bad Happened.\nCheck your Internet connection and make sure location is entered correctly.!')
            log_details.config(state='normal')
            log_details.insert(t.INSERT,
                               '\nSomething bad Happened.\nCheck your Internet connection and\nmake sure location is entered correctly !!\n')
            log_details.config(state='disabled')

        lat = str(json_data_loc['coord']['lat'])
        long = str(json_data_loc['coord']['lon'])

        api_call = 'https://api.openweathermap.org/data/2.5/onecall?lat='
        url_call = api_call + lat + '&lon=' + long + '&exclude=current,minutely,daily&appid=' + api_key

    elif lat != '' and lon != '':
        api_call = 'https://api.openweathermap.org/data/2.5/onecall?lat='
        url_call = api_call + lat + '&lon=' + lon + '&exclude=current,minutely,daily&appid=' + api_key
        location = geo_locator.reverse(lat + "," + lon)
        address = location.raw['address']
        # traverse the data
        city_name = address.get('city', '')
        if city_name == '':
            city_name = address.get('town', '')
        country_name = address.get('country', '')
        location = city_name + ',' + country_name

    try:
        json_data = requests.get(url_call).json()
    except:
        t.messagebox.showinfo('WinPS-1.1 INFO!!',
                              'Something bad Happened.\nCheck your Internet connection and make sure location is entered correctly.!')
        log_details.config(state='normal')
        log_details.insert(t.INSERT,
                           '\nSomething bad Happened.\nCheck your Internet connection and\nmake sure location is entered correctly !!\n')
        log_details.config(state='disabled')

    log_details.config(state='normal')
    log_details.insert(t.INSERT, 'Gathering Forecast.....\n')
    log_details.insert(t.INSERT, str(location) + '\n')
    log_details.config(state='disabled')

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
            yyyy, mm, dd = current_date.split('-')
        date_str = str(dd + '-' + mm + '-' + yyyy)
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
        pressure = item['pressure']
        # Weather condition
        description = item['weather'][0]['description']
        description_list.append(description)
        data.append(description)
        data.append(pressure)
        total_data_hourly.append(data)
    if not os.path.isfile('weather_data_hourly.csv'):
        try:
            with open('weather_data_hourly.csv', 'w', encoding="UTF8", newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(header)
                csv_writer.writerows(total_data_hourly)
        except PermissionError:
            t.messagebox.showerror('WinPS-1.1', 'Permission Denied to entry data.\nMake Sure The data file is closed.')
            log_details.config(state='normal')
            log_details.insert(t.INSERT,
                               '\nPermission Denied to entry data.\n\nMake Sure The data file is closed.\n')
            log_details.config(state='disabled')
    else:
        if os.stat('weather_data_hourly.csv').st_size == 0:
            try:
                with open('weather_data_hourly.csv', 'w', encoding="UTF8", newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(header)
                    csv_writer.writerows(total_data_hourly)
            except PermissionError:
                t.messagebox.showerror('WinPS-1.1',
                                       'Permission Denied to entry data.\nMake Sure The data file is closed.')
                log_details.config(state='normal')
                log_details.insert(t.INSERT,
                                   '\nPermission Denied to entry data.\n\nMake Sure The data file is closed.\n')
                log_details.config(state='disabled')
        else:
            try:
                with open('weather_data_hourly.csv', 'a', encoding="UTF8", newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerows(total_data_hourly)
            except PermissionError:
                t.messagebox.showerror('WinPS-1.1',
                                       'Permission Denied to entry data.\nMake Sure The data file is closed.')
                log_details.config(state='normal')
                log_details.insert(t.INSERT,
                                   '\nPermission Denied to entry data.\n\nMake Sure The data file is closed.\n')
                log_details.config(state='disabled')
    length = len(time_stamp_list)
    prediction(time_stamp_list, c_temp, wind_mps_list, wind_kps_list, prediction_power_list, length, pressure)
    forecast_choice_enter.delete(0, 'end')


def three_hourly_forecasting():
    # three hourly forecast section.........................................................................
    pressure = ''
    api_key = '3ee50f44c4e30cacbd795358f1c6531d'
    city_entry = cityE.get()
    country_entry = countryE.get()
    lat = latitudeE.get()
    lon = longitudeE.get()
    wind_mps_list = []
    wind_kps_list = []
    c_temp = []
    f_temp = []
    time_stamp_list = []
    description_list = []
    prediction_power_list = []
    header = ['Date', 'Location', 'Temperature', 'Wind Speed', 'Description', 'Pressure']
    total_data_3hourly = []
    geo_locator = Nominatim(user_agent="WinPS")
    log_details.config(state='normal')
    log_details.insert(t.INSERT, '\n\nThree Hourly Forecast.....!!!\n')
    log_details.config(state='disabled')
    url_call = ''
    loc = ''
    if city_entry != '' and country_entry != '':
        api_call = 'https://api.openweathermap.org/data/2.5/forecast?appid=' + api_key  # for three hourly
        url_call = api_call + '&q=' + city_entry  # for three hourly for five days
        loc = str(city_entry) + ', ' + str(country_entry)
    elif lat != '' and lon != '':
        api_call = 'https://api.openweathermap.org/data/2.5/forecast?lat=' + lat + '&lon=' + lon + '&appid=' + api_key
        url_call = api_call
        location_three_h = geo_locator.reverse(lat + "," + lon)
        address_three_h = location_three_h.raw['address']
        city_entry = address_three_h.get('city', '')
        if city_entry == '':
            city_entry = address_three_h.get('town', '')
        country_entry = address_three_h.get('country', '')
        loc = str(city_entry) + ', ' + str(country_entry)
    call = ''
    try:
        call = requests.get(url_call)
    except:
        t.messagebox.showinfo('WinPS-1.1 INFO!!',
                              'Something bad Happened.\nCheck your Internet connection and make sure location is entered correctly.!')
        log_details.config(state='normal')
        log_details.insert(t.INSERT,
                           '\nSomething bad Happened.\nCheck your Internet connection and\nmake sure location is entered correctly !!\n')
        log_details.config(state='disabled')
    json_data = call.json()
    log_details.config(state='normal')
    log_details.insert(t.INSERT, '\nGathering Forecast.....\n')
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
        # loading time stamps  in list
        time_stamp = str(hour) + ' ' + str(meridian) + ' ' + date_str
        time_stamp_list.append(time_stamp)
        data.append(time_stamp)
        data.append(str(loc))
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
        pressure = item['main']['pressure']
        # Weather condition
        description = item['weather'][0]['description']
        description_list.append(description)
        data.append(description)
        data.append(pressure)
        total_data_3hourly.append(data)
    if not os.path.isfile('weather_data_3hourly.csv'):
        try:
            with open('weather_data_3hourly.csv', 'w', encoding="UTF8", newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(header)
                csv_writer.writerows(total_data_3hourly)
        except PermissionError:
            t.messagebox.showerror('WinPS-1.1', 'Permission Denied to entry data.\nMake Sure The data file is closed.')
            log_details.config(state='normal')
            log_details.insert(t.INSERT,
                               '\nPermission Denied to entry data.\n\nMake Sure The data file is closed.\n\n')
            log_details.config(state='disabled')
    else:
        if os.stat('weather_data_3hourly.csv').st_size == 0:
            try:
                with open('weather_data_3hourly.csv', 'w', encoding="UTF8", newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(header)
                    csv_writer.writerows(total_data_3hourly)
            except PermissionError:
                t.messagebox.showerror('WinPS-1.1', 'Permission Denied to entry data.\nMake Sure The data file is closed.')
                log_details.config(state='normal')
                log_details.insert(t.INSERT,
                                   '\nPermission Denied to entry data.\n\nMake Sure The data file is closed.\n')
                log_details.config(state='disabled')
        else:
            try:
                with open('weather_data_3hourly.csv', 'a', encoding="UTF8", newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerows(total_data_3hourly)
            except PermissionError:
                t.messagebox.showerror('WinPS-1.1',
                                       'Permission Denied to entry data.\nMake Sure The data file is closed.')
                log_details.config(state='normal')
                log_details.insert(t.INSERT,
                                   '\nPermission Denied to entry data.\n\nMake Sure The data file is closed.\n')
                log_details.config(state='disabled')

    length = len(time_stamp_list)
    prediction(time_stamp_list, c_temp, wind_mps_list, wind_kps_list, prediction_power_list, length, pressure)
    forecast_choice_enter.delete(0, 'end')


def decision():
    main_choice = choice_enter.get()
    forecast_choice = forecast_choice_enter.get()
    cityText = cityE.get()
    countryText = countryE.get()
    lat = latitudeE.get()
    lon = longitudeE.get()
    email = variable.get()

    if cityText == '' and countryText == '' and lat == '' and lon == '':
        t.messagebox.showerror('WinPS-1.1', 'Enter Your Location First.!')
        log_details.config(state='normal')
        log_details.insert(t.INSERT, '\nEnter Your Location First !!!\n')
        log_details.config(state='disabled')
    else:
        if email == 'Select any one' or email == 'Choose any email':
            t.messagebox.showerror('WinPS-1.1', 'Please Select one Email first.!')
            log_details.config(state='normal')
            log_details.insert(t.INSERT, '\nPlease Select one Email first !!\n')
            log_details.config(state='disabled')
        else:
            if main_choice == '':
                t.messagebox.showerror('WinPS-1.1',
                                       'Choose any option.!')
                log_details.config(state='normal')
                log_details.insert(t.INSERT, '\nChoose any option !!!\n')
                log_details.config(state='disabled')
            elif main_choice == '1':
                if forecast_choice == 'H' or forecast_choice == 'h':
                    hourly_forecasting()
                elif forecast_choice == '3H' or forecast_choice == '3h':
                    three_hourly_forecasting()
                elif forecast_choice == '':
                    t.messagebox.showerror('WinPS-1.1',
                                           'Choose any Forecast Type.!')
                    log_details.config(state='normal')
                    log_details.insert(t.INSERT, '\nChoose any Forecast Type !!!\n')
                    log_details.config(state='disabled')
                else:
                    t.messagebox.showerror('WinPS-1.1',
                                           'Invalid Forecast Type.!')
                    log_details.config(state='normal')
                    log_details.insert(t.INSERT, '\nInvalid Forecast Type !!!\n')
                    log_details.config(state='disabled')
            elif main_choice == '2':
                current_weather()
            else:
                t.messagebox.showerror('WinPS-1.1',
                                       'Invalid Choice.!')
                log_details.config(state='normal')
                log_details.insert(t.INSERT, '\nInvalid Choice !!!\n')
                log_details.config(state='disabled')


def reset():
    choice_enter.delete(0, 'end')
    forecast_choice_enter.delete(0, 'end')
    cityE.config(state='normal')
    cityE.delete(0, 'end')
    countryE.config(state='normal')
    countryE.delete(0, 'end')
    latitudeE.config(state='normal')
    longitudeE.config(state='normal')
    latitudeE.delete(0, 'end')
    longitudeE.delete(0, 'end')
    cityE.config(state='disabled')
    countryE.config(state='disabled')
    latitudeE.config(state='disabled')
    longitudeE.config(state='disabled')


def add():
    new_Email_text = new_EmailE.get()
    row_Email = [new_Email_text]
    if new_Email_text == '':
        t.messagebox.showerror('WinPS 1.1', 'Please Enter any Email to ADD. !')
        log_details.config(state='normal')
        log_details.insert(t.INSERT,
                           '\nPlease Enter any Email to ADD. !\n\n')
        log_details.config(state='disabled')
    elif new_Email_text[-10:] != '@gmail.com':
        t.messagebox.showerror('WinPS 1.1', 'Please Enter a Valid Email to ADD. !')
        log_details.config(state='normal')
        log_details.insert(t.INSERT,
                           '\nPlease Enter a Valid Email to ADD. !\n\n')
        log_details.config(state='disabled')
    else:
        if not os.path.isfile('Emails.csv'):
            headerE = ['Email']
            try:
                with open('Emails.csv', 'w', newline='') as csv_file_email:
                    csv_write = csv.writer(csv_file_email)
                    csv_write.writerow(headerE)
            except PermissionError:
                t.messagebox.showerror('WinPS 1.1',
                                       'Permission Denied to entry data.\nMake Sure The data file is closed.')
                log_details.config(state='normal')
                log_details.insert(t.INSERT,
                                   '\nPermission Denied to entry data.\n\nMake Sure The data file is closed.\n\n')
                log_details.config(state='disabled')
        elif os.stat('Emails.csv').st_size == 0:
            headerE = ['Email']
            try:
                with open('Emails.csv', 'w', newline='') as csv_file_email:
                    csv_write = csv.writer(csv_file_email)
                    csv_write.writerow(headerE)
            except PermissionError:
                t.messagebox.showerror('WinPS 1.1',
                                       'Permission Denied to entry data.\nMake Sure The data file is closed.')
                log_details.config(state='normal')
                log_details.insert(t.INSERT,
                                   '\nPermission Denied to entry data.\n\nMake Sure The data file is closed.\n\n')
                log_details.config(state='disabled')
        else:
            try:
                with open('Emails.csv', 'a', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(row_Email)
            except PermissionError:
                t.messagebox.showerror('WinPS 1.1',
                                       'Permission Denied to entry data.\nMake Sure The data file is closed.')
                log_details.config(state='normal')
                log_details.insert(t.INSERT,
                                   '\nPermission Denied to entry data.\n\nMake Sure The data file is closed.\n')
                log_details.config(state='disabled')
            new_EmailE.delete(0, 'end')
            t.messagebox.showinfo('WinPS 1.1', 'For Viewing newly added Email.\nPlease Restart the App !')
            log_details.config(state='normal')
            log_details.insert(t.INSERT, 'New Email Added ->  ' + str(new_Email_text) + '\n')
            log_details.insert(t.INSERT, '\nFor Viewing newly added Email, Please Restart the App !!\n\n')
            log_details.config(state='disabled')


def delete_item():
    memberName = variable.get()
    temp = []
    file_Name = 'Emails.csv'
    if memberName == 'Select any one' or memberName == 'Choose any email':
        t.messagebox.showinfo('WinPS 1.1', 'Select an Email !')
        log_details.config(state='normal')
        log_details.insert(t.INSERT, '\nPlease Select one Email first !!\n')
        log_details.config(state='disabled')
    else:
        if not os.path.isfile(file_Name):
            t.messagebox.showerror('WinPS 1.1', 'NO FILE FOUND TO STORE !')
            log_details.config(state='normal')
            log_details.insert(t.INSERT, '\nNO FILE FOUND TO STORE !!\n')
            log_details.config(state='disabled')
        else:
            open_file = open(file_Name, 'r')
            file_opn = csv.DictReader(open_file)
            for row in file_opn:
                if str(row['Email']) != str(memberName):
                    temp.append(row['Email'])
                else:
                    t.messagebox.showinfo('WinPS 1.1', 'For Viewing Newly Modified Email List\nPlease Restart The App!')
                    log_details.config(state='normal')
                    log_details.insert(t.INSERT, '\nEmail ' + str(memberName) + ' Deleted !!\n')
                    log_details.insert(t.INSERT, '\nFor Viewing Newly Modified Email List, Please Restart The App !!\n\n')
                    log_details.config(state='disabled')
            open_file.close()
            os.remove(file_Name)
            header = ['Email']
            try:
                with open(file_Name, 'w') as csv_file_email:
                    csv_write = csv.writer(csv_file_email)
                    csv_write.writerow(header)
                    for inp in temp:
                        entry = [inp]
                        csv_write.writerow(entry)
            except PermissionError:
                log_details.config(state='normal')
                log_details.insert(t.INSERT,
                                   '\nPermission Denied to entery data.\n\nMake Sure The data file is closed.\n')
                log_details.config(state='disabled')


def clear_log():
    log_details.config(state='normal')
    log_details.delete(1.0, 'end')
    log_details.config(state='disabled')


def one():
    latitudeE.delete(0, 'end')
    latitudeE.config(state='disabled')
    longitudeE.delete(0, 'end')
    longitudeE.config(state='disabled')
    cityE.config(state='normal')
    countryE.config(state='normal')


def two():
    cityE.delete(0, 'end')
    cityE.config(state='disabled')
    countryE.delete(0, 'end')
    countryE.config(state='disabled')
    latitudeE.config(state='normal')
    longitudeE.config(state='normal')


def help_section():
    webbrowser.open_new_tab('UserManual.html')


# GUI SECTION

sender = 'karsumon131@gmail.com'

main = t.Tk()
height = main.winfo_screenheight()
width = main.winfo_screendepth()
main.title('WinPS-1.1')
main.geometry("1353x733+0+0")
main.configure(bg='#06789a')

back_img = t.PhotoImage(file='weather.png')
main_back = t.Label(main, image=back_img)
main_back.place(x=10, y=97)

image = Image.open('GEC.png')
image = image.resize((80, 80), Image.ANTIALIAS)
company_logo = ImageTk.PhotoImage(image)
company_logo_L = t.Label(main, image=company_logo)
company_logo_L.place(x=5, y=5, width=84, height=84)

image2 = Image.open('logo.png')
image2 = image2.resize((70, 70), Image.ANTIALIAS)
company_logo2 = ImageTk.PhotoImage(image2)
company_logo2_L = t.Label(main, image=company_logo2)
company_logo2_L.place(x=95, y=10, width=74, height=74)

image3 = Image.open('logo2.PNG')
image3 = image3.resize((770, 50), Image.ANTIALIAS)
company_logo3 = ImageTk.PhotoImage(image3)
company_logo3_L = t.Label(main, image=company_logo3)
company_logo3_L.place(x=275, y=20, width=774, height=54)

cityHead = t.Label(main, text="ENTER LOCATION", fg='black', bg='#a2ff00', width=50)
cityHead.place(x=40, y=110)
cityHead.config(font=('courier', 14))

# location section starts

city = t.Label(main, text="City: ", fg='black', bg='yellow')
city.place(x=50, y=150)
city.config(font=('courier', 12))
country = t.Label(main, text="Country: ", fg='black', bg='yellow')
country.place(x=50, y=190)
country.config(font=('courier', 12))

cityE = t.Entry(main)
cityE.place(x=160, y=147, height=30, width=152)
cityE.config(state='disabled')
countryE = t.Entry(main)
countryE.place(x=160, y=187, height=30, width=152)
countryE.config(state='disabled')

latitudeL = t.Label(main, text="Lat: ", fg='black', bg='yellow')
latitudeL.place(x=360, y=150)
latitudeL.config(font=('courier', 12))
longitudeL = t.Label(main, text="Lon: ", fg='black', bg='yellow')
longitudeL.place(x=360, y=190)
longitudeL.config(font=('courier', 12))

latitudeE = t.Entry(main)
latitudeE.place(x=430, y=147, height=30, width=152)
latitudeE.config(state='disabled')
longitudeE = t.Entry(main)
longitudeE.place(x=430, y=187, height=30, width=152)
longitudeE.config(state='disabled')

option_one = t.Button(main, text='1. Physical Address', fg='white', bg='#001555', width=15, command=one)
option_one.place(x=140, y=230)
option_one.config(font=('verna', 10))

option_two = t.Button(main, text='2. Geo Coordinates', fg='white', bg='#001555', width=15, command=two)
option_two.place(x=420, y=230)
option_two.config(font=('verna', 10))

# Email Entry

emails = ['Select any one']
email_count = 0
if not os.path.isfile('Emails.csv'):
    file_open = open('Emails.csv', 'w')
    file_open.close()
else:
    fileName = open('Emails.csv', 'r')
    file = csv.DictReader(fileName)
    for col in file:
        emails.append(col['Email'])
        email_count = email_count + 1
    fileName.close()

Authority_Email = t.Label(main, text='Authority Email: ', fg='black', bg='yellow')
Authority_Email.place(x=20, y=275)
Authority_Email.config(font=('verna', 14))

variable = t.StringVar(main)
variable.set("Choose any email")

Email_E = t.OptionMenu(main, variable, *emails)
Email_E.place(x=170, y=274, height=30, width=315)
Email_E.config(font=('verna', 10), bg='#d457ff', fg='#002e1f')

email_delete_button = t.Button(main, text='Delete Selected Email', fg='black', bg='#c8b10f', width=17,
                               command=delete_item)
email_delete_button.place(x=495, y=275)

email_count_L = t.Label(main, text='Email Count', fg='black', bg='#98ff04', width=12)
email_count_L.place(x=600, y=240)
email_count_L.config(font=('courier', 10))

email_count_T = t.Text(main)
email_count_T.place(x=630, y=274, height=30, width=45)
email_count_T.config(font=('verna', 14))
email_count_T.config(state='normal')
email_count_T.insert(t.INSERT, '  ' + str(email_count))
email_count_T.config(state='disabled')

# Actions

head = t.Label(main, text='TYPE YOUR CHOICE FROM THE OPTIONS BELOW: ->', fg='white', bg='#197e62', width=50)
head.place(x=40, y=320)
head.config(font=('courier', 14))

choice1 = t.Label(main, text='1. FORECAST (Enter 1)                                ', bg='#50c51d')
choice1.place(x=80, y=360)

choice2 = t.Label(main, text='2. CURRENT WEATHER (Enter 2)               ', bg='orange')
choice2.place(x=80, y=390)

choice_label = t.Label(main, text='Enter your choice here: ', fg='white', bg='#9330f1')
choice_label.place(x=50, y=420)
choice_label.config(font=('courier', 12))

choice_enter = t.Entry(main)
choice_enter.place(x=310, y=417, height=30, width=252)

forecast_choice_label = t.Label(main, text='ENTER YOUR FORECAST METHOD: ->', fg='white', bg='#197e62', width=50)
forecast_choice_label.place(x=50, y=470)
forecast_choice_label.config(font=('courier', 14))

forecast_choice1 = t.Label(main, text='1. TWO DAYS HOURLY (Enter H)             ', fg='black', bg='#50c51d')
forecast_choice1.place(x=80, y=510)

forecast_choice2 = t.Label(main, text='2. FIVE DAYS THREE HOURLY (Enter 3H)', fg='black', bg='orange')
forecast_choice2.place(x=80, y=540)

choice_label_forecast = t.Label(main, text='Enter your choice here: ', fg='white', bg='#9330f1')
choice_label_forecast.place(x=50, y=575)
choice_label_forecast.config(font=('courier', 12))

forecast_choice_enter = t.Entry(main)
forecast_choice_enter.place(x=310, y=572, height=30, width=252)

reset = t.Button(main, text='Refresh', fg='white', bg='#5f101c', width=15, command=reset)
reset.place(x=40, y=660)

start = t.Button(main, text='Start', fg='white', bg='green', width=15, command=decision)
start.place(x=240, y=660)

stop = t.Button(main, text='Stop', fg='white', bg='red', width=15, command=exit)
stop.place(x=440, y=660)

log_details_label = t.Label(main, text='LOG DETAILS', fg='black', bg='#17deb4', width=30)
log_details_label.place(x=880, y=100)
log_details_label.config(font=('courier', 12))

log_details = t.Text(main)
log_details.place(x=700, y=130, height=500, width=645)
log_details.config(state='disabled')

scroll_bar = t.Scrollbar(log_details, orient='vertical', command=log_details.yview())
scroll_bar.pack(side='right', fill='y')
log_details.configure(yscrollcommand=scroll_bar.set)

clear_log_details = t.Button(main, text='Clear Log Details', fg='black', bg='#ffd904', width=15, command=clear_log)
clear_log_details.place(x=1200, y=640)
clear_log_details.config(font=('Verna', 12))

Add_Email = t.Label(main, text='Add New Email: ', fg='black', bg='#3cb86b')
Add_Email.place(x=710, y=660)
Add_Email.config(font=('verna', 12))

new_EmailE = t.Entry(main)
new_EmailE.place(x=730, y=690, height=30, width=240)

Add_EmailB = t.Button(main, text='ADD', fg='white', bg='#3d073f', width=15, command=add)
Add_EmailB.place(x=990, y=690)

help_button_label = t.Label(main, text='Help ?', fg='black', bg='#3cb86b')
help_button_label.place(x=1260, y=20)
help_button_label.config(font=('verdana', 10))
help_button_image = Image.open('help_button.jpg')
help_button_width = 30
help_button_height = 30
help_button_image = help_button_image.resize((help_button_width, help_button_height), Image.ANTIALIAS)
help_button_logo = ImageTk.PhotoImage(help_button_image)
help_button = t.Button(main, image=help_button_logo, command=help_section)
help_button.place(x=1310, y=15, width=help_button_width, height=help_button_height)

main.mainloop()
