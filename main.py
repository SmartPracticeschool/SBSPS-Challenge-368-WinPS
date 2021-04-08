import tkinter as t
import smtplib
from pyowm.owm import OWM
import requests
import datetime
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def current_situation_d(temp, w, ws, press):
    # p is air density
    P = press / (287.058 * temp)
    # time.sleep(1)
    log_details.config(state='normal')
    log_details.insert(t.INSERT, 'density: ' + str(P) + ' kg/m^3\n')
    log_details.config(state='disabled')
    wind_test = 90
    # ws
    if ws < 20:
        # time.sleep(1)
        log_details.config(state='normal')
        log_details.insert(t.INSERT, 'Wind speed is not suitable for Energy Production... \n' + str(ws) + 'km/h\n')
        # time.sleep(1)
        log_details.insert(t.INSERT, 'Stopping Wind Turbines.....\n')
        log_details.config(state='disabled')
        # time.sleep(1)

    elif 20 <= ws <= 80:
        # time.sleep(1)
        log_details.config(state='normal')
        log_details.insert(t.INSERT, 'Energy production possible..... \n')
        # time.sleep(1)
        log_details.insert(t.INSERT, 'Starting Wind Turbines.....\n')
        r = 58  # average blade length 58 meters
        n = 40  # efficiency in percentage

        power = (1.314 * (r ** 2) * (w ** 3) * P * n) / 100
        # time.sleep(1)
        log_details.insert(t.INSERT, 'Current output: ' + str(power) + 'W ' + str(power / 1000) + 'KW ' + str(
            power / 1000000) + 'MW' + '\n')
        log_details.config(state='disabled')
        # time.sleep(2)

    elif ws >= 81:
        # time.sleep(1)
        log_details.config(state='normal')
        log_details.insert(t.INSERT, '\nWind speed exceeding limit.....\n')
        # time.sleep(1)
        log_details.insert(t.INSERT, '\nTurning off Wind Turbine.....\n')
        log_details.config(state='disabled')
        receiver = variable.get()
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = 'ALERT !!'
        # body = "Alert!!\nThis is an auto-generated E-mail.\nOver Production. Current Wind speed is " + str(ws) + 'km/h'
        body = "Alert!!\nThis is an auto-generated E-mail.\nOver Production. Current Wind speed is " + str(
            wind_test) + 'km/h'
        msg.attach(MIMEText(body, 'plain'))

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(sender, "mgmpisxgmeexshzs")

        message = msg.as_string()

        s.sendmail(sender, receiver, message)
        # time.sleep(1)
        s.quit()
        log_details.config(state='normal')
        log_details.insert(t.INSERT, '\nE-Mail Alert Sent !! \n')
        log_details.config(state='disabled')
        # time.sleep(1)


def prediction(t_s_list, c_t, w_mps_list, w_kps_list, p_d_power_list, len1, pressure):
    log_details.config(state='normal')
    log_details.insert(t.INSERT, '\n-------------This is prediction section-------------\n')
    log_details.config(state='disabled')
    # time.sleep(1)
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
            # time.sleep(1)
            log_details.config(state='normal')
            log_details.insert(t.INSERT, '\nWind speed will be optimum at ' + str(t_s_list[m]) + ' i.e. \n' + str(
                w_kps_list[m]) + 'km/h\n')
            # time.sleep(1)
            log_details.insert(t.INSERT, '\nHigh Time for optimum Production.....\n')
            # time.sleep(1)
            log_details.insert(t.INSERT,
                               '\nPredicted output: \n' + str(p_d_power1) + 'W \n' + str(p_d_power1 / 1000) + 'KW \n' +
                               str(p_d_power1 / 1000000) + 'MW' + '\n')
            log_details.config(state='disabled')
            p_d_power_list.append(p_d_power1)

        elif w_kps_list[m] >= 81:
            # time.sleep(1)
            log_details.config(state='normal')
            log_details.insert(t.INSERT, '\nOver production Alert..... ! ! !\n' + 'Speed= ' + str(w_kps_list[m]))
            # time.sleep(1)
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
            # body = "Alert!!\nThis is an auto-generated E-mail.\nOver Production. Current Wind speed is " + str(wind_test) + 'km/h'
            msg.attach(MIMEText(body, 'plain'))
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("karsumon131@gmail.com", "mgmpisxgmeexshzs")
            message = msg.as_string()
            s.sendmail(sender, receiver, message)
            s.quit()

            # time.sleep(1)
            log_details.config(state='normal')
            log_details.insert(t.INSERT, 'E-Mail Alert Sent !! \n')
            log_details.config(state='disabled')
    if count == len1:
        log_details.config(state='normal')
        log_details.insert(t.INSERT, '\nWind speed not suitable for maximum power production\nfor the '
                                     'selected time period.\n')
        # time.sleep(1)
        log_details.insert(t.INSERT, '\nWind speed will be less than 20 km/h!!!\n')
        # time.sleep(1)
        log_details.insert(t.INSERT, '\nLow Power Production Possible !!!\n')
        log_details.config(state='disabled')
    # time.sleep(1)


