import json
import requests
import random
import string
import uuid
from authgateway import *
import secrets
from pathlib import Path
import sys

def send_phone_code(phone_number):
    installid = ''.join(random.choices(
        string.ascii_uppercase + string.ascii_lowercase + string.digits, k=11))
    session = requests.Session()
    session.headers.update({"user-agent": "Tinder Android Version 13.21.0"})
    url = "https://api.gotinder.com"
    funnelid = str(uuid.uuid4())
    appsessionid = str(uuid.uuid4())
    deviceid = secrets.token_hex(8)
    authtoken = None
    refreshtoken = None
    userid = None
    email = None
    phonenumber = phone_number

    payload = {
        "device_id": installid,
        "experiments": ["default_login_token", "tinder_u_verification_method", "tinder_rules",
                        "user_interests_available"]
    }
    session.post(url + "/v2/buckets", json=payload)
    if refreshtoken is not None:
        print('[send_phone_code]: ', "Attempting to refresh auth token with saved refresh token")
        messageout = AuthGatewayRequest(
            refresh_auth=RefreshAuth(refresh_token=refreshtoken))
    else:
        messageout = AuthGatewayRequest(phone=Phone(phone=phonenumber))
    seconds = random.uniform(100, 250)
    headers = {
        'user-agent': "Tinder Android Version 12.6.0", 
        'os-version': "25",
        'app-version': "4023", 
        'platform': "android", 
        'platform-variant': "Google-Play", 
        'x-supported-image-formats': "webp",
        'accept-language': "en-US",
        'tinder-version': "12.6.0", 
        'store-Variant': 'Play-Store',
        'persistent-device-id': deviceid,
        'content-type': "application/x-protobuf",
        'host': 'api.gotinder.com',
        'connection': "close",
        'accept-encoding': "gzip,deflate, br",

        'install-id': installid,
        'app-session-id': appsessionid,
        'funnel-session-id': funnelid,
        'app-session-time-elapsed': format(seconds, ".3f")
    }
    if headers is not None:
        session.headers.update(headers)
    r = session.post(url + "/v3/auth/login", data=bytes(messageout))
    response = AuthGatewayResponse().parse(r.content).to_dict()
    print('[send_phone_code]: ', response)
       # print(response)
    # if(response.get("data")['sms_sent'] == 'false'):
    #     return False
    # else:
    #     return True
    return response

def get_token_through_phone(otp_code, phone_number):
    CODE_REQUEST_URL = "https://api.gotinder.com/v2/auth/sms/validate?auth_type=sms"
    HEADERS = {
        'User-Agent': 'Tinder/13.21.0 (iPhone; iOS 16.1.1; Scale/3.00)',
        'Content-Type': 'application/json',
    }
    
    data = {
        "otp_code": otp_code,
        "phone_number": phone_number
    }
    
    r = requests.post(CODE_REQUEST_URL, headers=HEADERS, data=json.dumps(data), verify=True)
    
    print('[get_token_through_phone]: base flow: ', r)

    response = r.json()
    print('[get_token_through_phone]: ', response)
    
    if(response.get("data")['validated'] == True):
        refresh_token = response.get("data")['refresh_token']
        
        CODE_REQUEST_URL = "https://api.gotinder.com/v2/auth/login/sms"
        HEADERS = {
            'User-Agent': 'Tinder/13.21.0 (iPhone; iOS 12.4.1; Scale/2.00)',
            'Content-Type': 'application/json',
        }
        
        data = {
            "client_version": "13.21.0",
            "refresh_token": refresh_token
        }
        
        r = requests.post(CODE_REQUEST_URL, headers=HEADERS, data=json.dumps(data), verify=True)
        
        print('[get_token_through_phone]: validated flow: ', r)

        response = r.json()
        print('[get_token_through_phone]: login auth refresh response: ', response)
            
        return response.get('data')['api_token']
    else:
        return False