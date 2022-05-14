import scrapy

#setting the limit of pages before 100
page_limit = True
if page_limit == True:
    pages = 100

class Link(scrapy.Item):
    link = scrapy.Field()

#creating the class Spider for scapry
class LinksSpider(scrapy.Spider):
    name = 'places'
    allowed_domains = ['https://www.formula1.com']
    try:
        with open("../../years.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:pages]
    except:
        start_urls = []

    # get the list of places for every year on the website
    # starting from first place(country), we dont count all places
    def parse(self, response):
        print(response)
        xpath = '(//ul)[12]/li/a/@href'
        places = response.xpath(xpath)
        for p in places[1:]:
            l = Link()
            l['link'] ='https://www.formula1.com' + p.get()
            print(l)
            yield l
