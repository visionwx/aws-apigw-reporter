    workspaceId: "364397913113100291"
    memberId: "409788576109166597"
    channelId: "364397913113165830"
    trickleId: "578759146069819400"




* trickle-app-lambda-live
* socket_service_live
* SEND_SOCKET_MESSAGE_LIVE
* trickle_async_handler_live
* baas-vc-async-handler-live
* baas-vc-app-handler-live


aws cloudwatch get-metric-statistics \
--namespace AWS/Lambda \
--metric-name Invocations \
--statistics Sum \
--start-time 2022-10-17T00:00:00 \
--end-time 2022-10-18T00:00:00 \
--period 3600 \
--dimensions Name=FunctionName,Value=trickle-app-lambda-live