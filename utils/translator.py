import tomllib
import requests
from pathlib import Path
from utils.AuthV3Util import addAuthParams

BASEDIR = Path(__file__).parent.parent
CONFIG = tomllib.load(open(BASEDIR.joinpath("config.toml"), "rb"))
APP_KEY = CONFIG['APP_KEY']
APP_SECRET = CONFIG['APP_SECRET']


def translate(text: str):
    """
    note: 将下列变量替换为需要请求的参数
    """
    q = text
    lang_from = 'auto'
    lang_to = 'zh-CHS'

    data = {'q': q, 'from': lang_from, 'to': lang_to}

    addAuthParams(APP_KEY, APP_SECRET, data)

    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        res = doCall('https://openapi.youdao.com/api', header, data, 'post')
        return res.json()["translation"][0]
    except Exception as e:
        print(repr(e))
        return None

def doCall(url, header, params, method):
    if 'get' == method:
        return requests.get(url, params)
    elif 'post' == method:
        return requests.post(url, params, header)
    else:
        return None


if __name__ == '__main__':
    result = translate("Systems maintenance 28 November – 29 November 2025")
    print(result)

