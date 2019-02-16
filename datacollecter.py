import pandas
import requests
import json

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