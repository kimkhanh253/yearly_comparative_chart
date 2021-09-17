from django.shortcuts import render
#from django.http import HttpResponse, HttpResponseRedirect
from .models import InputBox
import pandas as pd
import json
import requests
from datetime import datetime

API_URL = 'http://data.rcc-acis.org/StnData'
elements_avgt = [{
    'name':'avgt',
    'interval':'dly',
    'duration':'dly',
    'normal':'1'
}]
elements_pcpn = [{
    'name':'pcpn',
    'interval':'dly',
    'duration':'dly',
    'normal':'1'
}]

def get_station_data (station_id, year, w_normal, form): 
    if station_id !='' and station_id !='----':   
        req = requests.get('http://data.rcc-acis.org/StnData?sid={}&sdate={}0101&edate={}1231&elems=avgt,pcpn&output=json&meta=name'.format(station_id, year, year))
        r = req.json()
        if 'data' in r:
            df=pd.DataFrame(r['data'])
            df.columns=['time','avgt','rainfall']
            df['rainfall'] = df['rainfall'].replace('T',0).replace('M',0)
            df['avgt'] = df['avgt'].replace('T',0).replace('M',0)
            df['time']= pd.to_datetime(df['time'],format='%Y-%m-%d')
            df['avgt']=df['avgt'].astype(float)
            df['rainfall']=df['rainfall'].astype(float)
            rain=[]
            name=str(station_id)
            avgTemp=[]
            time=[]
            for d in df.index:
                avgTemp.append(df['avgt'][d])
                rain.append(df['rainfall'][d])
                time.append(str(df['time'][d]))
            
            content_to_update = ({
                'avgTemp':avgTemp,
                'rain': rain,
                'time':time
            })
        else:
            content_to_update = ({
                'avgTemp':[],
                'rain': [],
                'time':[]
            })
        return content_to_update
    else:
        content_to_update = ({
            'avgTemp':[],
            'rain': [],
            'time':[],
            'normal_avgt':[], 
            'normal_pcpn':[]
        })
        return content_to_update

def get_normal_data(station_id, start, end):
    params_avgt = {
        'sid':station_id,
        'sdate': start,
        'edate': end,
        'elems':elements_avgt
    }

    req_normal_avgt = requests.post(url=API_URL, data=json.dumps(params_avgt),headers={'content-type': 'application/json'})
    r_normal_avgt = req_normal_avgt.json()
    df_normal_avgt = pd.DataFrame(r_normal_avgt['data'])
    df_normal_avgt.columns=['time','avgt']
    df_normal_avgt['avgt'] = df_normal_avgt['avgt'].replace('T',0).replace('M',0)
    normal_avgt = [float(i) for i in df_normal_avgt['avgt']]

    params_pcpn = {
        'sid':station_id,
        'sdate': start,
        'edate': end,
        'elems':elements_pcpn
    }

    req_normal_pcpn =  requests.post(url=API_URL, data=json.dumps(params_pcpn),headers={'content-type': 'application/json'})
    r_normal_pcpn = req_normal_pcpn.json()
    df_normal_pcpn=pd.DataFrame(r_normal_pcpn['data'])
    df_normal_pcpn.columns=['time','pcpn']
    df_normal_pcpn['pcpn'] = df_normal_pcpn['pcpn'].replace('T',0).replace('M',0)
    normal_pcpn = [float(i) for i in df_normal_pcpn['pcpn']]

    content_to_update = {'normal_avgt':normal_avgt, 'normal_pcpn':normal_pcpn}
    return content_to_update

def index (request):
    if request.method == 'POST':
        form = InputBox(request.POST or None, initial={'station1': 'ssss','station2': 'iiii', 'station3': 'uuuu', 'year': '0000', 'w_normal1':'false','w_normal2':'false','w_normal3':'false'})
        if form.is_valid():
            station1=form['station1'].data
            station1=str(station1).upper()
            station2=form['station2'].data
            station2=str(station2).upper()
            station3=form['station3'].data
            station3=str(station3).upper()
            w_normal1 = form['w_normal1'].data
            w_normal2 = form['w_normal2'].data
            w_normal3 = form['w_normal3'].data
            year = form['year'].data
            
            start = year+'-01-01'
            end = year+'-12-31'
            content ={
                'form':form,
                'year':year, 
                'name1':station1,
                'name2':station2,
                'name3':station3,
                'w_normal1':w_normal1, 
                'w_normal2':w_normal2, 
                'w_normal3':w_normal3
            }

            content['station1'] = get_station_data (station1, year, w_normal1, form)
            if w_normal1==True:
                new_content = get_normal_data(station1, start, end) 
                content['station1'].update(new_content)
            else:
                content['station1']['normal_avgt'] = []
                content['station1']['normal_pcpn'] = []
            
            content['station2'] =  get_station_data (station2, year, w_normal2, form)
            if w_normal2==True:
                new_content = get_normal_data(station2, start, end) 
                content['station2'].update(new_content)
            else:
                content['station2']['normal_avgt'] = []
                content['station2']['normal_pcpn'] = []
            
            content['station3'] =  get_station_data(station3, year, w_normal3, form)
            if w_normal3==True:
                new_content = get_normal_data(station3, start, end) 
                content['station3'].update(new_content)
            else:
                content['station3']['normal_avgt'] = []
                content['station3']['normal_pcpn'] = []
            
            return render(request,'display/index.html/', content)
            
    else:
        form = InputBox()
    return render(request,'display/index.html/', {'form': form})
    

