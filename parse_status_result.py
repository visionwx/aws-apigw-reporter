import json

dataFile = "status_result.json"
dateFieldName = "status"
countFieldName = "statusCount"

class QueryResult:
    complete = "Complete"

def loadQueryData():
    return json.load(open(dataFile))

def isComplete(data):
    return data.get("status","Failed") == QueryResult.complete

def getFiledValue(data):
    dateVal = None
    countVal = None
    for perField in data:
        nam = perField.get("field","")
        val = perField.get("value",None)
        if nam == dateFieldName:
            dateVal = val
        elif nam == countFieldName:
            countVal = val
    if dateVal is None or countVal is None:
        raise Exception("NotFound")
    return {
        "name": dateVal,
        "value": countVal
    }

def convertData(data):
    out = {
        "data": [],
        "totalMatch": ""
    }
    totalMatch = data.get("statistics",{}).get("recordsMatched",0)
    out["totalMatch"] = totalMatch
    datas = data.get("results",[])
    perData2 = None
    for perData in datas[::-1]:
        try:
            perData2 = getFiledValue(perData)
            out["data"].append(perData2)
        except:
            pass
    return out

def main():
    data = loadQueryData()
    if not isComplete(data):
        raise Exception("query failed")
    outs = convertData(data)
    json.dump(outs,open('status.html.json','w'))
    print(outs)

main()