def current_weather():
    api_key = '3ee50f44c4e30cacbd795358f1c6531d'

    cityText = cityE.get()
    countryText = countryE.get()

    if cityText == '' and countryText == '':
        log_details.config(state='normal')
        log_details.insert(t.INSERT, 'Enter Your Location First !!!\n')
        log_details.config(state='disabled')
        # time.sleep(4)

    else:
        city_entry = cityText
        country_entry = countryText
        owm = OWM(api_key)
        mgr = owm.weather_manager()
        loc = city_entry + ', ' + country_entry

        observation = ''
        try:
            observation = mgr.weather_at_place(loc)
        except:
            log_details.config(state='normal')
            log_details.insert(t.INSERT,
                               '\nSomething bad Happened.\nCheck your Internet connection and\nmake sure location is entered correctly !!\n')
            log_details.config(state='disabled')

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
        # time.sleep(1)
        log_details.insert(t.INSERT, str(city_entry) + ', ' + str(country_entry) + '\n')
        # time.sleep(2)
        log_details.insert(t.INSERT, 'Date:  ' + str(curr_date) + '\n')
        # time.sleep(2)
        log_details.insert(t.INSERT, 'Time:  ' + str(current_time) + '\n')
        # time.sleep(1)
        log_details.insert(t.INSERT, 'Current Temperature: ' + str(temperature) + ' degree C\n')
        # time.sleep(1)
        log_details.insert(t.INSERT, 'Current Wind Speed in mps: ' + str(wind) + ' m/s\n')
        # time.sleep(1)
        log_details.insert(t.INSERT, 'Current Wind Speed in kph:  ' + str(windSpeed) + ' km/h\n')
        # time.sleep(1)
        log_details.insert(t.INSERT, 'Current Atmospheric Pressure:  ' + str(pressure) + '\n')
        # time.sleep(1)
        log_details.insert(t.INSERT, 'Current Status: ' + str(status) + '\n')
        log_details.config(state='disabled')
        # time.sleep(1)
        with open('current_weather_data.csv', 'a') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(current_data_header)
            csv_writer.writerows(current_data)

        current_situation_d(temperature, wind, windSpeed, pressure)
        # time.sleep(1)
    choice_enter.delete(0, 'end')


