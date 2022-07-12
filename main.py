import csv
import requests
from bs4 import BeautifulSoup

def get_html(url):
    response = requests.get(url)
    return response.text

def get_all_links(html, links):
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find('div', class_='main-wrap').find_all('div', class_='product-size-wrap')
    for td in tds:
        a = td.find('a', class_='product-link').get('href')
        link = a
        links.append(link)
    return links

def get_div(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = soup.find('h1', itemprop="name").text
    except:
        name = "None"
    all_ch_name = soup.find('div', class_="temp").find_all('div', class_='name')
    all_ch_value = soup.find('div', class_="temp").find_all('div', class_='value')
    nx = []
    nt = []
    for y in all_ch_name:
        nx.append(str(y.get_text(strip=True)))
    for z in all_ch_value:
        nt.append(str(z.get_text(strip=True, separator=', ')))
    data = {'Наименование': name}
    for i in range(len(nx)):
        data[nx[i]] = nt[i]
    bar_code = data.get('Артикул', 0000000000000)
    Power = data.get('Мощность', None)
    if Power == None:
        Power = data.get('Мощность потребляемая', None)
    infor = {
        'bar_code': bar_code,
        'name': name,
        'Power': Power
    }
    return infor

def write_csv(datas):
    with open('bafus.csv', 'a') as f:
        writer = csv.writer(f, delimiter = ';')
        writer.writerow(('Артикул','Наименование','Мощность'))
        for data in datas:
            writer.writerow((data['bar_code'],
                            data['name'],
                            data['Power']))

def main():
    url = 'https://www.bafus.ru/sq/ntu/'
    links = []
    datas = []
    for j in range(1, 9):
        all_links = get_all_links(get_html(url + 'page:' + str(j) + '/'), links)
    for link in all_links:
        html = get_html(link)
        datas.extend(get_div(html))
        print(datas)

if __name__ == '__main__':
    main()

