# SocialConnection_web
#### 本專案利用Python 的框架 [Django](https://www.djangoproject.com/) 進行設計並透過[Pyrebase](https://github.com/thisbejim/Pyrebase)連結[Firebase](https://firebase.google.com/?hl=zh-tw)。
#
我在Windows在安裝Pyrebase時，有發生安裝失敗的問題，然後我照[這篇文章底下的留言](https://github.com/thisbejim/Pyrebase/issues/288)，成功解決問題。
```python
# app/ppyrebase_settings.py
# config 改成你從Firebase得到的以下資料

config = {
    "apiKey": "your apiKey",
    "authDomain": "your authDomain",
    "databaseURL": "your databaseURL",
    "projectId": "your projectId",
    "storageBucket": "your storageBucket",
    "messagingSenderId": "your messagingSenderId",
    "appId": "your appId"
  };
```
#
```python
# app/views..py
#在上傳檔案時，由於作業系統的關係，檔案路徑需要自行調整
# windows 作業系統 
                uploaded_file_url = settings.BASE_DIR + uploaded_file_url.replace("/", "\\")
# 非 windows 作業系統 
                uploaded_file_url = settings.BASE_DIR + uploaded_file_url
```
#
我將[本專案](https://socialconnection-web.herokuapp.com/)佈署在[Heroku](https://www.heroku.com/)。
#
#
## [展示影片](https://youtu.be/vtAoAvWAe78)
