import json
import re
import requests
import mytime
import binascii
import base64
import CatAndMouseGame

requests.packages.urllib3.disable_warnings()
session = requests.Session()

#===== Game's arguments =====
appVer = ''
dateVer = 0
verCode = ''
assetbundleFolder = ''
dataVer = 0
dataServerFolderCrc = ''
gameServerAddr = "https://game.fate-go.jp"
GithubToken = ''
GithubName = ''
UserAgent = 'Dalvik/2.1.0 (Linux; U; Android 11; Pixel 5 Build/RD1A.201105.003.A1)'


#==== User Info ====
def ReadConf():
    data = json.loads(
        requests.get(
            url=
            f"https://github.com/{GithubName}/FGODailyBonusLog/raw/main/cfg.json"
        ).text)
    global appVer, dateVer, assetbundleFolder, dataVer, dataServerFolderCrc
    appVer = data['global']['appVer']
    dataVer = data['global']['dataVer']
    dateVer = data['global']['dateVer']
    assetbundleFolder = data['global']['assetbundleFolder']
    dataServerFolderCrc = data['global']['dataServerFolderCrc']


def WriteConf(data):
    UploadFileToRepo('cfg.json', data, "update config")


def UpdateBundleFolder(assetbundle):
    new_assetbundle = CatAndMouseGame.MouseInfoMsgPack(
        base64.b64decode(assetbundle))
    print("new_assetbundle: %s" % new_assetbundle)
    global assetbundleFolder, dataServerFolderCrc
    assetbundleFolder = new_assetbundle
    dataServerFolderCrc = binascii.crc32(new_assetbundle.encode('utf8'))
    return 1


def UpdateAppVer(detail):
    matchObj = re.match('.*新ver.：(.*)、現.*', detail)
    if matchObj:
        global appVer
        appVer = matchObj.group(1)
        print("new version: %s" % appVer)
    else:
        print("No matches")
        raise Exception("update app ver failed")


#===== End =====

#===== Telegram arguments =====
TelegramBotToken = ''
TelegramAdminId = ''


def SendMessageToAdmin(message):
    if (TelegramBotToken != 'nullvalue'):
        nowtime = mytime.GetFormattedNowTime()
        url = "https://api.telegram.org/bot%s/sendMessage?chat_id=%s&parse_mode=markdown&text=_%s_\n%s" % (
            TelegramBotToken, TelegramAdminId, nowtime, message)
        result = json.loads(requests.get(url).text)
        if not result['ok']:
            print(result)
            print(message)
            raise 'something wrong'


#===== End =====


#===== Github api =====
def UploadFileToRepo(filename, content, commit="updated"):
    url = f"https://api.github.com/repos/{GithubName}/FGODailyBonusLog/contents/" + filename
    res = requests.get(url=url)
    jobject = json.loads(res.text)
    header = {
        "Content-Type": "application/json",
        "User-Agent": f"{GithubName}_bot",
        "Authorization": "token " + GithubToken
    }
    content = str(base64.b64encode(content.encode('utf-8')), 'utf-8')
    form = {
        "message": commit,
        "committer": {
            "name": f"{GithubName}_bot",
            "email": "none@none.none"
        },
        "content": content
    }
    if "sha" in jobject:
        form["sha"] = jobject["sha"]
    form = json.dumps(form)
    result = requests.put(url, data=form, headers=header)
    print(result.status_code)


#===== End =====

httpheader = {
    'Accept-Encoding': 'gzip, identity',
    'User-Agent': UserAgent,
    'Content-Type': 'application/x-www-form-urlencoded',
    'Connection': 'Keep-Alive, TE',
    'TE': 'identity'
}


def NewSession():
    return requests.Session()


def PostReq(session, url, data):
    res = session.post(url, data=data, headers=httpheader, verify=False).json()
    if res['response'][0]['resCode'] != '00':
        SendMessageToAdmin("[ErrorCode: %s]\n%s" %
                           (res['response'][0]['resCode'],
                            res['response'][0]['fail']['detail']))
    return res