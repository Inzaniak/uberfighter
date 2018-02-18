import requests
from bs4 import BeautifulSoup

url = 'https://cache-api.ranker.com/lists/2184824/items?limit=100&offset=0&include=votes,wikiText,rankings,openListItemContributors&propertyFetchType=ALL&liCacheKey=null'
url_reddit = 'https://www.reddit.com/r/AskReddit/comments/2b1636/if_you_could_have_one_useless_superpower_what.json'

data = requests.get(url_reddit,headers={'user-agent':'lel'}).json()

# for el in data['listItems']:
#     print(BeautifulSoup(el['name'],'html.parser').text)

for el in data[1]['data']['children']:
    try:
        print(el['data']['body'].replace('\n',''))
    except:
        pass