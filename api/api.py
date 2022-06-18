import time
import requests
import os
import json
from flask import Flask
from dotenv import load_dotenv
from preWeather import getWeatherfromAPI,predictionforAcc,loadModel,timesplit


load_dotenv()
app = Flask(__name__)

@app.route('/test')
def get_current_time():
    return {
        'time': time.time(),
        'data': "this is test ~"
        }

#get all accident data
@app.route('/apis/getAccidentData')
def getIncidentData():
    
    datamall_key = os.environ.get('DATAMALL_KEY')
    data_api = os.environ.get('GET_INCIDENT_API')

    HEADERS = {'AccountKey':datamall_key,}

    data = None
    try:
        response=requests.get(data_api, headers=HEADERS)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    else:
        data = response.json()
    return data

#get acccident data only
@app.route('/apis/incidentShow')
def incidentShow():
    
    data = getIncidentData()
    i = len(data["value"])-1
    while i>=0:
        if data["value"][i]["Type"] != 'Accident':
            del data["value"][i]
        i=i-1
    return data 

@app.route('/apis/roadWorkAdv')
def roadWorkAdv():
    data = getIncidentData()
    i = len(data["value"])-1
    while i>=0:
        if data["value"][i]["Type"] != 'Roadwork':
            del data["value"][i]
        i=i-1   
    leftlane=[]
    rightlane=[]
    for j in data["value"]:
        
        advice=j["Message"].split(". ")
        
        if len(advice)==2:     
            if advice[1] == "Avoid left lane.":
                leftlane.append(j)
            elif advice[1] == "Avoid right lane.":
                rightlane.append(j)         
    return  {"left":leftlane,"right":rightlane}

@app.route('/apis/prediction')
def prediction():
    accidentlist=incidentShow()["value"]
    resultList=[]
    for accident in accidentlist:
        modelSe, modelDur,modelDis=loadModel()
        weather=getWeatherfromAPI()
        result=predictionforAcc(modelSe, modelDur,modelDis,weather,accident) 
        resultList.append(result)
    return {"Result":resultList}

@app.route('/apis/timeCount')
def timeCountAcc():
    accidentlist=incidentShow()["value"]
    accHourDir={"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0,"10":0,"11":0,"12":0,"13":0,"14":0,"15":0,
             "16":0,"17":0,"18":0,"19":0,"20":0,"21":0,"22":0,"23":0}
    for accident in accidentlist:
        hour=str(timesplit(accident).strftime("%H"))
        for i in accHourDir.keys():
            if hour==i:
                accHourDir[hour]=accHourDir[hour]+1
    return accHourDir
          
@app.route('/apis/timeCount')
def timeCountinc():
    iccidentlist=getIncidentData()["value"]   
    incHourDir={"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0,"10":0,"11":0,"12":0,"13":0,"14":0,"15":0,
             "16":0,"17":0,"18":0,"19":0,"20":0,"21":0,"22":0,"23":0}
    for incident in iccidentlist:
        hour=str(timesplit(incident).strftime("%H"))
        for i in incHourDir.keys():
            if hour==i:
                incHourDir[hour]=incHourDir[hour]+1
    return incHourDir



if __name__ == '__main__':
    app.run(debug=True)