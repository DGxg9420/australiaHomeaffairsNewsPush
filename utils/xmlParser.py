import html
from utils.translator import translate
from bs4 import BeautifulSoup, NavigableString
import re
import unicodedata


def get_rendered_text(text: str) -> str:
    """
    模拟 print() 的“视觉效果”，返回干净、可读、无隐藏字符的纯文本。
    """
    # 1. 移除常见零宽字符和 BOM
    cleaned = re.sub(r'[\u200b\u200c\u200d\u2060\ufeff\u00ad]', '', text)

    # 2. 将不间断空格 \xa0 替换为普通空格
    cleaned = cleaned.replace('\xa0', ' ')

    # 3. Unicode 正规化（组合字符统一）
    cleaned = unicodedata.normalize('NFC', cleaned)

    # 4. 可选：压缩多余空白（保留单个换行，合并空行为一个）
    # 先将 \r\n / \r 统一为 \n
    cleaned = re.sub(r'\r\n|\r', '\n', cleaned)
    # 合并多个连续空行为一个空行
    cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)
    # 去除每行首尾空白
    cleaned = '\n'.join(line.strip() for line in cleaned.splitlines())
    # 去除首尾空白
    cleaned = cleaned.strip()

    return cleaned


def parserHtml(content_html: str, APP_KEY: str, APP_SECRET: str)  -> str:
    try:
        # 解析
        soup = BeautifulSoup(content_html, 'html.parser')
        clean_text = get_rendered_text(soup.text)
        translate_text = translate(clean_text, APP_KEY, APP_SECRET)
        lines_clean = clean_text.split('\n')
        lines_translate = translate_text.split('\n')
        new_lines = []
        for en_text, zh_text in zip(lines_clean, lines_translate):
            new_line = f"{en_text}\n{zh_text}"
            new_lines.append(new_line)
        return '\n\n'.join(new_lines)
    except Exception as e:
        print(repr(e))
        return content


if __name__ == '__main__':
    content = """<p>\u200b\u200b\u200b\u200bWe will be doing systems maintenance from 8&#58;30 pm (AEDT) Friday 28 November 2025 to 12 noon (AEDT) Saturday 29 November 2025.</p>\r\n\r\n<p>During this time, some of the following online services may&#160;be unavailable&#58;</p>\r\n\r\n<ul>\r\n\t<li>ImmiAccount</li>\r\n\t<li>eLodgement (online visa and citizenship applications)</li>\r\n\t<li>My Health Declarations (MHD) service</li>\r\n\t<li>eMedical</li>\r\n\t<li>Visa Entitlement Verification Online (VEVO)</li>\r\n\t<li>LEGENDcom</li>\r\n\t<li>Australian Trusted Trader</li>\r\n\t<li>Employment Suitability Clearances</li>\r\n\t<li>Detention Visitor Application</li>\r\n\t<li>APEC Business Travel Card (ABTC)</li>\r\n\t<li>Humanitarian Entrants Management System (HEMS)</li>\r\n\t<li>Adult Migrant English Program Reporting and Management System (ARMS)</li>\r\n\t<li>Education Provider Report (eBIT)</li>\r\n\t<li>Visa Pricing Estimator</li>\r\n\t<li>MSI Register</li>\r\n\t<li>Australian Migration Status (AMS) Training Portal</li>\r\n\t<li>Online Payment Portal</li>\r\n\t<li>Registration Gateway.</li>\r\n</ul>\r\n\r\n<p>If you receive a 'Service Temporarily Unavailable' message during this time, please try again after the outage.</p>\r\n\r\n<p>If your current visa is due to expire on 28 November 2025 and you intend to stay in Australia, you must lodge your application before <strong>8&#58;30 pm (AEDT) Friday 28 November</strong>.&#160;</p>\r\n\r\n<p>We apologise for the inconvenience and thank you for your patience.</p>\r\n"""
    print(parserHtml(content, "15b861e879647f2f", "brKIT6xHPtOpOtF8MhQFf2j5mUB9PBji"))
