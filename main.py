import tkinter as t
import smtplib
import time
import pyowm
import requests
import datetime
import csv


def forecast_menu_func():
    forecast_menu = t.Tk()
    forecast_menu.title('Forecast Menu')
    forecast_menu.geometry("900x500+230+80")
    forecast_menu.configure(bg='#a2e146')

    head = t.Label(forecast_menu, text='CLICK ON ANY ONE FROM THE MENU', fg='white', bg='#197e62', width='50')
    head.place(x=150, y=50)
    head.config(font=('courier', 12))

    label_help1 = t.Label(forecast_menu, text='(For Two Days)', fg='black', bg='#c8b10f', width='15')
    label_help1.place(x=550, y=140)
    label_help1.config(font=('courier', 12))

    label_help2 = t.Label(forecast_menu, text='(For Five Days)', fg='black', bg='#50c51d', width='15')
    label_help2.place(x=550, y=200)
    label_help2.config(font=('courier', 12))

    forecast_menu1 = t.Label(forecast_menu, text='1. ')
    forecast_menu1.place(x=230, y=140)
    hourly = t.Button(forecast_menu, text='HOURLY', bg='#04bde6', width=30, command=hourly_f)
    hourly.place(x=280, y=140)
    forecast_menu2 = t.Label(forecast_menu, text='2. ')
    forecast_menu2.place(x=230, y=200)
    three_hourly = t.Button(forecast_menu, text='THREE HOURLY', fg='black', bg='#fd7f00', width=30, command=three_hourly_f)
    three_hourly.place(x=280, y=200)


def hourly_f():
    h_f = t.Tk()
    h_f.title('HOURLY FORECAST')
    h_f.geometry("900x500+230+80")
    h_f.configure(bg='#c18a3b')
    start = t.Button(h_f, text='Start', bg='yellow', width=15, command=hourly_forecasting)
    start.place(x=240, y=420)
    stop = t.Button(h_f, text='Stop', fg='white', bg='red', width=15, command=forecast_menu_func)
    stop.place(x=270, y=420)
    stop.place(x=440, y=420)
    log_details_hf = t.Text(h_f)
    log_details_hf.place(x=120, y=10)


def three_hourly_f():
    th_f = t.Tk()
    th_f.title('THREE HOURLY FORECAST')
    th_f.geometry("900x500+230+80")
    th_f.configure(bg='pink')
    start = t.Button(th_f, text='Start', bg='yellow', width=15, command=three_hourly_forecasting)
    start.place(x=240, y=420)
    stop = t.Button(th_f, text='Stop', fg='white', bg='red', width=15, command=forecast_menu_func)
    stop.place(x=270, y=420)
    stop.place(x=440, y=420)
    log_details_thf = t.Text(th_f)
    log_details_thf.place(x=120, y=10)



def current_func():
    current = t.Tk()
    current.title('CURRENT WEATHER')
    current.geometry("900x500+230+80")
    current.configure(bg='light blue')
    start = t.Button(current, text='Start', bg='yellow', width=15, command=current_weather)
    start.place(x=240, y=420)
    stop = t.Button(current, text='Stop', fg='white', bg='red', width=15, command=menu_function)
    stop.place(x=270, y=420)
    stop.place(x=440, y=420)
    log_details_current = t.Text(current)
    log_details_current.place(x=120, y=10)


def menu_function():
    menu = t.Tk()
    menu.title('MENU')
    menu.geometry("900x500+230+80")
    menu.configure(bg='#9330f1')
    head = t.Label(menu, text='CLICK ON ANY ONE FROM THE MENU', fg='white', bg='#197e62', width='50')
    head.place(x=150, y=50)
    head.config(font=('courier', 12))
    menu1 = t.Label(menu, text='1. ')
    menu1.place(x=250, y=120)
    forecast = t.Button(menu, text='FORECASTING', bg='yellow', width=30, command=forecast_menu_func)
    forecast.place(x=300, y=120)

    menu2 = t.Label(menu, text='2. ')
    menu2.place(x=250, y=180)
    current = t.Button(menu, text='CURRENT WEATHER', bg='light green', width=30, command=current_func)
    current.place(x=300, y=180)

    menu3 = t.Label(menu, text='3. ')
    menu3.place(x=250, y=240)
    back = t.Button(menu, text='EXIT', bg='orange', width=30, command=exit)
    back.place(x=300, y=240)


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
    print('density: {} kg/m^3'.format(P))
    if ws < 12:
        time.sleep(1)
        print('Wind speed is not suitable for Energy Production........')
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


def current_weather():
    api_key = '3ee50f44c4e30cacbd795358f1c6531d'

    cityText = cityE.get()
    countryText = countryE.get()

    city_entry = cityText
    country_entry = countryText
    owm = pyowm.OWM(api_key)
    loc = city_entry + ', ' + country_entry
    observation = owm.weather_at_place(loc)

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

    current_situation_d(temperature, wind, windSpeed)
    time.sleep(1)


def hourly_forecasting():
    # hourly forecast section...............................................................................

    cityText = cityE.get()
    countryText = countryE.get()

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


def three_hourly_forecasting():
    # three hourly forecast section.........................................................................

    cityText = cityE.get()
    countryText = countryE.get()

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

    print('Three Hourly Forecast..... !!!')
    api_call = 'https://api.openweathermap.org/data/2.5/forecast?appid=' + api_key  # for three hourly
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


main = t.Tk()
main.title('WinPS-1')
main.geometry("900x500+230+80")

back_img = t.PhotoImage(file='weather.png')
main_back = t.Label(main, image=back_img)
main_back.place(x=0, y=0, relwidth=1, relheight=1)

city = t.Label(main, text="ENTER LOCATION", fg='white', bg='#6a0490', width=50)
city.place(x=180, y=50)
city.config(font=('courier', 14))

city = t.Label(main, text="City: ", fg='black', bg='yellow')
city.place(x=240, y=125)
city.config(font=('courier', 12))
country = t.Label(main, text="Country: ", fg='black', bg='yellow')
country.place(x=240, y=185)
country.config(font=('courier', 12))

cityE = t.Entry(main)
cityE.place(x=350, y=120, height=30, width=252)
countryE = t.Entry(main)
countryE.place(x=350, y=180, height=30, width=252)

Next = t.Button(main, text='Next', fg='white', bg='blue', width=15, command=menu_function)
Next.place(x=280, y=320)
close = t.Button(main, text='Exit', fg='white', bg='red', width=15, command=exit)
close.place(x=450, y=320)

main.mainloop()
