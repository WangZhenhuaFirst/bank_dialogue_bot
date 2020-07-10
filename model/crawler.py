from bs4 import BeautifulSoup
from urllib.parse import quote
from urllib.request import urlopen
import re


def crawl_answer(user_input):
    base_url = 'https://www.sogou.com'
    url = base_url + \
        f"/sogou?query={quote(user_input)}&ie=utf8&insite=wenwen.sogou.com&pid=sogou-wsse-a9e18cb5dd9d3ab4&rcer="

    list_page = urlopen(url).read().decode('utf-8')
    list_soup = BeautifulSoup(list_page, features='lxml')
    for vrTitle in list_soup.find_all('h3', class_='vrTitle', limit=1):
        # question = vrTitle.get_text()
        # print(question)
        answer_page_url = base_url + vrTitle.find('a').get('href')
        res = urlopen(answer_page_url).read().decode('utf-8')
        print(f"res: {res}")

        # res并不是答案页面，但包含答案页面的URL。所以需要提取出URL，再打开该URL
        pttn = re.compile(r"URL='(.+)'")
        answer_page_url = re.findall(pttn, res)[0]
        print(f"answer_page_url: {answer_page_url}")
        answer_page = urlopen(answer_page_url).read().decode('utf-8')
        answer_soup = BeautifulSoup(answer_page, features='lxml')

        # 从页面中提取答案
        answer = ''
        answer = answer_soup.find(
            'pre', class_="replay-info-txt answer_con").get_text()
        print(f"answer:{answer}")
        # cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")
        # answer = cop.sub('', answer)
        answer = answer.replace("nbsp;", '')  # 删除一些特殊字符
        answer = answer[0:200] + '......'  # 只保留前200个字符，防止回答太长
        print(f"answer_re: {answer}")
    return answer
