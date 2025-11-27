from utils.getNews import getNews
from utils.xmlParser import parserHtml
from utils.translator import translate

def main():
    result = getNews()
    if result:
        title, content = result
        translate_title = translate(title)
        if not translate_title:
            translate_title = title
        translate_content = parserHtml(content)
        print(translate_title)


if __name__ == '__main__':
    main()
