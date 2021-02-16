import requests
import json
import os
import re

RE_COMP = re.compile('[b\\/:*?"<>|\\t]')
EXCEL_BASE_URL = "http://www.hrd.go.kr/hrdp/ps/ppsmo/excelDownAll0109P.do?"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DL_DIR = os.path.join(BASE_DIR, "result")


def chkLogin(ID, PW):
    s = requests.Session()
    s.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
    }
    res = s.get(
        'https://www.hrd.go.kr/hrdp/mb/pmbao/login.do?'
        f'userloginId={ID}&'
        f'userloginPwd={PW}&'
        'loginType=personal&'
        'mberSe=C0178'
    )

    res = json.loads(res.text)
    if res['message'] == 'checkLoginId' or res['message'] == 'FAIL':
        return 0

    return s
