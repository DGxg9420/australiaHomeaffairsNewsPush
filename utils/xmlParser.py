import html
from utils.translator import translate
from bs4 import BeautifulSoup, NavigableString


def parserHtml(content_html: str, APP_KEY: str, APP_SECRET: str)  -> str:
    try:
        # 解析
        soup = BeautifulSoup(content_html, 'html.parser')

        # 要跳过的标签（通常不包含用户可见内容）
        skip_tags = {'script', 'style', 'meta', 'link', 'title', 'head', 'noscript', "ul"}

        # 找出所有可能包含用户可见文本的标签
        candidate_tags = []
        for tag in soup.find_all(True):  # True 表示所有标签
            if tag.name in skip_tags:
                continue
            # 获取纯文本并清理
            text = tag.get_text(strip=True)
            if text:  # 非空文本
                candidate_tags.append(tag)

        # 注意：为了避免重复处理（比如 <li> 在 <ul> 内，而 <ul> 也有文本），我们按深度排序：先处理深层（子）标签
        # 这样可以优先翻译 <li> 而不是整个 <ul>
        candidate_tags.sort(key=lambda t: len(list(t.parents)), reverse=True)

        # 记录已处理的标签，防止重复（比如同一个标签被多次加入）
        processed = set()

        for tag in candidate_tags:
            if tag in processed:
                continue

            # 提取完整文本（保留空格和换行，但解码实体）
            clean_text = ''.join(str(child) for child in tag.contents if isinstance(child, NavigableString))
            if not clean_text:
                continue
            # 翻译
            translated_text = translate(clean_text, APP_KEY, APP_SECRET)
            if not translated_text:
                translated_text = clean_text

            # 创建新标签（同名，纯文本内容）
            new_tag = soup.new_tag(tag.name, string=translated_text)

            # 插入到原标签之后
            tag.insert_after(new_tag)

            # 标记为已处理（防止父标签再处理）
            processed.add(tag)
        return soup.prettify(formatter="html")
    except Exception as e:
        print(repr(e))
        return content


if __name__ == '__main__':
    content = """<p>\u200b\u200b\u200b\u200bWe will be doing systems maintenance from 8&#58;30 pm (AEDT) Friday 28 November 2025 to 12 noon (AEDT) Saturday 29 November 2025.</p>\r\n\r\n<p>During this time, some of the following online services may&#160;be unavailable&#58;</p>\r\n\r\n<ul>\r\n\t<li>ImmiAccount</li>\r\n\t<li>eLodgement (online visa and citizenship applications)</li>\r\n\t<li>My Health Declarations (MHD) service</li>\r\n\t<li>eMedical</li>\r\n\t<li>Visa Entitlement Verification Online (VEVO)</li>\r\n\t<li>LEGENDcom</li>\r\n\t<li>Australian Trusted Trader</li>\r\n\t<li>Employment Suitability Clearances</li>\r\n\t<li>Detention Visitor Application</li>\r\n\t<li>APEC Business Travel Card (ABTC)</li>\r\n\t<li>Humanitarian Entrants Management System (HEMS)</li>\r\n\t<li>Adult Migrant English Program Reporting and Management System (ARMS)</li>\r\n\t<li>Education Provider Report (eBIT)</li>\r\n\t<li>Visa Pricing Estimator</li>\r\n\t<li>MSI Register</li>\r\n\t<li>Australian Migration Status (AMS) Training Portal</li>\r\n\t<li>Online Payment Portal</li>\r\n\t<li>Registration Gateway.</li>\r\n</ul>\r\n\r\n<p>If you receive a 'Service Temporarily Unavailable' message during this time, please try again after the outage.</p>\r\n\r\n<p>If your current visa is due to expire on 28 November 2025 and you intend to stay in Australia, you must lodge your application before <strong>8&#58;30 pm (AEDT) Friday 28 November</strong>.&#160;</p>\r\n\r\n<p>We apologise for the inconvenience and thank you for your patience.</p>\r\n"""
    print(parserHtml(content))
