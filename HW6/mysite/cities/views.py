from django.shortcuts import render
from django.http import HttpResponse
from cities.models import Cities
from weatherAPI import onstream, citylist
import json
def index(request):
    templist = onstream()
    for i in range(0,len(templist)):
        name = str(citylist[i])
        temp_max = str(templist[citylist[i]]['temp_max'])
        temp_kf = str(templist[citylist[i]]['temp_kf'])
        temp = str(templist[citylist[i]]['temp'])
        temp_min = str(templist[citylist[i]]['temp_min'])
        c = Cities(name=name,temp_max=temp_max,temp_kf=temp_kf,temp=temp,temp_min=temp_min)
        c.save()
    if request.method == 'POST':
        search1 = request.POST.get('source')
        search2 = request.POST.get('destination')
        context = []
        if search1 == "None":
            search1_temp_dict={"name":"None","temp":"None","temp_kf":"None","temp_max":"None","temp_min":"None"}
            #search1_temp_dict=["None","None","None","None","None"]
        else:
            search1_temp = str(Cities.objects.get(name=search1)).split(";")
            search1_temp_dict={"name":search1_temp[0],"temp":search1_temp[1],"temp_kf":search1_temp[2],"temp_max":search1_temp[3],"temp_min":search1_temp[4]}
            #search1_temp_dict=[search1_temp[0],search1_temp[1],search1_temp[2],search1_temp[3],search1_temp[4]]
        context.append(search1_temp_dict)
        if search2 == "None":
            search2_temp_dict={"name":"None","temp":"None","temp_kf":"None","temp_max":"None","temp_min":"None"}
            #search2_temp_dict=["None","None","None","None","None"]
        else:         
            search2_temp = str(Cities.objects.get(name=search2)).split(";")
            search2_temp_dict={"name":search2_temp[0],"temp":search2_temp[1],"temp_kf":search2_temp[2],"temp_max":search2_temp[3],"temp_min":search2_temp[4]}
            #search2_temp_dict=[search2_temp[0],search2_temp[1],search2_temp[2],search2_temp[3],search2_temp[4]]
        #context.append(search2_temp_dict)
        context = {'search1':search1_temp_dict, 'search2':search2_temp_dict}
        return render(request, 'weather_result.html', context)
        #return render(request, 'weather_result.html', {'context':json.dumps(context)})

    else:
        return render(request, 'weather_result.html')

