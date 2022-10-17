import json

dataFile = "rps_result.json"
dateFieldName = "bin(15m)"
countFieldName = "count()"

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
    return [dateVal,countVal]

def convertData(data):
    out = []
    datas = data.get("results",[])
    for perData in datas[::-1]:
        try:
            perData2 = getFiledValue(perData)
            out.append(perData2)
        except:
            pass
    return out

def main():
    data = loadQueryData()
    if not isComplete(data):
        raise Exception("query failed")
    outs = convertData(data)
    json.dump(outs,open('rps.html.json','w'))
    print(outs)

main()