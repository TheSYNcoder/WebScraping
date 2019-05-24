'''

Just a simple script to to extract all job descriptions along with its url from craigslist
'''


from bs4 import BeautifulSoup
import requests
import re
import lxml

url = 'https://boston.craigslist.org/search/sof'

response = requests.get(url) #gets the response
# no = re.compile('^2[0-9]*')
assert (response.status_code == 200)


data = response.content #gets the content from the response

soup = BeautifulSoup(data, 'lxml') #Beautiful Soup object

a_tags = soup.find_all('a', {'class':'result-title'}) #finds a_tags by **kwargs only class names


for i in range(len(a_tags)):    #iterating over the class names
        print("Job:", a_tags[i].string)
        print("URL:", a_tags[i]['href'])
        print()
