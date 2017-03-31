import pyowm

citylist=['Orlando,us','Chicago,us','New York,us','Los Angeles,us']
owm = pyowm.OWM('9ac385293ca9eb73c8a0a663dfc1674a')  
templist={}
def onstream():
    for cityname in citylist:
        observation = owm.weather_at_place(cityname)
        w = observation.get_weather()
        temperature=w.get_temperature('celsius')
        # print cityname,
        # print (temperature),
        templist[cityname]=temperature
    
    return templist
   # for i in range(0,len(temlist)):
   #     name = str(citylist[i])
   #     temp_max = str(temlist[citylist[i]]['temp_max'])
   #     temp_kf = str(temlist[citylist[i]]['temp_kf'])
   #     temp = str(temlist[citylist[i]]['temp'])
   #     temp_min = str(temlist[citylist[i]]['temp_min'])
 
