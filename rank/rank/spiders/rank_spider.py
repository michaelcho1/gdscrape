from scrapy import Spider, Request
from rank.items import RankItem
import re



class RankSpider(Spider):
    name = "rank_spider"
    allowed_domains = ['www.glassdoor.com']
    start_urls = ['https://www.glassdoor.com']

    def parse(self,response):

        result_urls = ['https://www.glassdoor.com/Award/Best-Places-to-Work-{}-LST_KQ0,24.htm'.format(x) for x in range(2009,2020)]

        for url in result_urls:
            yield Request(url=url, callback= self.parse_result_page)


    def parse_result_page(self,response):

        company_list = response.xpath('//p[@class="h2 m-0 strong"]/text()').extract()

        company_rank = response.xpath('//span[@class="h2 listRank my-0 mr-xsm strong"]/text()').extract()

        company_score = response.xpath('//span[@class="ratingNum "]/text()').extract() 

        try:
            year = re.findall('\d+', response.xpath('//h1[@class="listTitle center my-xl strong"]/small/text()').extract_first())[0]
        except: 
            year = ''

        try: 
            start_date = re.findall('\d+/\d+/\d+',response.xpath('//span[@class="minor"]/text()').extract_first())[0]
        except:
            start_date = ''

        try:
            end_date =  re.findall('\d+/\d+/\d+',response.xpath('//span[@class="minor"]/text()').extract_first())[1]
        except: 
            end_date = ''


        review_item = RankItem()
        review_item['year'] = year
        review_item['start_date'] = start_date
        review_item['end_date'] = end_date
        review_item['company_rank'] = company_rank
        review_item['company_list'] = company_list
        review_item['company_score'] = company_score

        yield review_item