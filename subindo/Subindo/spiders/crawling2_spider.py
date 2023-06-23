from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.exporters import CsvItemExporter
import csv
import scrapy

class CrawlingSpider(CrawlSpider):
    name = 'mycrawler'
    allowed_domains = ['espn.com.br']
    start_urls = [
        'https://www.espn.com.br/nba/time/estatisticas/_/nome/mil/milwaukee-bucks']

    rules = (
        Rule(LinkExtractor( 
            allow=''), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        name = response.css('span.db.pr3.nowrap::text').get()
        points = response.xpath(
            '//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section/div/div[5]/div[2]/div/div[2]/table/tbody/tr[1]/td[4]/span/text()').get()
        j = response.xpath(
            '//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section/div/div[5]/div[2]/div/div[2]/table/tbody/tr[1]/td[1]/span/text()').get()
        gs = response.xpath(
            '//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section/div/div[5]/div[2]/div/div[2]/table/tbody/tr[1]/td[2]/span/text()').get()
        Min = response.xpath(
            '//*[@id="fittPageContainer"]/div[2]/div[5]/div/div/section/div/div[5]/div[2]/div/div[2]/table/tbody/tr[1]/td[3]/span/text()').get()
        Win = response.xpath(
            '//*[@id="fittPageContainer"]/div[2]/div[1]/div/div/div/div/div/ul/li[1]/text()').get()
        
        if name and points and j and gs and Min and Win:
            data = {
                'names': name,
                'J': j,
                'gs': gs,
                'min': Min,
                'points': points,
                'Win/defeat': Win,
            }

            yield data
            self.export_to_csv(data)

    def export_to_csv(self, data):
        
        filename = 'file.csv'
        fieldnames = ['names',  'J',  'gs',  'min',  'points',  'Win/defeat']
        header = 'names,J,gs,min,points,Win/defeat'

        with open(filename, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(data)


if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess
    process = CrawlerProcess()
    process.crawl(CrawlingSpider)
    process.start()