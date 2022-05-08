import requests
from bs4 import BeautifulSoup
import json
import random
import re

class ImageScrape:
    ProxyList = []
    with open("./proxy.txt") as Pl:
        i = 0
        while i < 7533:
            content = Pl.readline().split(' ')[0]
            content = content.split(':')
            ProxyList.append(content)
            i += 1

    RandomItem = random.randrange(0, 7532)
    number = RandomItem

    IpAndPort = ProxyList[number]
    IP = IpAndPort[0]
    PORT = IpAndPort[1]

    proxy = {str(IP): str(PORT)}

    def mine_img(self):
        with open('imagejson.json') as imgjson:
            imgjson = json.load(imgjson)
            for url in imgjson['initial']:
                if url['hiRes'] != None:
                    imgurl = url['hiRes']
                    break
                else:
                    imgurl = url['large']
                    break
        return imgurl
    def amazonImageScrape(self, ProductUrl):
        headers = headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'referer': 'https://www.amazon.in/',
        }
        r = requests.get(ProductUrl, headers=headers, proxies=self.proxy)
        content = r.content

        soup = BeautifulSoup(content, 'lxml')
        image_script = soup.find_all('script', type='text/javascript')
        length = len(image_script)
        print(length)
        for image in image_script:
            print(re.search('''hiRes''', image.string))
            if re.search('''hiRes''', image.string) != None:
                jsonpatt = re.findall(r'''{.*}''', image.string)

                with open('imagejson.json', 'w') as imgjson:
                    replaced = jsonpatt[0].replace("'", '"')
                    imgjson.write(replaced)

                imgUrl = self.mine_img()
                break
        return imgUrl
    
    def flipkartImageScrape(self, ProductUrl):
        headers = headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'referer': 'https://www.flipkart.com',
        }
        r = requests.get(ProductUrl, headers=headers, proxies=self.proxy)
        content = r.content

        soup = BeautifulSoup(content, 'lxml')
        image = soup.select("._1YokD2._3Mn1Gg img")
        image = image[0].attrs['src']
        image_url = image.replace('128/128', '800/960')
        return image_url