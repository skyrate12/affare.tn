import requests
import re
import lxml.html
import json
import addons


class test:

    def __init__(self):
        self.site_api = {}
        self.req = requests.Session()
        self.get_links()


    def get_links(self):

        cv_url = 'https://www.affare.tn/petites-annonces/'
        for a in addons.categorieId:
            
            
            while True:
                for category in addons.categories:

                    # while True:
                    #     c = 2
                    #     for b in addons.villeId:
                    #         # print('ville', b)
                            
                    #         if c == 2:
                    #             self.site_api['categories'] = {category: {'Villes': {b: []}}}
                    #             save = json.dumps(self.site_api)

                    #             with open('site_api.json', 'w') as f:
                    #                 f.write(save)

                    #         with open('site_api.json', 'r') as f:
                    #             new = json.load(f)

                    #         new.update(self.site_api)
                    #         save = json.dumps(new, indent=3)

                    #         with open('site_api.json', 'w') as f:
                    #             f.write(save)


                    #         cat_url = cv_url+b+'/'+a

                    #         with open('categories-links.txt', 'a+') as f:
                    #             f.write(cat_url)

                    #         print('>>>', cat_url)
                    #         resp = self.req.get(cat_url)
                    #         print(resp.url)

                    #         p_urls = self.get_p_urls(cat_url)
                    #         p_details = self.p_details(p_urls, b, category, pos)

                    #         c = 0

                    #     break

                    while True:
                        for k, v in addons.regionId.items():
                            print('ville', k)
                        
                            while True:
                                pos = False
                                c = 2
                                for e in v:
                                    # print('region', e)

                                    if c == 2:
                                        self.site_api['categories'] = {category: {'Villes': {k: {'regions':{e: []}}}}}
                                        save = json.dumps(self.site_api)

                                        with open('site_api.json', 'w') as f:
                                            f.write(save)

                                    
                                    # self.site_api['categories'] = {category: {'Villes': {k: {'regions':{e: []}}}}}

                                    with open('site_api.json', 'r') as f:
                                        new = json.load(f)

                                    new.update(self.site_api)
                                    save = json.dumps(new, indent=3)

                                    with open('site_api.json', 'w') as f:
                                        f.write(save)


                                    cat_url = cv_url+k+'/'+e+'/'+a

                                    with open('categories-links.txt', 'a+') as f:
                                        f.write(cat_url)

                                    # resp = self.req.get(cat_url)
                                    # print('>>>', x)
                                    # print(resp.url)

                                    p_urls = self.get_p_urls(cat_url)
                                    p_details = self.p_details(p_urls, k, e, category, pos)
                                    c = 0
                                
                                break
                        break

                break
            
        print('All Links are Scraped and Saved')


    def get_p_urls(self, cv_url):

        resp = self.req.get(cv_url)
        self.annonces_count = ''.join(
            re.findall('"one-line">\((.*?)\)', resp.text))
        pages = round(int(self.annonces_count) / 30)

        print('Number of ads', self.annonces_count)
        print('Number of Pages', pages)

        products_urls = []
        for page in range(pages):

            resp = self.req.get(cv_url+'?o='+str(page))
            print(resp.url)
            print('Getting products urls from page:', page, 'of', pages)

            p_urls = re.findall('"product-x"><a\shref="(.*?)"\s', resp.text)
            for p_url in p_urls:
                products_urls.append('https://www.affare.tn'+p_url)

        print('product length:', len(products_urls))
        # print(products_urls)

        return products_urls

    def p_details(self, p_urls, ville, region, category, pos):
        
            count = 0
            for p_url in p_urls:

                print("Getting product info:", count, 'of', len(p_urls), 'current position', category, ville)
                count += 1
                resp = self.req.get(p_url)

                Product_url = p_url
                # print(p_url)

                Seller_name = ''.join(re.findall(
                    '"no-margin">(.*?)<\/h3>', resp.text))
                # print(Seller_name)

                Phone_number = ''.join(re.findall(
                    ':\snone;">(.*?)<\/div><button', resp.text))
                # print(Phone_number)

                Product_title = ''.join(re.findall(
                    'name\sno-margin">(.*?)<\/h1>', resp.text))
                # print(Product_title)

                Product_price = ''.join(re.findall(
                    '"price2">(.*?)<\/span>', resp.text))
                # print(Product_price)

                Created_date = ''.join(re.findall(
                    'span><\/div><div>(.*?)<\/div>', resp.text))
                # print(Created_date)

                doc = lxml.html.fromstring(resp.content)
                Description = doc.xpath(
                    '/html/body/div[3]/div/div/div/div/div[1]/div/div[3]/p/text()')
                # print(Description)

                images = []
                imgs = re.findall('e:url\(\/image\/(.*?)\);"><\/div>', resp.text)
                for img in imgs:
                    images.append('https://www.affare.tn/large/'+img)
                # print(images)

                properties = re.findall('"prop-1">(.*?)<\/div>', resp.text)
                valeurs = re.findall('"valeur-1">(.*?)<\/div>', resp.text)
                Details = dict(zip(properties, valeurs))
                # print(Details)

                if pos == False:

                    self.site_api['categories'][category]['Villes'][ville]['regions'][region].append({'Product_url': Product_url, 'Seller_name': Seller_name, 'Phone_number': Phone_number, 'Product_title': Product_title, 'Product_price': Product_price, 'Created_date': Created_date, 'Description': Description, 'images': images, 'Details': Details})


                    with open('site_api.json', 'r') as f:
                        new = json.load(f)

                    new.update(self.site_api)
                    save = json.dumps(new, indent=3)

                    
                    with open('site_api.json', 'w') as f:
                        f.write(save)

                    


