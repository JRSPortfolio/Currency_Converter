import requests
from bs4 import BeautifulSoup

def getECBEuro():
    response = requests.get("https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html")
    page_content = BeautifulSoup(response.content, 'html.parser')
    tbody = page_content.find('tbody')
    tags = tbody.find_all('tr')
    values = {'EUR' : ['European euro', '1']}
    
    for tag in tags:
        td_tags = tag.find_all('td')
        # spans = tag.find_all('span')
        contents = [td.get_text() for td in td_tags]
        content = [item.replace('\n', '') for item in contents]
        
        values[content[0]] = [content[1], content[2]]
    
    return values
