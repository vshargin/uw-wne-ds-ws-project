import scrapy

class Table(scrapy.Item):
    Pos = scrapy.Field()
    No = scrapy.Field()
    Driver = scrapy.Field()
    Car = scrapy.Field()
    LAPS = scrapy.Field()
    TIME = scrapy.Field()
    PTS = scrapy.Field()
    Location = scrapy.Field()
    Race_name = scrapy.Field()
    Date = scrapy.Field()
    Season = scrapy.Field()
    Place = scrapy.Field()

#creating the class Spider for scapry
class LinksSpider(scrapy.Spider):
    name = 'data'
    allowed_domains = ['https://www.formula1.com']
    try:
        with open("../../places.csv", "rt") as f:
            # starting to execute the links from csv starting from 1 because of heading
            start_urls = [url.strip() for url in f.readlines()][1:]
    except:
        start_urls = []

    # get the data about races, driver, places, result and other additional info
    def parse(self, response):
        t = Table()

        Pos1 = '//tbody//tr//td[@class="dark"]/text()'
        No1 = '//tbody//tr//td[@class="dark hide-for-mobile"]/text()'
        Driver1 = '//span[@class="hide-for-mobile"]/text()'
        Car1 = '//tbody//tr//td[@class="semi-bold uppercase hide-for-tablet"]/text()'
        PTS1 = '//tbody//tr//td[@class="bold"]/text()'
        Location1 = '//span[@class="circuit-info"]/text()'
        Race_name1 = '//h1[@class="ResultsArchiveTitle"]/text()'
        Date1 = '//span[@class="full-date"]/text()'
        Season1 = '// a[@data-name = "year"]/text()'
        Place1 = '//a[@data-name="meetingKey"]/text()'

        t['Pos'] = response.xpath(Pos1).getall()
        t['No'] = response.xpath(No1).getall()
        t['Driver'] = response.xpath(Driver1).getall()
        t['Car'] = response.xpath(Car1).getall()
        t['PTS'] = response.xpath(PTS1).getall()
        t['Location'] = response.xpath(Location1).getall()
        t['Race_name'] = response.xpath(Race_name1).getall()
        t['Date'] = response.xpath(Date1).getall()
        t['Season'] = response.xpath(Season1).getall()
        t['Place'] = response.xpath(Place1).getall()

        yield t