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
        mpName = numberOfSigsAsDict["result"]["primaryTopic"]["memberPrinted"]["_value"][:-3]
        resultAsDict.append({"Constituency": constituency,"GssCode": gssCode, "Number of Signitures" : numOfSigs, "MP Name" : mpName})

    
    df = pandas.DataFrame(data=resultAsDict, columns=["Constituency","GssCode","Number of Signitures"])
    return df

def getOralAndWrittenQuestions(requestAtATime,n,lim) :
    
    
    
    resultAsDict = []

    while n<lim:
        querry = urllib.parse.urlencode({"_pageSize" : requestAtATime, "_page" : n })
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


#k = 3
#CtrlZ_Flipped = CtrlZ.sort_values(by = ['Number of Signitures'])



n=0
#champs = getOralAndWrittenQuestions(500,0,50)

#champs = pandas.read_csv('C:\\Users\dvder\Desktop\ThePeopleVoted\questions.csv')
#champs2 = champs[(champs['Date']>datetime.date(2018,8,1))]

champs = pandas.read_csv('C:\\Users\dvder\Desktop\ThePeopleVoted\questionsclip.csv')

BrexitT = np.column_stack([champs['Question Text'].str.contains(r"\ Brexit", na=False) for col in champs])[:,1]
BrexitT = pandas.DataFrame(BrexitT)
brexitT = np.column_stack([champs['Question Text'].str.contains(r"\ brexit", na=False) for col in champs])[:,1]
brexitT = pandas.DataFrame(brexitT)
ref2 = np.column_stack([champs['Question Text'].str.contains(r"\ second referendum", na=False) for col in champs])[:,1]
ref2 = pandas.DataFrame(ref2)
A50 = np.column_stack([champs['Question Text'].str.contains(r"\ Article 50", na=False) for col in champs])[:,1]
A50 = pandas.DataFrame(A50)
leavingEU = np.column_stack([champs['Question Text'].str.contains(r"\ leaving the EU", na=False) for col in champs])[:,1]
leavingEU = pandas.DataFrame(leavingEU)
leavingEu = np.column_stack([champs['Question Text'].str.contains(r"\ leaving the Eu", na=False) for col in champs])[:,1]
leavingEu = pandas.DataFrame(leavingEu)
withdrawal = np.column_stack([champs['Question Text'].str.contains(r"\ withdrawal agreement", na=False) for col in champs])[:,1]
withdrawal = pandas.DataFrame(withdrawal)
leavesEU = np.column_stack([champs['Question Text'].str.contains(r"\ leaves the EU", na=False) for col in champs])[:,1]
leavesEU = pandas.DataFrame(leavesEU)
nodeal = np.column_stack([champs['Question Text'].str.contains(r"\ no deal", na=False) for col in champs])[:,1]
nodeal = pandas.DataFrame(nodeal)
left = np.column_stack([champs['Question Text'].str.contains(r"\ left the Eu", na=False) for col in champs])[:,1]
left = pandas.DataFrame(left)
negotiations = np.column_stack([champs['Question Text'].str.contains(r"\ negotiations with the EU", na=False) for col in champs])[:,1]
negotiations = pandas.DataFrame(negotiations)

Matchyboi = np.column_stack([champs['Question Text'].str.contains('brexit|second referendum|negotiations with the EU|left the Eu|no deal|leaves the EU|withdrawal agreement|leaving the Eu|Article 50', na=False, regex=True, flags=re.IGNORECASE) for col in champs])[:,1]
Matchyboi = pandas.DataFrame(Matchyboi)

champs2 = champs.assign(Word = Matchyboi)




Matchyboi[0].value_counts()
1786/(1786+22950)


    

helpme = champs.loc[nodeal]
champs.to_csv('C:\\Users\dvder\Desktop\ThePeopleVoted\Champs.csv',index=False)
