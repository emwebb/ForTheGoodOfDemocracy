import pandas
import requests
import json
import urllib

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