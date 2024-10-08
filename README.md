[TestCase Link](https://docs.google.com/spreadsheets/d/1I97oWxnWm3V7b3F1M-oc-SntYrbt_PvVeWe7kIEaNDU/edit?pli=1&gid=0#gid=0)

[사용 라이브러리]
1. selenium
2. webdriver-manager
3. google-api-python-client google-auth-httplib2 google-auth-oauthlib

<br>

[트러블 슈팅] <br>
스크립트 실행 시 THIRD_PARTY_NOTICES.chromedriver 로 실행된다면, 사용되는 chromedriver 경로에서 THIRD_PARTY_NOTICES.chromedriver 파일 삭제 후 재 실행 <br>
ex) C:\Users\user\.wdm\drivers\chromedriver\win64\129.0.6668.89\chromedriver-win32 경로의 THIRD_PARTY_NOTICES.chromedriver
