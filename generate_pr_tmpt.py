import argparse
import json

TMPT = [
  {
    "type": "gallery",
    "value": [
      "https://resource.trickle.so/upload/images/e93c1fc3-e389-4bf7-9f5e-513484fda312.png"
    ]
  },
  {
    "type": "h3",
    "value": "Trickle test env has been update"
  },
  {
    "type": "text",
    "value": "Update workflow"
  },
  {
    "type": "text",
    "value": "- featue 1,ajiwoefjowqeqwe\n- feature 2,ajoiefjoweiofwqe\n- feature 3,aejioweofiqwoe"
  }
]

def parseArgs():
    # 获取脚本参数
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--title", required=True, 
        type=str, default=None, help="pr title")
    ap.add_argument("-b", "--body", required=True, 
        type=str, default=None, help="pr body")
    args = vars(ap.parse_args())
    return args

def main():
    # 获取脚本参数
    args = parseArgs()

    # r = json.load(open(args['jsonFile'],'r'))
    TMPT[2]["value"] = args['title']
    TMPT[3]["value"] = args['body']

    print(json.dumps(TMPT))


if __name__ == "__main__":
    main()