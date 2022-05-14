import scrapy

class Link(scrapy.Item):
    link = scrapy.Field()

#creating the class Spider for scapry
class LinkListsSpider(scrapy.Spider):
    name = 'years'
    allowed_domains = ['www.formula1.com']
    start_urls = ['https://www.formula1.com/en/results.html']

    # get thed list of year urls
    def parse(self, response):
        xpath = '(//ul)[10]/li/a/@href'
        years_url = response.xpath(xpath)
        for y in years_url:
            l = Link()
            l['link'] = 'https://www.formula1.com' + y.get()
            yield l

