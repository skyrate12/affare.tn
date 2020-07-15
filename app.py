import requests
import lxml.html
from bs4 import BeautifulSoup
import requests

content = []

categorieId = 'voiture-neuve-occassion-prix-tayara-a-vendre'
villeId = 'grand-tunis'
url = f'https://www.affare.tn/petites-annonces/{villeId}/{categorieId}'

req = requests.Session()
resp = req.get(url)
soup = BeautifulSoup(resp.content, features='lxml')

products_urls = []
product_x = soup.find_all('a', class_='saz')

for product in product_x:
    products_urls.append('https://www.affare.tn'+product.attrs['href'])
    # print(html.content)
details = {
    
    'first_page': 'Number of products '+ str(len(products_urls)),

}
content.append(details)

for products_url in products_urls:

    html = requests.get(products_url)
    doc = lxml.html.fromstring(html.content)

    products_url = products_url
    print('products_url', products_url)

    product_title = ''.join(doc.xpath('/html/body/div[3]/div/div/div/div/div[1]/div/div[2]/div[3]/h1/text()'))
    print('product_title:', product_title)

    phone = ''.join(doc.xpath('/html/body/div[3]/div/div/div/div/div[2]/div[2]/text()'))
    print('phone:', phone)

    seller_info = ''.join(doc.xpath('/html/body/div[3]/div/div/div/div/div[2]/div[1]/div/a/div/div/h3/text()'))
    print('seller_info:', seller_info)

    product_price = ''.join(doc.xpath('/html/body/div[3]/div/div/div/div/div[1]/div/div[2]/div[4]/span/text()'))
    print('product_price:', product_price)

    created_date = ''.join(doc.xpath('/html/body/div[3]/div/div/div/div/div[1]/div/div[2]/div[5]/text()'))
    print('created_date:', created_date)

    ENERGIE = ''.join(doc.xpath('/html/body/div[3]/div/div/div/div/div[1]/div/div[3]/div/div[1]/div[2]/text()'))
    print('ENERGIE:', ENERGIE)

    ANNÉE = ''.join(doc.xpath('/html/body/div[3]/div/div/div/div/div[1]/div/div[3]/div/div[2]/div[2]/text()'))
    print('ANNÉE:', ANNÉE)

    KILOMÉTRAGE = ''.join(doc.xpath('/html/body/div[3]/div/div/div/div/div[1]/div/div[3]/div/div[3]/div[2]/text()'))
    print('KILOMÉTRAGE:', KILOMÉTRAGE)

    PUISSANCE = ''.join(doc.xpath('/html/body/div[3]/div/div/div/div/div[1]/div/div[3]/div/div[4]/div[2]/text()'))
    print('PUISSANCE:', PUISSANCE)

    MISE_EN_CIRCULATION = ''.join(doc.xpath('/html/body/div[3]/div/div/div/div/div[1]/div/div[3]/div/div[5]/div[2]/text()'))
    print('MISE_EN_CIRCULATION:', MISE_EN_CIRCULATION)

    BOÎTE = ''.join(doc.xpath('/html/body/div[3]/div/div/div/div/div[1]/div/div[3]/div/div[6]/div[2]/text()'))
    print('BOÎTE:', BOÎTE)

    resp = req.get(products_url)
    soup = BeautifulSoup(resp.content, features='lxml')

    try:
        Description = ''.join(soup.find('div', class_='description').text).replace('Description', '')
        print('Description:', Description)
    except:
        Description = None
        print('Description:', Description)


    image_urls = soup.find_all('ul', class_ ='bxslider')
    # print(image_urls)

    images = []
    for image_url in image_urls:
        for i in image_url.find_all('li'):
            images.append(i.find('a').attrs['href'])
    print(images)


    metadata = {

        'products_url': products_url,
        'product_title': product_title,
        'phone': phone,
        'seller_info': seller_info,
        'product_price': product_price,
        'created_date': created_date,
        'ENERGIE': ENERGIE,
        'ANNÉE': ANNÉE,
        'KILOMÉTRAGE': KILOMÉTRAGE,
        'PUISSANCE': PUISSANCE,
        'MISE_EN_CIRCULATION': MISE_EN_CIRCULATION,
        'BOÎTE': BOÎTE,
        'Description': Description,
        'images': images

    }

    content.append(metadata)
    with open('data.json', 'w', encoding='utf8') as f:
        f.write(str(content))

    print('_____________________________________________________________')

