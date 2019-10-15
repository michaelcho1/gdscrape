from scrapy import Spider, Request
from tsr.items import TsrItem
import pandas as pd
import re
import math


class TsrSpider(Spider):
    name = 'tsr_spider'
    allowed_domains = ['www.buyupside.com']
    start_urls = ['https://www.buyupside.com/stockreturncalculator/stockreturncalcinput.php']

    def parse(self, response):
        tsr_one = pd.read_csv('tsr_one_ytd.csv')
        
        result_urls = ['https://www.buyupside.com/stockreturncalculator/stockreturncalccompute.php?symbol={}&interval=daily&start_month=12&start_year={}&end_month=10&end_year={}&submit=Calculate+Returns'.format(x,y,z) for x,y,z in tsr_one.values]

        for url in result_urls:
            yield Request(url = url, callback = self.parse_result_page)

    def parse_result_page(self, response):
        
        tsr_one_ytd_return = response.xpath('//table[@class = "formOutput"]/tr[12]/td[2]/text()').extract_first()

        try:
            ticker = re.findall('[A-Z ]+',response.xpath('//table[@class="formOutput"]/tr[1]/th/text()').extract_first())[-1].strip()
        except:
            ticker = ''

        begyear = re.findall('.{4}$', response.xpath('//table[@class="formOutput"]/tr[2]/td[2]/text()').extract_first())
        endyear = re.findall('.{4}$', response.xpath('//table[@class="formOutput"]/tr[4]/td[2]/text()').extract_first())
        beg = response.xpath('//table[@class="formOutput"]/tr[2]/td[2]/text()').extract_first()
        end = response.xpath('//table[@class="formOutput"]/tr[4]/td[2]/text()').extract_first()

        item = TsrItem()
        item['tsr_one_ytd'] = tsr_one_ytd
        item['ticker'] = ticker
        item['begyear'] = begyear
        item['endyear'] = endyear
        item['beg'] = beg
        item['end'] = end
        
        yield item
