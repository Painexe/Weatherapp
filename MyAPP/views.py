from django.shortcuts import render
# from MyAPP import models
# from MyAPP.models import Weatherforecast

# Create your views here.

import urllib.request
import json
import mysql.connector
import cursor

def index(request):
      if request.method == 'POST': 
        # lat=request.POST.get('lat')
        # lon=request.POST.get('lon')
        
        #city = request.POST['city'] 
        lat = request.POST['lat'] 
        lon = request.POST['lon'] 

        apikey = ''

        #source = urllib.request.urlopen('https://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&appid='+apikey).read()
        source = urllib.request.urlopen('https://api.openweathermap.org/data/2.5/weather?lat='+lat+'&lon='+lon+'&units=metric&appid='+apikey).read()
        list_of_data = json.loads(source)
        cnx = mysql.connector.connect(host='127.0.0.1',user='raj',passwd='django',database='newdb') 
        cursor = cnx.cursor()

        insert_weather_data = ("INSERT INTO newdb.weather_data"
                "(coordinates,description)"
                "VALUES ( %(coordinate)s, %(description)s)")

        data = {
            "country_code": str(list_of_data['sys']['country']) , 
            "coordinate": str(list_of_data['coord']['lon']) + ', ' + str(list_of_data['coord']['lat']),
            "temp": str(list_of_data['main']['temp']) + ' °C',
            "pressure": str(list_of_data['main']['pressure']),
            "humidity": str(list_of_data['main']['humidity']),
            'main': str(list_of_data['weather'][0]['main']),
            'description': str(list_of_data['weather'][0]['description']),
            'icon': list_of_data['weather'][0]['icon'],
            #'precipitation':str(list_of_data['minutely'][0]['precipitation']),
        }
        cursor.execute(insert_weather_data, data)
        cnx.commit()
        # print(data)
        # print(lat,lon)
        # ins=Weatherforecast(lat=lat , lon=lon ,weather=weather)
        # ins.save()
        print("datawritten")
        
        cursor.close() 
        cnx.close()
        print( "Database connection closed")
        print( "Done")

        

      else :
         data = {}
      return render(request, 'main/index.html', data)
cnx = mysql.connector.connect(host='127.0.0.1',
    user='',
    passwd='',
    database='')
cursor = cnx.cursor()
insert_weather_data = ("INSERT INTO `newdb`.`weather_data`"
                "(`latitude`,`longitude`,'description')"
                "VALUES ( %(lat)s, %(lon)s, %(description)s)")
cursor.close() 
cnx.close()
print( "Database connection closed")
print( "Done")
# def saveEnquiry(request):
#     if request.method=="POST":
#         coordinate=request.POST.get('coordinate')
#         weather=request.POST.get('Description')
#         en=Weatherforecast(coordinate=coordinate,weather=weather)
#         en.save()
#     return render(request, 'main/index.html',)