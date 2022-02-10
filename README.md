# FGODailyBonus
`Fate/Go` daily check-in script, stable since `2020/06/23`.  
**But do not exclude the possibility of being blocked, use at your own risk. **

## Use
0. First extract the `account`, `password` and `id`, the files are located in `/sdcard/Android/data/com.aniplex.fategrandorder/files/data/54cc790bf952ea710ed7e8be08049531`, open them with notepad and start with the `letter Z` and copy it to the end
      ![0](imgs/0.jpg)
   
      Then search for `C# Online Compiler`, e.g. [this site](https://www.onlinegdb.com/online_csharp_compiler), copy and paste the contents of `CertificateExtractor.cs` into the edit box and change the ninth line ` YourCertificate` to the content you copied from `54cc790bf952ea710ed7e8be08049531`, click `Run`
      ![0-1](imgs/0-1.jpg) 

      The output corresponds to the values needed for `GAME_AUTHKEYS`, `GAME_SECRETKEYS` and `GAME_USERIDS`

1. Create a repository called `FGODailyBonusLog`, make sure `branch` is `main` and click `creating a new file`
        ![1](imgs/1.jpg)

2. Create a new `cfg.json` and copy and paste the contents of [here](https://raw.githubusercontent.com/nishuoshenme/FGODailyBonusLog/main/cfg.json) and click on `Commit new file`
        ![2](imgs/2.jpg)

3. Click on `Generate new token` in [this link](https://github.com/settings/tokens), select `No expiration` for `Expiration` and tick `repo`, slide down and click on `Generate token` to create a ` token` and write it down
        ![3](imgs/3.jpg)

        Here is the newly generated `token`  
        ![3-1](imgs/3-1.jpg)

4. `fork` [this repo](https://github.com/nishuoshenme/FGODailyBonus) and click `Settings`->`New repository secret` to create `secrets`. Refer to [secrets list](#secrets list) for the `secrets` needed for the script.
      ![4](imgs/4.jpg)

5. Click on `Actions` and enable
      ![5](imgs/5.jpg)

6. Finally, edit a file at random
      ![6](imgs/6.jpg)

      (e.g. add a blank line to `.gitignore`) and then click `Commit changes`  
      ![6-1](imgs/6-1.jpg)

7. Click on `Actions` again to see the results
      ![7](imgs/7.jpg)

      And `telegram notifications`  
      ![7-1](imgs/7-1.jpg)

      and `log files`  
      ![7-2](imgs/7-2.jpg)

8. The default check-in time is daily `UTC+0 19:30`, i.e. Tokyo time `04:30`, if you need to change it, please search for `cron calculations` and set `.github/workflows/run.yml#L12` yourself

9. Note: each commit `commit` will trigger `Action`

## secrets列表
| key                  | value                                                                 | description                                 |
|----------------------|-----------------------------------------------------------------------|---------------------------------------------|
| GAME_AUTHKEYS        | RaNdOmStRiNg1234:randomAAAAA=,RaNdOmStRiNg1235:randomAAAAA=           | 需要签到的账号，多个账号使用英文逗号","分隔 |
| GAME_SECRETKEYS      | RaNdOmStRiNg1234:randomAAAAA=,RaNdOmStRiNg1235:randomAAAAA=           | 对应的密码，多个账号使用英文逗号","分隔     |
| GAME_USERAGENT       | Dalvik/2.1.0 (Linux; U; Android 11; Pixel 5 Build/RD1A.201105.003.A1) | 伪装UA，填入nullvalue使用默认值             |
| GAME_USERIDS         | 60951234,60951235                                                     | 账号id                                      |
| GAME_VERCODE         | 723d93a599b6f10ef3085ff1131fa5679a91da924246b8ca40dded18eccaf3da      | ←填这个就行                                 |
| TELEGRAM_ADMIN_ID    | nullvalue                                                             | 接收通知的telegram id，不需要就填nullvalue  |
| TELEGRAM_BOT_TOKEN   | nullvalue                                                             | 发送通知的bot token，不需要就填nullvalue    |
| VERY_IMPORTANT_NAME  | your_github_name                                                      | 填你的github name                           |
| VERY_IMPORTANT_TOKEN | ghp_uCwPxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx                              | 第三步申请的access token                    |
