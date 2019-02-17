import pandas
import requests
import json
import urllib
import numpy as np

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
        resultAsDict.append({"Constituency": constituency,"GssCode": gssCode, "Number of Signitures" : numOfSigs})

    
    df = pandas.DataFrame(data=resultAsDict, columns=["Constituency","GssCode","Number of Signitures"])
    return df

def getOralAndWrittenQuestions(requestAtATime = 500) :
    
    
    
    resultAsDict = []
    n = 0
    while True:
        querry = urllib.parse.urlencode({"_pageSize" : requestAtATime, "_page" : 0 })
        url = domain + "commonswrittenquestions.json?" + querry
        response = requests.get(url)
        dataAsDict = json.loads(response.content)
        for question in dataAsDict['result']['items'] :
            questionText = question['questionText']
            mpName = question['tablingMemberPrinted'][0]['_value']
            date = question['dateTabled']['_value']
            resultAsDict.append({"Question Text":questionText,"MP Name":mpName,"Date":date})
        if (n + 1) * requestAtATime > dataAsDict['result']['totalResults']:
            break
        n = n + 1

    pd = pandas.DataFrame(data=resultAsDict, columns=["Question Text","MP Name","Date"])
    return pd

print(getOralAndWrittenQuestions())


CtrlZ = getPetitionSignituresPerConstituency(1059153)
SuperContender = getPetitionSignituresPerConstituency(528705)
LeaveEU = getPetitionSignituresPerConstituency(990119)

pop = pandas.read_csv('C:\\Users\dvder\Desktop\ThePeopleVoted\pop.csv')
pop.rename(columns = {'Code':'GssCode'}, inplace = True)

CtrlZ2 = pandas.merge(CtrlZ, pop, on = 'GssCode')
SuperContender2 = pandas.merge(SuperContender, pop, on = 'GssCode')
LeaveEU2 = pandas.merge(LeaveEU, pop, on = 'GssCode')

CtrlZ2['Percy'] = np.divide(CtrlZ2['Number of Signitures'],CtrlZ2['Total electors 2017'])
CtrlZ2['Percy'] = CtrlZ2['Percy']*100
SuperContender2['Percy'] = np.divide(SuperContender2['Number of Signitures'],SuperContender2['Total electors 2017'])
SuperContender2['Percy'] = SuperContender2['Percy']*100
LeaveEU2['Percy'] = np.divide(LeaveEU2['Number of Signitures'],LeaveEU2['Total electors 2017'])
LeaveEU2['Percy'] = LeaveEU2['Percy']*100

BOI = requests.get("http://lda.data.parliament.uk/commonswrittenquestions.json?_view=Written+Questions&_pageSize=10000&_page=0&_exists-[brexit]=[true]")

#k = 3
#CtrlZ_Flipped = CtrlZ.sort_values(by = ['Number of Signitures'])





