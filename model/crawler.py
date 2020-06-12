from bs4 import BeautifulSoup
from urllib.parse import quote
from urllib.request import urlopen
import re


base_url = 'https://www.sogou.com'
print("请输入你的问题：")
user_input = input()
url = base_url + \
    f"/sogou?query={quote(user_input)}&ie=utf8&insite=wenwen.sogou.com&pid=sogou-wsse-a9e18cb5dd9d3ab4&rcer="

question_answer_dicts = {}
list_page = urlopen(url).read().decode('utf-8')
list_soup = BeautifulSoup(list_page, features='lxml')
for vrTitle in list_soup.find_all('h3', class_='vrTitle'):
    question = vrTitle.get_text()
    print(question)
    answer_page_url = base_url + vrTitle.find('a').get('href')
    res = urlopen(answer_page_url).read().decode('utf-8')
    pttn = re.compile(r'"(https.+htm)"')
    answer_page_url = re.findall(pttn, res)[0]
    answer_page = urlopen(answer_page_url).read().decode('utf-8')
    answer_soup = BeautifulSoup(answer_page, features='lxml')
    answer = answer_soup.find(
        'pre', class_="replay-info-txt answer_con").get_text()
    print(answer)
    question_answer_dicts[question] = answer

print(question_answer_dicts)
