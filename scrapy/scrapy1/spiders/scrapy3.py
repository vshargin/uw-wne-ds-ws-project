import scrapy
from scrapy.exceptions import CloseSpider

limit = True

class Table(scrapy.Item):
    SEASON = scrapy.Field()
    RACE_NAME = scrapy.Field()
    FULL_RACE_NAME = scrapy.Field()
    RACE_DATE = scrapy.Field()
    RACE_LOCATION = scrapy.Field()
    POS = scrapy.Field()
    DRIVER = scrapy.Field()
    CAR = scrapy.Field()
    PTS = scrapy.Field()

#creating the class Spider for scapry
class LinksSpider(scrapy.Spider):
    scraped_pages = 0
    name = 'data'
    allowed_domains = ['formula1.com']
    try:
        with open("places.csv", "rt") as f:
            # starting to execute the links from csv starting from 1 because of heading
            start_urls = [url.strip() for url in f.readlines()][1:]
    except:
        start_urls = []

    # get the data about races, driver, places, result and other additional info
    def parse(self, response):
        if limit and self.scraped_pages >= 100:
            raise(CloseSpider)
        Location1 = 'normalize-space(//span[@class="circuit-info"])'
        Race_name1 = 'normalize-space(//h1[@class="ResultsArchiveTitle"])'
        Date1 = 'normalize-space(//span[@class="full-date"])'
        Season1 = 'normalize-space(// a[@data-name = "year"])'
        Place1 = 'normalize-space(//a[@data-name="meetingKey"])'
        location = response.xpath(Location1).get()
        race_name = response.xpath(Race_name1).get()
        date = response.xpath(Date1).get()
        season = response.xpath(Season1).get()
        track_name = response.xpath(Place1).get()

        Pos1 = '//tbody//tr//td[@class="dark"]/text()'
        Driver1 = '//span[@class="hide-for-mobile"]/text()'
        Car1 = '//tbody//tr//td[@class="semi-bold uppercase hide-for-tablet"]/text()'
        PTS1 = '//tbody//tr//td[@class="bold"]/text()'

        Pos = response.xpath(Pos1).getall()
        Driver = response.xpath(Driver1).getall()
        Car = response.xpath(Car1).getall()
        PTS = response.xpath(PTS1).getall()

        for i in range(len(Pos)):
            t = Table()
            t['SEASON'] = season
            t['RACE_NAME'] = location
            t['FULL_RACE_NAME'] = race_name
            t['RACE_DATE'] = date
            t['RACE_LOCATION'] = track_name
            t['POS'] = Pos[i]
            t['DRIVER'] = Driver[i]
            t['CAR'] = Car[i]
            t['PTS'] = PTS[i]
            yield t

        self.scraped_pages += 1
        