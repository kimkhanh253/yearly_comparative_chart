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

def check_input_data (station1, station2, station3):
    station_count = 0

def get_station_data (station_id, year, w_normal, form): 
    content_to_update = ({
        'avgTemp':[],
        'rain': [],
        'time':[]
    })
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
    content_to_update.update({
        'normal_avgt':[], 
        'normal_pcpn':[]
    })
    
    if w_normal == True:
        start = year+'-01-01'
        end = year+'-12-31'

        normal_data = get_normal_data(station_id, w_normal, start, end) 
        content_to_update.update(normal_data)
    return content_to_update

def get_normal_data(station_id, w_normal, start, end):
    content_to_update = {
        'normal_avgt':[], 
        'normal_pcpn':[]
    }
    params_avgt = {
        'sid':station_id,
        'sdate': start,
        'edate': end,
        'elems':elements_avgt
    }

    req_normal_avgt = requests.post(url=API_URL, data=json.dumps(params_avgt),headers={'content-type': 'application/json'})
    r_normal_avgt = req_normal_avgt.json()
    if 'data' in r_normal_avgt:
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

        content_to_update = {
            'normal_avgt':normal_avgt, 
            'normal_pcpn':normal_pcpn
        }
    return content_to_update

def index (request):
    if request.method == 'POST':
        form = InputBox(request.POST or None)
        if form.is_valid():
            station1=str(form['station1'].data).upper()
            station2=str(form['station2'].data).upper()
            station3=str(form['station3'].data).upper()
            w_normal1 = form['w_normal1'].data
            w_normal2 = form['w_normal2'].data
            w_normal3 = form['w_normal3'].data
            year = form['year'].data
            
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
            content['station2'] = get_station_data (station2, year, w_normal2, form)
            content['station3'] = get_station_data (station3, year, w_normal3, form)
            
            return render(request,'display/index.html/', content)
            
    else:
        form = InputBox()
    return render(request,'display/index.html/', {'form': form})
    

