import requests
from bs4 import BeautifulSoup

def findOnePage():
    url = 'http://ris.szpl.gov.cn/bol/'
    r = requests.get(url)
    soap = BeautifulSoup(r.text, 'lxml')
    #print(soap.prettify())
    projectTable = soap.find('table', id='DataList1')
    projectRowsText = projectTable.find('tr')
    if projectRowsText is None:
        print('has no row')
        return

    rowList = projectRowsText.find_all('tr', recursive='False')
    for project in rowList:
        link = project.find('a')
        if link is None:
            continue
        print('')
        columns = project.find_all('td')
        for column in columns:
            print(column.text)
        print(link['href'])


findOnePage()
