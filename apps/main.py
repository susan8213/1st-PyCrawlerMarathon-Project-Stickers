import os
import re
import json
import urllib
import argparse
import requests
from bs4 import BeautifulSoup


def crawler_main(args):

    if args.type == 'product':
        product_spider(args.value)
    elif args.type == 'author':
        author_spider(args.value)
    else:
        raise AttributeError('Your request is not supported: ', args)

def product_spider(product_id):
    save_path = './img/{}'.format(product_id)
    if not os.path.isdir(save_path):
        os.makedirs(save_path)

    url = 'https://store.line.me/stickershop/product/{}'.format(product_id)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for idx, element in enumerate(soup.find_all('li', attrs={'class': 'mdCMN09Li'})):
        data = json.loads(element['data-preview'])
        img_url = data.get('animationUrl') or data['staticUrl']
        img_url = img_url.split(';compress=true')[0]
        img_type = img_url.split('.')[-1]

        urllib.request.urlretrieve(img_url, '{}/{:03}.{}'.format(save_path, idx, img_type)) 
        print('Downloading sticker: ', img_url)


def author_spider(author_id):
    url = 'https://store.line.me/stickershop/author/{}'.format(author_id)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for element in soup.find_all('li', attrs={'class': 'mdCMN02Li'}):
        product_id = re.search(r'\/product/(\d+)\/', element.find('a')['href']).group(1)
        sticker_title = element.find('p', attrs={'class': 'mdCMN05Ttl'}).text
        print('Sticker Product: ', product_id, sticker_title)
        product_spider(product_id)
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--type', '-t', type=str, help='type: [product] or [author]')
    parser.add_argument('--value', '-v', type=str, help='id of the specific type')
    args = parser.parse_args()

    crawler_main(args)
