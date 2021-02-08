import requests
import json
import os
import re

from bs4 import BeautifulSoup as bs

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

    elif not chkAuthKey(s):
        return -1

    else:
        return 1


def chkAuthKey(s):
    ak = os.path.join(BASE_DIR, "authKey.key")
    if not os.path.isfile(ak):
        res = bs(s.get('https://www.hrd.go.kr/hrdp/ps/ppsho/PPSHO0100L.do').content, "html.parser")

        try:
            key = re.sub('\\s', '', res.select('table.view > tbody > tr > td')[-1].text)
            with open(ak, "w+") as f:
                f.write(key)
        except IndexError:
            return False

    return True
