# coding: utf-8. 
import time
import json
import hashlib
import base64
import urllib.parse
import fgourl as url
import mytime


class user:
    def __init__(self, userId, authKey, secretKey):
        self.name = ''
        self.userId = (int)(userId)
        self.authKey = authKey
        self.secretKey = secretKey
        self.session = url.NewSession()

    def getAuthCode(self, par):
        par = {k: par[k] for k in sorted(par)}
        par = urllib.parse.urlencode(par, safe='+=:/ ')
        text = par + ':' + self.secretKey
        dig = hashlib.sha1(text.encode('utf-8')).digest()
        return base64.b64encode(dig)

    def userLogin(self):
        self.gameData()
        time.sleep(6)
        self.topLogin()
        time.sleep(3)
        self.topHome()

    def topLogin(self):
        lastAccessTime = mytime.GetTimeStamp()
        userState = (
            -lastAccessTime >> 2) ^ self.userId & url.dataServerFolderCrc
        par = {
            'userId': self.userId,
            'authKey': self.authKey,
            'appVer': url.appVer,
            'dateVer': url.dateVer,
            'lastAccessTime': lastAccessTime,
            'verCode': url.verCode,
            'userState': userState,
            'assetbundleFolder': url.assetbundleFolder,
            'dataVer': url.dataVer,
            'isTerminalLogin': '1'
        }
        par['authCode'] = self.getAuthCode(par)
        req = urllib.parse.urlencode(par)

        data = url.PostReq(
            self.session,
            "%s/login/top?_userId=%s" % (url.gameServerAddr, self.userId), req)
        self.message = data['cache']['replaced']['userGame'][0]['message']
        self.name = hashlib.md5(data['cache']['replaced']['userGame'][0]
                                ['name'].encode('utf-8')).hexdigest()
        self.stone = data['cache']['replaced']['userGame'][0]['stone']
        self.lv = data['cache']['replaced']['userGame'][0]['lv']
        self.exp = data['cache']['replaced']['userGame'][0]['exp']
        self.ticket = 0

        # 呼符
        for item in data['cache']['replaced']['userItem']:
            if (item['itemId'] == 4001):
                self.ticket = item['num']
                break

        # 登陆天数
        res = "[%s]\n`登陆天数: %s天 / %s天\n" % (
            self.name,
            data['cache']['updated']['userLogin'][0]['seqLoginCount'],
            data['cache']['updated']['userLogin'][0]['totalLoginCount'])

        # 角色信息
        res += "等级: %s\n石头: %s\n呼符: %s\n" % (self.lv, self.stone, self.ticket)

        # 现有体力
        #actMax = data['cache']['replaced']['userGame'][0]['actMax']
        #actRecoverAt = data['cache']['replaced']['userGame'][0]['actRecoverAt']
        #res += "现存体力: %s\n" % (actMax - (actRecoverAt - mytime.GetTimeStamp()) / 300)

        # 友情点
        res += "友情点: %s / %s`\n" % (
            data['response'][0]['success']['addFriendPoint'],
            data['cache']['replaced']['tblUserGame'][0]['friendPoint'])

        # 登陆奖励
        if 'seqLoginBonus' in data['response'][0]['success']:
            res += '*%s*\n`' % data['response'][0]['success']['seqLoginBonus'][
                0]['message']
            for i in data['response'][0]['success']['seqLoginBonus'][0][
                    'items']:
                res += "%s X %s\n" % (i['name'], i['num'])
            if 'campaignbonus' in data['response'][0]['success']:
                res += '`*%s*\n*%s*\n`' % (
                    data['response'][0]['success']['campaignbonus'][0]['name'],
                    data['response'][0]['success']['campaignbonus'][0]
                    ['detail'])
                for i in data['response'][0]['success']['campaignbonus'][0][
                        'items']:
                    res += "%s X %s\n" % (i['name'], i['num'])
            res += '`'
        return res + '_%s_\n--------\n' % mytime.TimeStampToString(
            data['cache']['serverTime'])

    def topHome(self):
        par = {
            'userId': self.userId,
            'authKey': self.authKey,
            'appVer': url.appVer,
            'dateVer': url.dateVer,
            'lastAccessTime': mytime.GetTimeStamp(),
            'verCode': url.verCode,
            'dataVer': url.dataVer
        }
        par['authCode'] = self.getAuthCode(par)
        req = urllib.parse.urlencode(par)
        url.PostReq(
            self.session,
            "%s/home/top?_userId=%s" % (url.gameServerAddr, self.userId), req)

    def gameData(self):
        par = {
            'userId': self.userId,
            'authKey': self.authKey,
            'appVer': url.appVer,
            'dateVer': url.dateVer,
            'lastAccessTime': mytime.GetTimeStamp(),
            'verCode': url.verCode,
            'dataVer': url.dataVer
        }
        par['authCode'] = self.getAuthCode(par)
        req = urllib.parse.urlencode(par)
        data = url.PostReq(
            self.session,
            "%s/gamedata/top?_userId=%s" % (url.gameServerAddr, self.userId),
            req)
        if 'action' in data['response'][0]['fail'] and data['response'][0][
                'fail']['action'] == "app_version_up":
            url.UpdateAppVer(data['response'][0]['fail']['detail'].replace(
                "\r\n", ""))
            self.gameData()
            return
        if data['response'][0]['success']['dateVer'] != url.dateVer or data[
                'response'][0]['success']['dataVer'] != url.dataVer:
            s = "*Need Update*\n"
            s += "appVer: %s\n" % (url.appVer)
            s += "dateVer: %s Server: %s\n" % (
                url.dateVer, data['response'][0]['success']['dateVer'])
            s += "dataVer: %s Server: %s" % (
                url.dataVer, data['response'][0]['success']['dataVer'])
            url.SendMessageToAdmin(s)
            val = url.UpdateBundleFolder(
                data['response'][0]['success']['assetbundle'])
            if val == 1:
                url.dataVer = data['response'][0]['success']['dataVer']
                url.dateVer = data['response'][0]['success']['dateVer']
                dict = {}
                dict['global'] = {
                    "appVer": url.appVer,
                    "assetbundleFolder": url.assetbundleFolder,
                    "dataServerFolderCrc": url.dataServerFolderCrc,
                    "dataVer": url.dataVer,
                    "dateVer": url.dateVer
                }
                url.WriteConf(json.dumps(dict))
            else:
                url.SendMessageToAdmin('update failed')
