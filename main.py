import os
import time
import mytime
import fgourl as url
from user import user

userIds = os.environ['userIds'].split(",")
authKeys = os.environ['authKeys'].split(",")
secretKeys = os.environ['secretKeys'].split(",")

userNums = len(userIds)
authKeyNums = len(authKeys)
secretKeyNums = len(secretKeys)

url.verCode = os.environ['verCode']
url.TelegramBotToken = os.environ['TGBotToken']
url.TelegramAdminId = os.environ['TGAdminId']
url.GithubToken = os.environ['GithubToken']
url.GithubName = os.environ['GithubName']
UA = os.environ['UserAgent']
if UA != 'nullvalue':
    url.UserAgent = UA


def main():
    url.SendMessageToAdmin("铛铛铛( \`д´) *%s点* 了" % mytime.GetNowTimeHour())
    if userNums == authKeyNums and userNums == secretKeyNums:
        url.ReadConf()
        print("待签到: %d 个" % userNums)
        res = '【登录信息】\n'
        for i in range(userNums):
            instance = user(userIds[i], authKeys[i], secretKeys[i])
            instance.gameData()
            time.sleep(5)
            res += instance.topLogin()
            time.sleep(2)
            instance.topHome()
        url.SendMessageToAdmin(res)
        url.UploadFileToRepo(mytime.GetNowTimeFileName(), res,
                             mytime.GetNowTimeFileName())
    else:
        print("账号密码数量不匹配")


if __name__ == '__main__':
    main()

