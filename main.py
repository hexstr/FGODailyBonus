import os
import traceback
import time
import mytime
import fgourl
from user import user

userIds = os.environ['userIds'].split(',')
authKeys = os.environ['authKeys'].split(',')
secretKeys = os.environ['secretKeys'].split(',')

userNums = len(userIds)
authKeyNums = len(authKeys)
secretKeyNums = len(secretKeys)

fgourl.ver_code_ = os.environ['verCode']
fgourl.TelegramBotToken = os.environ['TGBotToken']
fgourl.TelegramAdminId = os.environ['TGAdminId']
fgourl.github_token_ = os.environ['GithubToken']
fgourl.github_name_ = os.environ['GithubName']
UA = os.environ['UserAgent']
if UA != 'nullvalue':
    fgourl.user_agent_ = UA


def main():
    fgourl.SendMessageToAdmin(f'铛铛铛( \`д´) *{mytime.GetNowTimeHour()}点* 了')
    if userNums == authKeyNums and userNums == secretKeyNums:
        fgourl.ReadConf()
        fgourl.gameData()
        print(f'待签到: {userNums}个')
        res = '【登录信息】\n'
        for i in range(userNums):
            try:
                instance = user(userIds[i], authKeys[i], secretKeys[i])
                time.sleep(3)
                res += instance.topLogin()
                time.sleep(2)
                instance.topHome()
                time.sleep(2)
            except Exception as ex:
                print(f'{i}th user login failed: {ex}')
                traceback.print_exc()

        fgourl.UploadFileToRepo(mytime.GetNowTimeFileName(), res, mytime.GetNowTimeFileName())
        fgourl.SendMessageToAdmin(res)
    else:
        print('账号密码数量不匹配')


if __name__ == '__main__':
    main()
