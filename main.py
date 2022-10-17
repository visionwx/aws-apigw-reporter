import json
import os

# {
#     "queryId": "21e2ef83-ab5f-4fb0-8eda-5f557ad55849"
# }

queryCmd = """
aws logs start-query \
 --log-group-name API_GW_LIVE_V1 \
 --start-time `date -v-1d "+%s"` \
 --end-time `date "+%s"` \
 --query-string 'fields @timestamp, @message | stats count() by bin(15m)'
"""

res = os.popen(queryCmd)

print(res)
print(type(res))
print(json.loads(res))
print(res.get("queryId"))