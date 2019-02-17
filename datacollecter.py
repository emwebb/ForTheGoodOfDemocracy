import pandas
import requests
import json
import urllib
import numpy as np
import re


domain = "http://eldaddp.azurewebsites.net/"

def getPetitionSignituresPerConstituency(petition_id) :
    url = domain + "epetitions/" + str(petition_id) + ".json?_view=all&_properties=votingByConstituency.ePetition"
    response = requests.get(url)
    dataAsDict = json.loads(response.content)
    resultAsDict = []
    for constituencyUrl in dataAsDict["result"]["primaryTopic"]["votingByConstituency"]:
        url = constituencyUrl["_about"]
        url = str(url).replace("data.parliament.uk","eldaddp.azurewebsites.net")
        response = requests.get(url + ".json")
        numberOfSigsAsDict = json.loads(response.content)
        constituency = numberOfSigsAsDict["result"]["primaryTopic"]["constituency"]["label"]["_value"]
        numOfSigs = numberOfSigsAsDict["result"]["primaryTopic"]["numberOfSignatures"]
        gssCode = numberOfSigsAsDict["result"]["primaryTopic"]["gssCode"]
        mpUrl = domain + "/commonsmembers.json?constituency.label=" + constituency
        response = requests.get(mpUrl)
        constituencyAsDict = json.loads(response.content)

        mpName = constituencyAsDict["result"]["items"][0]["memberPrinted"]["_value"][:-3]
        resultAsDict.append({"Constituency": constituency,"GssCode": gssCode, "Number of Signitures" : numOfSigs, "MP Name" : mpName})

    
    df = pandas.DataFrame(data=resultAsDict, columns=["Constituency","GssCode","Number of Signitures","MP Name"])
    return df

def getOralAndWrittenQuestions(requestAtATime=10000):

    resultAsDict = []

    n = 0
    while True:
        querry = urllib.parse.urlencode({"_pageSize" : requestAtATime, "_page" : n })
        url = domain + "commonswrittenquestions.json?" + querry
        response = requests.get(url)
        dataAsDict = json.loads(response.content)
        for question in dataAsDict['result']['items'] :
            questionText = question['questionText']
            mpName = question['tablingMemberPrinted'][0]['_value']
            date = question['dateTabled']['_value']
            resultAsDict.append({"Question Text":questionText,"MP Name":mpName,"Date":date,"Oral":True})
        if (n + 1) * requestAtATime > dataAsDict['result']['totalResults']:
            break
        n = n + 1
    

    n = 0
    while True:
        querry = urllib.parse.urlencode({"_pageSize" : requestAtATime, "_page" : n })
        url = domain + "commonsoralquestions.json?" + querry
        response = requests.get(url)
        dataAsDict = json.loads(response.content)
        for question in dataAsDict['result']['items'] :
            questionText = question['questionText']
            mpName = question['tablingMemberPrinted'][0]['_value']
            date = question['dateTabled']['_value']
            constituency = question['tablingMember']['constituency']['prefLabel']['_value']
            resultAsDict.append({"Question Text":questionText,"MP Name":mpName,"Date":date,"Oral":True,"Constituency":constituency})
        if (n + 1) * requestAtATime > dataAsDict['result']['totalResults']:
            break
        n = n + 1

    pd = pandas.DataFrame(data=resultAsDict, columns=["Question Text","MP Name","Date","Oral","Constituency"])
    return pd

def getCachedOralAndWrittenQuestions():
    pd = pandas.read_csv('questions.csv')
    pd['Date'] = pd.to_datetime(pd['Date'])
    return pd

def getCachedConstituencyPopulation():
    pd = pandas.read_csv('constituencyPopulation.csv')
    return pd