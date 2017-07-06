"""
* Nagios Alert Message SMS to Dingtalk
* 
* @author David
* Version 1.0 , 2017-06-23
"""
# !/usr/bin/env python3
import re
import time , datetime
import requests
import json

# nagios admin's phone number
nagios_admin_num = "09" # David

# read sms_service log file
f = open('D:\david_hsu\Desktop\message.txt','r')
line = f.read()

# find alert message and phone number
msg = re.findall('Src = \[KBT]\w+.+\n SMS Phone Number = \d{10}',line)

# split src
alert_msg = list()
for i in msg:
    alert_msg.append(i.replace('Src = ', ''))


# definite function for transfer date to second
def get_sec(time_str):
    struct_time = time.strptime(time_str , "%Y/%m/%d %H:%M")
    sec = time.mktime(struct_time)
    return sec

# get now time
nowtime = time.strftime("%Y/%m/%d %H:%M")
now_time = get_sec(nowtime)

# get access token from dingtalk
headers = {'Content-Type': 'application/json'}
r = requests.get('https://oapi.dingtalk.com/gettoken?corpid=',headers=headers)
accessToken = json.loads(r.text)['access_token']

# send alert message during 60s and write log
for i in alert_msg:
    if i[-10:] == nagios_admin_num:
        log_time = get_sec((time.strftime("%Y/"))+i[-42:-31])
        if now_time - log_time <= 60:
            payload={
               "chatid":"chat0", # chatid is Linux Alert Group in Dingtalk
               "msgtype": "text",
               "text": {
                   "content": i[:-42]
                   }
               }
            r = requests.post('https://oapi.dingtalk.com/chat/send?access_token={0}'.format(accessToken),data=json.dumps(payload),headers=headers) 
            # write message log
            f = open('D:\david_hsu\Desktop\send_log.txt','a')
            f.write("===================Log Start===================\n")
            f.write("Time = "+time.strftime("%Y/%m/%d %H:%M:%S")+'\n')
            f.write("Payload = "+json.dumps(payload)+'\n')
            f.write("Response = "+r.text+'\n')
            f.write("Access Token = "+accessToken+'\n')
            f.write("Src = "+i+'\n')
            f.write("====================Log End====================\n")
            f.close()


        
    

