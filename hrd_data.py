import json
import requests
"""
ncsSearchUrl = 'https://www.hrd.go.kr/hrdc/gcod/searchNcsList.do'

a = {'upperNcsCd': '02', 'ncsCdLvl': 2}
b = {'ncsCdLvl': 1}

ncsCode = ['0' + str(i) if i <= 10 else str(i) for i in range(1, 25)]
# 대분류
with open("ncsCd.json", "w+", encoding='utf-8') as f:
    tmp = {}
    st_data = json.loads(requests.post(ncsSearchUrl, data=b).content)
    for st in st_data['ncsList']:
        print(st)
        tmp[f"{st['ncsCdNm']}"] = {}
        a['upperNcsCd'] = st['ncsCd']
        a['ncsCdLvl'] = 2

        # 중분류
        nd_data = json.loads(requests.post(ncsSearchUrl, data=a).content)
        for nd in nd_data['ncsList']:
            tmp[f"{st['ncsCdNm']}"][f"{nd['ncsCdNm']}"] = {'전체': '전체'}
            a['upperNcsCd'] = nd['ncsCd']
            a['ncsCdLvl'] = 3

            # 소분류
            rd_data = json.loads(requests.post(ncsSearchUrl, data=a).content)
            for rd in rd_data['ncsList']:
                tmp[f"{st['ncsCdNm']}"][f"{nd['ncsCdNm']}"][f"{rd['ncsCdNm']}"] = ['전체']
                a['upperNcsCd'] = rd['ncsCd']
                a['ncsCdLvl'] = 4

                th_data = json.loads(requests.post(ncsSearchUrl, data=a).content)
                for th in th_data['ncsList']:
                    tmp[f"{st['ncsCdNm']}"][f"{nd['ncsCdNm']}"][f"{rd['ncsCdNm']}"].append(th['ncsCdNm'])

    json.dump(tmp, f)
"""

ncs = object()

with open("ncsCd.json", encoding='utf-8') as f:
    ncs = json.load(f)

print(ncs['사업관리'])
print(list(ncs['사업관리']))

print(ncs['사업관리']['사업관리'])
print(list(ncs['사업관리']['사업관리']))

print(ncs['사업관리']['사업관리']['프로젝트관리'])