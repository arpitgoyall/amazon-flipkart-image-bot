from telegram import *
from telegram.ext import *
import re
from scraping import *

# Settings = SettingsFunctions()
Scrape = ImageScrape()

bot = Bot("Bot Token here") #Your bor token

def Find(string):
        # findall() has been used 
        # with valid conditions for urls in string
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex,string)      
        return [x[0] for x in url]

def Unshort_urls(urls):
    unshort_urls = []
    for u in urls:
        try:
            session = requests.Session()  # so connections are recycled
            resp = session.head(u, allow_redirects=True)
            print(resp.url)
            unshort_urls.append(resp.url)
        except:
            session = requests.Session()  # so connections are recycled
            resp = session.head(f'http://{u}', allow_redirects=True)
            print(resp.url)
            unshort_urls.append(resp.url)
    print(unshort_urls)
    return unshort_urls

class Message:
    
    def send_message(update: Update, context: CallbackContext):

        string = update.effective_message.text
        if string == None:
            string = update.effective_message.caption
            if string == None:
                update.message.reply_text("Please send message in a correct format!")
                return

        # Finds link in the message
        extracted_link = Find(string)
        if extracted_link == []:
            update.message.reply_text("Url not found")
            return

        # Unshorting urls
        unshort_urls = Unshort_urls(extracted_link)
        allImgUrls = []
        for url in unshort_urls:
            # For Flipkart
            if 'flipkart.com' in url:
                try:
                    # Runs Flipkart scraping script
                    imgUrl = Scrape.flipkartImageScrape(url)
                    allImgUrls.append(imgUrl)
                except:
                    pass

            # For Amazon Images
            if re.search(r"amazon\..*?/", url) != None:
                try:
                    # Runs Amazon scraping script
                    imgUrl = Scrape.amazonImageScrape(url)
                    allImgUrls.append(imgUrl)
                except:
                    pass

        print('COMPLETED TAKING IMAGES')


        old_msg = update.effective_message.text
        if old_msg == None:
            old_msg = update.effective_message.caption
        print(old_msg)
            
        def photo_msg():
            if len(allImgUrls) == 1:
                try:
                    update.message.reply_media_group([InputMediaPhoto(allImgUrls[0], caption=old_msg)])
                except:
                    update.message.reply_text(old_msg, disable_web_page_preview=True)
            elif len(allImgUrls) > 1:
                try:
                    update.message.reply_media_group([InputMediaPhoto(allImgUrls[0], caption=old_msg)] + [InputMediaPhoto(url) for url in allImgUrls[1:]])
                except:
                    update.message.reply_text(old_msg, disable_web_page_preview=True)
            else:
                update.message.reply_text(old_msg, disable_web_page_preview=True)
        photo_msg()