def hourly_forecasting():
    # hourly forecast section...............................................................................

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
    header = ['Date', 'Location', 'Temperature', 'Wind Speed', 'Description']
    total_data_hourly = []
    log_details.config(state='normal')
    log_details.insert(t.INSERT, '\n\nHourly Forecast.....!!!\n')
    log_details.config(state='disabled')
    if city_entry != '' and country_entry != '':
        api_call_loc = 'https://api.openweathermap.org/data/2.5/weather?q='
        location = city_entry + ',' + country_entry
        url_call_loc = api_call_loc + location + '&appid=' + api_key

        try:
            json_data_loc = requests.get(url_call_loc).json()
        except:
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
        location = lat + ',' + lon

    try:
        json_data = requests.get(url_call).json()
    except:
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

        pressure = item['pressure']

        # Weather condition
        description = item['weather'][0]['description'],
        description_list.append(description)
        data.append(description)
        total_data_hourly.append(data)

    with open('weather_data_hourly.csv', 'a') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header)
        csv_writer.writerows(total_data_hourly)

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
    header = ['Date', 'Location', 'Temperature', 'Wind Speed', 'Description']
    total_data_3hourly = []

    log_details.config(state='normal')
    log_details.insert(t.INSERT, '\n\nThree Hourly Forecast.....!!!\n')
    log_details.config(state='disabled')

    url_call = ''
    if city_entry != '' and country_entry != '':
        api_call = 'https://api.openweathermap.org/data/2.5/forecast?appid=' + api_key  # for three hourly
        url_call = api_call + '&q=' + city_entry  # for three hourly for five days
    elif lat != '' and lon != '':
        api_call = 'https://api.openweathermap.org/data/2.5/forecast?lat=' + lat + '&lon=' + lon + '&appid=' + api_key
        url_call = api_call

    call = ''
    try:
        call = requests.get(url_call)
    except:
        log_details.config(state='normal')
        log_details.insert(t.INSERT,
                           '\nSomething bad Happened.\nCheck your Internet connection and\nmake sure location is entered correctly !!\n')
        log_details.config(state='disabled')

    json_data = call.json()
    city_entry = json_data['city']['name']
    country_entry = json_data['city']['country']

    loc = city_entry + ',' + country_entry

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

        pressure = item['main']['pressure']

        # Weather condition
        description = item['weather'][0]['description'],
        description_list.append(description)
        data.append(description)
        total_data_3hourly.append(data)
    with open('weather_data_3hourly.csv', 'a') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header)
        csv_writer.writerows(total_data_3hourly)

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
        log_details.config(state='normal')
        log_details.insert(t.INSERT, '\nEnter Your Location First !!!\n')
        log_details.config(state='disabled')
    else:
        if email == 'Select any one' or email == 'Choose any email':
            log_details.config(state='normal')
            log_details.insert(t.INSERT, '\nPlease Select one Email first !!\n')
            log_details.config(state='disabled')
        else:
            if main_choice == '':
                log_details.config(state='normal')
                log_details.insert(t.INSERT, '\nChoose any option !!!\n')
                log_details.config(state='disabled')
            elif main_choice == '1':
                if forecast_choice == 'H' or forecast_choice == 'h':
                    hourly_forecasting()
                elif forecast_choice == '3H' or forecast_choice == '3h':
                    three_hourly_forecasting()
                elif forecast_choice == '':
                    log_details.config(state='normal')
                    log_details.insert(t.INSERT, '\nChoose any Forecast Type !!!\n')
                    log_details.config(state='disabled')
                else:
                    log_details.config(state='normal')
                    log_details.insert(t.INSERT, '\nInvalid Forecast Type !!!\n')
                    log_details.config(state='disabled')
            elif main_choice == '2':
                current_weather()
            else:
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


def add():
    if os.stat('Emails.csv').st_size == 0:
        headerE = ['Email']
        with open('Emails.csv', 'a') as csv_file_email:
            csv_write = csv.writer(csv_file_email)
            csv_write.writerow(headerE)
    else:
        new_Email_text = new_EmailE.get()
        row_Email = [new_Email_text]
        with open('Emails.csv', 'a') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(row_Email)
        new_EmailE.delete(0, 'end')
        log_details.config(state='normal')
        log_details.insert(t.INSERT, 'New Email Added ->  ' + str(new_Email_text) + '\n')
        log_details.insert(t.INSERT, 'Please Restart the App !!\n')
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
main_back.place(x=10, y=7)

cityHead = t.Label(main, text="ENTER LOCATION", fg='black', bg='#a2ff00', width=50)
cityHead.place(x=40, y=20)
cityHead.config(font=('courier', 14))

# location section starts


city = t.Label(main, text="City: ", fg='black', bg='yellow')
city.place(x=50, y=60)
city.config(font=('courier', 12))
country = t.Label(main, text="Country: ", fg='black', bg='yellow')
country.place(x=50, y=100)
country.config(font=('courier', 12))

cityE = t.Entry(main)
cityE.place(x=160, y=57, height=30, width=152)
countryE = t.Entry(main)
countryE.place(x=160, y=97, height=30, width=152)

latitudeL = t.Label(main, text="Lat: ", fg='black', bg='yellow')
latitudeL.place(x=360, y=60)
latitudeL.config(font=('courier', 12))
longitudeL = t.Label(main, text="Lon: ", fg='black', bg='yellow')
longitudeL.place(x=360, y=100)
longitudeL.config(font=('courier', 12))

latitudeE = t.Entry(main)
latitudeE.place(x=430, y=57, height=30, width=152)
longitudeE = t.Entry(main)
longitudeE.place(x=430, y=97, height=30, width=152)

option_one = t.Button(main, text='1.', fg='white', bg='#001555', width=15, command=one)
option_one.place(x=140, y=140)
option_one.config(font=('verna', 10))

option_two = t.Button(main, text='2.', fg='white', bg='#001555', width=15, command=two)
option_two.place(x=420, y=140)
option_two.config(font=('verna', 10))

# Email Entry

