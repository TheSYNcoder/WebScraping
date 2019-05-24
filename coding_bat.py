'''
IN this script a website
https://codingbat.com/java
was scraped for all its problems and their examples , it required
3 loops of usage of Beautiful Soup to extract problems from all categories

'''

import re
import requests
from bs4 import  BeautifulSoup
import lxml
from fake_useragent import UserAgent


url = 'https://codingbat.com/java'

us = UserAgent()

header = {'user-agent':us.chrome}

page = requests.get(url , headers =header)

soup = BeautifulSoup(page.content , 'lxml')

div_tags = {div.a.span.string : 'https://codingbat.com'+div.a['href'] for div in soup.find_all('div' , attrs ={'class' : 'summ'})}
links_of_problem_categories =[]
for key,value in div_tags.items():
    links_of_problem_categories.append(value)


newlinks =[]
for link in links_of_problem_categories:
    problems_page = requests.get(link , headers = header)
    newsoup = BeautifulSoup(problems_page.content , 'lxml')
    div = newsoup.find('div', class_ ='tabc' )
    for td in div.table.find_all('td'):
        newlinks.append('https://codingbat.com' + td.a['href'])



# 'div', class_ ='tabin'  --> 'p' , class_='max2' -> navigable string
problem_description ={}
for link in newlinks:
    # print(link)
    problem_page = requests.get(link , headers = header)
    assert (problem_page.status_code == 200)
    problemsoup = BeautifulSoup(problem_page.content , 'lxml')
    indent_div = problemsoup.find('div',attrs={'class':'tabin'})

    problem_statement =indent_div.table.p.string
    siblings_of_statement = indent_div.table.div.next_siblings
    problem_description[problem_statement] = [sibling for sibling in siblings_of_statement if sibling.string is not None]
    print(problem_description[problem_statement])
    break
