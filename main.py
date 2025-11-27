import tomllib
from pathlib import Path
from utils.getNews import getNews
from utils.xmlParser import parserHtml
from utils.translator import translate


def main():
    result = getNews()
    if result:
        if result == "None":
            print("没有新的消息")
            return
        title, content = result
        translate_title = translate(title, APP_KEY, APP_SECRET)
        if not translate_title:
            translate_title = title
        translate_content = parserHtml(content, APP_KEY, APP_SECRET)
        try:
            inner_title = f"{title}\n{translate_title}\n\n"
            QLAPI.notify("奥移民：" + translate_title, inner_title + translate_content)
        except NameError:
            noti_title = title + f"({translate_title})"
            print(noti_title)
            print(f"\n{translate_content}")


if __name__ == '__main__':
    try:
        APP_KEY = QLAPI.getEnvs({"searchValue": "youdao_APP_KEY"})["data"][0]["value"]
        APP_SECRET = QLAPI.getEnvs({"searchValue": "youdao_APP_SECRET"})["data"][0]["value"]
        print(APP_KEY, APP_SECRET)
    except NameError:
        BASEDIR = Path(__file__).parent
        CONFIG = tomllib.load(open(BASEDIR.joinpath("config.toml"), "rb"))
        APP_KEY = CONFIG['APP_KEY']
        APP_SECRET = CONFIG['APP_SECRET']
        print(APP_KEY, APP_SECRET)
    main()
