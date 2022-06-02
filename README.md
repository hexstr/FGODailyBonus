# FGODailyBonus
`Fate/Go`每日签到脚本，自`2020/06/23`以来稳定运行中。  
**但不排除有被封号的可能性，使用后果请自负。**

## 使用
0. 首先提取`账号`、`密码`和`id`，文件位于`/sdcard/Android/data/com.aniplex.fategrandorder/files/data/54cc790bf952ea710ed7e8be08049531`，用记事本打开，从`字母Z`复制到结尾
   ![0](imgs/0.jpg)
   
   然后搜索`C# Online Compiler`，比如[这个网站](https://www.onlinegdb.com/online_csharp_compiler)，把`CertificateExtractor.cs`中的内容复制粘贴到编辑框，修改第九行`YourCertificate`为你从`54cc790bf952ea710ed7e8be08049531`复制的内容，点击`Run`
   ![0-1](imgs/0-1.jpg)

   输出的结果对应`GAME_AUTHKEYS`、`GAME_SECRETKEYS`和`GAME_USERIDS`所需要的值

1. 创建一个名为`FGODailyBonusLog`的仓库，确保`branch`为`main`，点击`creating a new file`
    ![1](imgs/1.jpg)

2. 新建`cfg.json`并把[这里](https://raw.githubusercontent.com/hexstr/FGODailyBonusLog/main/cfg.json)的内容复制粘贴，并点击`Commit new file`
    ![2](imgs/2.jpg)

3. 点击[这个链接中](https://github.com/settings/tokens)的`Generate new token`，`Expiration`选择`No expiration`，并勾选`repo`，下滑点击`Generate token`创建一个`token`并记下来
    ![3](imgs/3.jpg)

    这里是新生成的`token`  
    ![3-1](imgs/3-1.jpg)

4. `fork`[这个repo](https://github.com/hexstr/FGODailyBonus)，点击`Settings`->`New repository secret`来创建`secrets`。脚本需要的`secrets`参考[secrets列表](#secrets列表)。
   ![4](imgs/4.jpg)

5. 点击`Actions`并启用
   ![5](imgs/5.jpg)

6. 最后，随意编辑一个文件
   ![6](imgs/6.jpg)

   （比如在`.gitignore`加一个空行）之后，点击`Commit changes`即可  
   ![6-1](imgs/6-1.jpg)

7. 再次点击`Actions`查看运行结果
   ![7](imgs/7.jpg)

   还有`telegram 通知`  
   ![7-1](imgs/7-1.jpg)

   和`日志文件`  
   ![7-2](imgs/7-2.jpg)

8. 默认签到时间为每日`UTC+0 19:30`，即东京时间`04:30`，如果需要修改，请自行搜索`cron 计算`并设置`.github/workflows/run.yml#L12`

9.  注意：每次提交`commit`都会触发`Action`

## secrets列表
| key                  | value                                                                 | description                                 |
|----------------------|-----------------------------------------------------------------------|---------------------------------------------|
| GAME_AUTHKEYS        | RaNdOmStRiNg1234:randomAAAAA=,RaNdOmStRiNg1235:randomAAAAA=           | 需要签到的账号，多个账号使用英文逗号","分隔 |
| GAME_SECRETKEYS      | RaNdOmStRiNg1234:randomAAAAA=,RaNdOmStRiNg1235:randomAAAAA=           | 对应的密码，多个账号使用英文逗号","分隔     |
| GAME_USERAGENT       | Dalvik/2.1.0 (Linux; U; Android 11; Pixel 5 Build/RD1A.201105.003.A1) | 伪装UA，填入nullvalue使用默认值             |
| GAME_USERIDS         | 60951234,60951235                                                     | 账号id                                      |
| GAME_VERCODE         | 48a1e86bdbb80b4795204d447cfc073ce21b132a5bd5b096cb919830b1d3b93e      | ←填这个就行                                 |
| TELEGRAM_ADMIN_ID    | nullvalue                                                             | 接收通知的telegram id，不需要就填nullvalue  |
| TELEGRAM_BOT_TOKEN   | nullvalue                                                             | 发送通知的bot token，不需要就填nullvalue    |
| VERY_IMPORTANT_NAME  | your_github_name                                                      | 填你的github name                           |
| VERY_IMPORTANT_TOKEN | ghp_uCwPxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx                              | 第三步申请的access token                    |
