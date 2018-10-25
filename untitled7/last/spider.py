
import requests,os,django,re
from bs4 import BeautifulSoup
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE","untitled7.settings")
application = get_wsgi_application()
django.setup()
from last.models import Notice



def get_page(url):
    res = requests.get(url)
    res.encoding = 'GBK'
    content = res.text
    return content


def get_noticeURL(content):
    pattern = re.compile('<i class="icon-double-angle-right".*?<a.*?href="(.*?)".*?</a>', re.S)
    result = pattern.findall(content)
    notices = []
    for url_ in result:
        url_ = 'http://pmc.whu.edu.cn/' + str(url_)
        notice = requests.get(url_)
        notice.encoding = 'GBK'
        notice = notice.text
        notices.append(notice)
    return notices


def parse_page_db(notices):
    global text

    for note in notices:
        items = {}
        tip = []
        soup = BeautifulSoup(note, 'html.parser')
        title = soup.find('h1').get_text()
        texts = soup.select('p[style]')
        try:
            picture = soup.find('img')
            img = picture.get('src')
        except:
            img = 'none'
        time = re.search('(\d{4}-\d{1,2}-\d{1,2})', note, re.S)
        if texts:
            for text in texts:
                text = text.get_text()
                tip.append(text.strip())
                text = '.'.join(tip)
                text = ''.join(text.split())
        else:text ='none'
        insertdata = Notice.objects.get_or_create(
            notice_title=title,
            notice_data=text,
            notice_picture=img,
            notice_time=time.group(0))

        items['标题'] = title
        items['正文'] = text
        items['照片'] = img
        items['时间'] = time.group(0)

def main(id):
    url = 'http://pmc.whu.edu.cn/list/1/page/' + str(id) + '.html'
    content = get_page(url)
    notices = get_noticeURL(content)
    parse_page_db(notices)

if __name__ == '__main__':
    for i in range(100):
        main(i)