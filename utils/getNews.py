import json
import requests
from datetime import datetime
from hashlib import md5
from pathlib import Path


BASEDIR = Path(__file__).parent.parent

def md5_text(text):
  return md5(text.encode('utf-8')).hexdigest()

def getNews():
  now_year = datetime.today().date().year
  url = "https://immi.homeaffairs.gov.au/_layouts/15/api/Data.aspx/GetNews"

  payload = {
    "siteUrl": "https://www.homeaffairs.gov.au",
    "webUrl": "/News-subsite",
    "filter": {
      "Categories": [],
      "PageNumber": 1,
      "RowLimit": 20,
      "ShowCurrentSiteOnly": False,
      "CurrentSite": "Immi",
      "Year": f"{now_year}"
    }
  }

  headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    'Accept': "application/json;odata=verbose",
    'Accept-Encoding': "gzip, deflate, br, zstd",
    'Content-Type': "application/json",
    'pragma': "no-cache",
    'cache-control': "no-cache",
    'sec-ch-ua-platform': "\"Windows\"",
    'sec-ch-ua': "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
    'sec-ch-ua-mobile': "?0",
    'x-requested-with': "XMLHttpRequest",
    'content-type': "application/json;odata=verbose",
    'origin': "https://immi.homeaffairs.gov.au",
    'sec-fetch-site': "same-origin",
    'sec-fetch-mode': "cors",
    'sec-fetch-dest': "empty",
    'referer': "https://immi.homeaffairs.gov.au/news-media",
    'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
    'priority': "u=1, i"
  }
  try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    news_data = response.json()["d"]["data"]
    latest_new = news_data[0]
    hashText = latest_new["Date"] + latest_new["Title"] + latest_new["Url"]
    hashId = md5_text(hashText)
    hashIdPath = BASEDIR.joinpath("homeaffairs_latest_new_id")
    if hashIdPath.exists():
      with open(hashIdPath, "r", encoding="utf-8") as f:
        oldHashId = f.read()
      if oldHashId != hashId:
          with open(hashIdPath, "w", encoding="utf-8") as f:
              f.write(hashId)
          title = latest_new["Title"]
          content = latest_new["Content"]
          return title, content
      # 没有新的消息
      else:
        return "None"
    else:
      with open(hashIdPath, "w", encoding="utf-8") as f:
        f.write(hashId)
      title = latest_new["Title"]
      content = latest_new["Content"]
      return title, content
  except Exception as e:
    print(repr(e))
    return None


if __name__ == '__main__':
  print(getNews())
