import json,os
import argparse
from datetime import datetime,timedelta
from logging import raiseExceptions

# 86400
ONE_DAY_SECONDS = 24 * 60 * 60

def generateTimeList(period):
    if period > ONE_DAY_SECONDS:
        raise Exception("period greater than 86400")
    if period <= 0:
        raise Exception("period less than 0")
    
    if ONE_DAY_SECONDS % period != 0:
        raise Exception("period not divisible by 86400, " + str(ONE_DAY_SECONDS) + " % " + str(period))
    timeList = []
    dt0 = datetime(2022,10,10,0,0)
    timeList.append(dt0.strftime('%H:%M:%S'))

    timeLen = ONE_DAY_SECONDS / period
    for i in range(1,int(timeLen)):
        dt0 = dt0 + timedelta(seconds=period)
        timeList.append(dt0.strftime('%H:%M:%S'))
    return timeList
    

# 获取脚本参数
def parseArgs():
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--dataFolder", required=True, 
        type=str, default=None, help="local data folder")
    ap.add_argument("-t", "--title", required=True, 
        type=str, default=None, help="data title")
    ap.add_argument("-m", "--metricName", required=False, 
        type=str, default="Sum", help="metric name, by default Sum")
    ap.add_argument("-p", "--period", required=False, 
        type=int, default=900, help="statices period in seconds, by default 900s,15min")
    args = vars(ap.parse_args())
    return args

def checkData(data):
    if type(data) is not dict:
        raise Exception("DataFormatError,NotDict")
    if "Label" not in data.keys():
        raise Exception("DataFormatError,NoLabel")
    if "Datapoints" not in data.keys():
        raise Exception("DataFormatError,NoDatapoints")

# {
#     "Timestamp": "2022-10-17T08:00:00+00:00",
#     "Sum": 93.0,
#     "Unit": "Count"
# }
def convertDataPointsToDict(dataPoints, metricName):
    out = {}
    for perPoint in dataPoints:
        if "Timestamp" not in perPoint.keys() or metricName not in perPoint.keys():
            raise Exception("DataPoint format error")
        ts = perPoint["Timestamp"].split("T")[1].replace("+00:00","")
        value = int(perPoint[metricName])
        out[ts] = value
    return out

def transformDataByTimeList(label, dataPointsInDict, timeList):
    out = [label]
    for perTime in timeList:
        out.append(str(dataPointsInDict.get(perTime,0)))
    return out

def getJsonFileList(folder):
    outs = []
    for perFile in os.listdir(folder):
        if not perFile.endswith(".json"):
            continue
        outs.append(os.path.join(folder,perFile))
    return outs

def main():
    # Get para
    args = parseArgs()

    # genrate time list
    timeList = generateTimeList(args['period'])
    print(timeList)
    print(len(timeList))

    # get json files
    jsonFiles = getJsonFileList(args['dataFolder'])
    
    outs = []
    outs.append(["Lambda"] + timeList)
    for perJsonFile in jsonFiles:
        # get data label
        label = os.path.split(perJsonFile)[-1].replace(".json","")

        # load data
        data = json.load(open(perJsonFile,'r'))

        # check data
        checkData(data)

        # convert datapoint
        dataPoints = convertDataPointsToDict(data["Datapoints"], args["metricName"])
        print(dataPoints)

        # transform data
        dataConverted = transformDataByTimeList(label, dataPoints, timeList)

        outs.append(dataConverted)
    
    print(outs)
    json.dump({
        "title": args['title'],
        "source": outs
    }, open("outs.json","w"))

if __name__ == "__main__":
    main()