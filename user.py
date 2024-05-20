# coding: utf-8
import uuid
import hashlib
import base64
from urllib.parse import quote_plus
import fgourl
import mytime
import rsa


class ParameterBuilder:
    def __init__(self, uid: str, auth_key: str, secret_key: str):
        self.uid_ = uid
        self.auth_key_ = auth_key
        self.secret_key_ = secret_key
        self.content_ = ''
        self.parameter_list_ = [
            ('appVer', fgourl.app_ver_),
            ('authKey', self.auth_key_),
            ('dataVer', str(fgourl.data_ver_)),
            ('dateVer', str(fgourl.date_ver_)),
            ('idempotencyKey', str(uuid.uuid4())),
            ('lastAccessTime', str(mytime.GetTimeStamp())),
            ('userId', self.uid_),
            ('verCode', fgourl.ver_code_),
        ]

    def AddParameter(self, key: str, value: str):
        self.parameter_list_.append((key, value))

    def Build(self) -> str:
        self.parameter_list_.sort(key=lambda tup: tup[0])
        temp = ''
        for first, second in self.parameter_list_:
            if temp:
                temp += '&'
                self.content_ += '&'
            escaped_key = quote_plus(first)
            if not second:
                temp += first + '='
                self.content_ += escaped_key + '='
            else:
                escaped_value = quote_plus(second)
                temp += first + '=' + second
                self.content_ += escaped_key + '=' + escaped_value

        temp += ':' + self.secret_key_
        self.content_ += '&authCode=' + quote_plus(base64.b64encode(hashlib.sha1(temp.encode('utf-8')).digest()))
        return self.content_

    def Clean(self):
        self.content_ = ''
        self.parameter_list_ = [
            ('appVer', fgourl.app_ver_),
            ('authKey', self.auth_key_),
            ('dataVer', str(fgourl.data_ver_)),
            ('dateVer', str(fgourl.date_ver_)),
            ('idempotencyKey', str(uuid.uuid4())),
            ('lastAccessTime', str(mytime.GetTimeStamp())),
            ('userId', self.uid_),
            ('verCode', fgourl.ver_code_),
        ]


class user:
    def __init__(self, user_id: str, auth_key: str, secret_key: str):
        self.name_ = ''
        self.user_id_ = (int)(user_id)
        self.s_ = fgourl.NewSession()
        self.builder_ = ParameterBuilder(user_id, auth_key, secret_key)

    def Post(self, url):
        res = fgourl.PostReq(self.s_, url, self.builder_.Build())
        self.builder_.Clean()
        return res

    def topLogin(self):
        idempotencyKey = self.builder_.parameter_list_[4][1]
        idempotencyKeySignature = rsa.sign(f'{self.user_id_}{idempotencyKey}')
        lastAccessTime = self.builder_.parameter_list_[5][1]
        userState = (-int(lastAccessTime) >> 2) ^ self.user_id_ & fgourl.data_server_folder_crc_

        self.builder_.AddParameter('idempotencyKeySignature', idempotencyKeySignature)
        self.builder_.AddParameter('assetbundleFolder', fgourl.asset_bundle_folder_)
        self.builder_.AddParameter('isTerminalLogin', '1')
        self.builder_.AddParameter('userState', str(userState))
        data = self.Post(f'{fgourl.server_addr_}/login/top?_userId={self.user_id_}')

        self.name_ = hashlib.md5(data['cache']['replaced']['userGame'][0]['name'].encode('utf-8')).hexdigest()
        stone = data['cache']['replaced']['userGame'][0]['stone']
        lv = data['cache']['replaced']['userGame'][0]['lv']
        ticket = 0

        # 呼符
        for item in data['cache']['replaced']['userItem']:
            if item['itemId'] == 4001:
                ticket = item['num']
                break

        # 登陆天数
        login_days = data['cache']['updated']['userLogin'][0]['seqLoginCount']
        total_days = data['cache']['updated']['userLogin'][0]['totalLoginCount']
        res = f'*{self.name_}*\n`登陆天数: {login_days}天 / {total_days}天\n'

        # 角色信息
        res += f'等级: {lv}\n石头: {stone}\n呼符: {ticket}\n'

        # 现有体力
        act_max = data['cache']['replaced']['userGame'][0]['actMax']
        act_recover_at = data['cache']['replaced']['userGame'][0]['actRecoverAt']
        now_act = (act_max - (act_recover_at - mytime.GetTimeStamp()) / 300)
        res += f'体力: {now_act} / {act_max}\n'

        # 友情点
        add_fp = data['response'][0]['success']['addFriendPoint']
        total_fp = data['cache']['replaced']['tblUserGame'][0]['friendPoint']
        res += f'友情点: {add_fp} / {total_fp}`\n'

        # 登陆奖励
        if 'seqLoginBonus' in data['response'][0]['success']:
            bonus_message = data['response'][0]['success']['seqLoginBonus'][0]['message']
            res += f'*{bonus_message}*\n`'

            for i in data['response'][0]['success']['seqLoginBonus'][0]['items']:
                res += f'{i["name"]} X {i["num"]}\n'

            if 'campaignbonus' in data['response'][0]['success']:
                bonus_name = data['response'][0]['success']['campaignbonus'][0]['name']
                bonus_detail = data['response'][0]['success']['campaignbonus'][0]['detail']
                res += f'`*{bonus_name}*\n*{bonus_detail}*\n`'

                for i in data['response'][0]['success']['campaignbonus'][0]['items']:
                    res += f'{i["name"]} X {i["num"]}\n'
            res += '`'

        server_now_time = mytime.TimeStampToString(data['cache']['serverTime'])
        res += f'_{server_now_time}_\n--------\n'
        print(res)
        return res

    def topHome(self):
        self.Post(f'{fgourl.server_addr_}/home/top?_userId={self.user_id_}')