emails = ['Select any one']
email_count = 0
fileName = open('Emails.csv', 'r')
file = csv.DictReader(fileName)
for col in file:
    emails.append(col['Email'])
    email_count = email_count + 1

Authority_Email = t.Label(main, text='Authority Email: ', fg='black', bg='yellow')
Authority_Email.place(x=100, y=185)
Authority_Email.config(font=('verna', 14))

variable = t.StringVar(main)
variable.set("Choose any email")

Email_E = t.OptionMenu(main, variable, *emails)
Email_E.place(x=250, y=184, height=30, width=350)
Email_E.config(font=('verna', 10), bg='#d457ff', fg='#002e1f')

email_count_L = t.Label(main, text='Email Count', fg='black', bg='#98ff04', width=12)
email_count_L.place(x=600, y=150)
email_count_L.config(font=('courier', 10))

email_count_T = t.Text(main)
email_count_T.place(x=630, y=184, height=30, width=45)
email_count_T.config(font=('verna', 14))
email_count_T.config(state='normal')
email_count_T.insert(t.INSERT, '  ' + str(email_count))
email_count_T.config(state='disabled')

# Actions

head = t.Label(main, text='TYPE YOUR CHOICE FROM THE OPTIONS BELOW: ->', fg='white', bg='#197e62', width=50)
head.place(x=40, y=230)
head.config(font=('courier', 14))

choice1 = t.Label(main, text='1. FORECAST (Enter 1)', bg='#50c51d', width=35)
choice1.place(x=80, y=270)

choice2 = t.Label(main, text='2. CURRENT WEATHER (Enter 2)', bg='orange', width=35)
choice2.place(x=80, y=300)

choice_label = t.Label(main, text='Enter your choice here: ', fg='white', bg='#9330f1')
choice_label.place(x=50, y=330)
choice_label.config(font=('courier', 12))

choice_enter = t.Entry(main)
choice_enter.place(x=310, y=327, height=30, width=252)

forecast_choice_label = t.Label(main, text='ENTER YOUR FORECAST METHOD: ->', fg='white', bg='#197e62', width=50)
forecast_choice_label.place(x=50, y=380)
forecast_choice_label.config(font=('courier', 14))

forecast_choice1 = t.Label(main, text='1. TWO DAYS HOURLY (Enter H)', fg='black', bg='#50c51d', width=35)
forecast_choice1.place(x=80, y=420)

forecast_choice2 = t.Label(main, text='2. FIVE DAYS THREE HOURLY (Enter 3H)', fg='black', bg='#c8b10f', width=35)
forecast_choice2.place(x=80, y=450)

choice_label_forecast = t.Label(main, text='Enter your choice here: ', fg='white', bg='#9330f1')
choice_label_forecast.place(x=50, y=485)
choice_label_forecast.config(font=('courier', 12))

forecast_choice_enter = t.Entry(main)
forecast_choice_enter.place(x=310, y=482, height=30, width=252)

reset = t.Button(main, text='Reset', fg='white', bg='#5f101c', width=15, command=reset)
reset.place(x=40, y=570)

start = t.Button(main, text='Start', fg='white', bg='green', width=15, command=decision)
start.place(x=240, y=570)

stop = t.Button(main, text='Stop', fg='white', bg='red', width=15, command=exit)
stop.place(x=440, y=570)

log_details_label = t.Label(main, text='LOG DETAILS', fg='black', bg='#17deb4', width=30)
log_details_label.place(x=880, y=10)
log_details_label.config(font=('courier', 12))

log_details = t.Text(main)
log_details.place(x=700, y=40, height=500, width=645)
log_details.config(state='disabled')

scroll_bar = t.Scrollbar(log_details, orient='vertical', command=log_details.yview())
scroll_bar.pack(side='right', fill='y')
log_details.configure(yscrollcommand=scroll_bar.set)
# scroll_bar.config()

clear_log_details = t.Button(main, text='Clear Log Details', fg='black', bg='#ffd904', width=15, command=clear_log)
clear_log_details.place(x=1200, y=550)
clear_log_details.config(font=('Verna', 12))

Add_Email = t.Label(main, text='Add New Email: ', fg='black', bg='#3cb86b')
Add_Email.place(x=710, y=570)
Add_Email.config(font=('verna', 12))

new_EmailE = t.Entry(main)
new_EmailE.place(x=730, y=600, height=30, width=240)

Add_EmailB = t.Button(main, text='ADD', fg='white', bg='#3d073f', width=15, command=add)
Add_EmailB.place(x=990, y=600)

main.mainloop()
