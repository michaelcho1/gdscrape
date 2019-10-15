from scrapy import Spider, Request
from glassdoor.items import GlassdoorItem
import re



class GlassdoorSpider(Spider):
    name = "glassdoor_spider"
    allowed_domains = ['www.glassdoor.com']
    start_urls = ['https://www.glassdoor.com']

    def parse(self,response):

        result_urls = ['https://www.glassdoor.com/Award/Best-Places-to-Work-{}-LST_KQ0,24.htm'.format(x) for x in range(2009,2020)]

        for url in result_urls:
            yield Request(url=url, callback= self.parse_result_page,dont_filter=True)


    def parse_result_page(self,response):

        company_urls = response.xpath('//div[@class="employerLogo ml-xl mr-std"]/a/@href').extract()

        company_urls = ['https://www.glassdoor.com{}'.format(x) for x in company_urls]

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

        for url in company_urls:
            yield Request(url=url, callback = self.parse_overview_page, dont_filter=True, meta = {'start_date': start_date, 'end_date':end_date, 'year':year})

    def parse_overview_page(self,response):
        start_date = response.meta['start_date']
        end_date = response.meta['end_date']
        year = response.meta['year']


        benefitsurl = ''.join(response.xpath('//a[@class="eiCell cell benefits "]/@href').extract()+response.xpath('//a[@class="eiCell cell benefits active"]/@href').extract())

        benefits_url = 'https://www.glassdoor.com{}'.format(benefitsurl)

        company = response.xpath('//*[@id="DivisionsDropdownComponent"]/text()').extract_first()

        website = response.xpath('//div[@class="info flexbox row col-hh"]/div[1]/span/a/text()').extract_first()

        location = response.xpath('//div[@class="info flexbox row col-hh"]/div[2]/span/text()').extract_first()

        employee_count = response.xpath('//div[@class="info flexbox row col-hh"]/div[3]/span/text()').extract_first()

        founded = response.xpath('//div[@class="info flexbox row col-hh"]/div[4]/span/text()').extract_first()

        cotype = response.xpath('//div[@class="info flexbox row col-hh"]/div[5]/span/text()').extract_first()

        ticker = ''.join(re.findall('\(([^\)]+)\)', cotype))

        industry = response.xpath('//div[@class="info flexbox row col-hh"]/div[6]/span/text()').extract_first()

        revenue = response.xpath('//div[@class="info flexbox row col-hh"]/div[7]/span/text()').extract_first()

        yield Request(url=benefits_url, callback = self.parse_benefits_page, dont_filter=True, meta = {'start_date': start_date, 'end_date':end_date, 'year':year, 'company':company,'website':website,'location':location,'employee_count':employee_count,'founded':founded,'cotype':cotype, 'ticker':ticker, 'industry':industry, 'revenue':revenue})

    def parse_benefits_page(self,response):
        start_date = response.meta['start_date']
        end_date = response.meta['end_date']
        year = response.meta['year']
        company = response.meta['company']
        website = response.meta['website']
        location = response.meta['location']
        employee_count = response.meta['employee_count']
        founded = response.meta['founded']
        cotype = response.meta['cotype']
        ticker = response.meta['ticker']
        industry = response.meta['industry']
        revenue = response.meta['revenue']

        interviewurl = response.xpath('//a[@class="eiCell cell interviews "]/@href').extract_first()

        interview_url = 'https://www.glassdoor.com{}'.format(interviewurl)

        benefits_rating = response.xpath('//div[@class="ratingNum rating"]/text()').extract_first() 

        benefits_n_reviews = response.xpath('//div[@class="minor"]/span/text()').extract_first()

        yield Request(url=interview_url, callback = self.parse_interview_page, dont_filter=True, meta = {'start_date': start_date, 'end_date':end_date, 'year':year, 'company':company,'website':website,'location':location,'employee_count':employee_count,'founded':founded,'cotype':cotype, 'ticker':ticker,'industry':industry, 'revenue':revenue,'benefits_rating':benefits_rating, 'benefits_n_reviews': benefits_n_reviews})

    def parse_interview_page(self,response):
        start_date = response.meta['start_date']
        end_date = response.meta['end_date']
        year = response.meta['year']
        company = response.meta['company']
        website = response.meta['website']
        location = response.meta['location']
        employee_count = response.meta['employee_count']
        founded = response.meta['founded']
        cotype = response.meta['cotype']
        ticker = response.meta['ticker']
        industry = response.meta['industry']
        revenue = response.meta['revenue']
        benefits_rating = response.meta['benefits_rating']
        benefits_n_reviews = response.meta['benefits_n_reviews']

        reviewsurl = response.xpath('//a[@class="eiCell cell reviews "]/@href').extract_first() 

        reviews_url = 'https://www.glassdoor.com{}'.format(reviewsurl)

        interview_difficulty = response.xpath('//div[@class="difficultyLabel subtle"]/text()').extract_first()

        interview_n_reviews = re.findall('\d+', response.xpath('//div[@class="cell chartWrapper experience"]/h3/span/text()').extract_first())

        positive_xp = response.xpath('//div[@class="cell chartWrapper experience"]/div/div/div[2]/div/div[2]/div[2]/span/text()').extract_first()

        neutral_xp = response.xpath('//div[@class="cell chartWrapper experience"]/div/div/div[2]/div/div[3]/div[2]/span/text()').extract_first()

        negative_xp = response.xpath('//div[@class="cell chartWrapper experience"]/div/div/div[2]/div/div[4]/div[2]/span/text()').extract_first()

        yield Request(url=reviews_url, callback = self.parse_reviews_page, dont_filter=True, meta = {'start_date': start_date, 'end_date':end_date, 'year':year, 'company':company,'website':website,'location':location,'employee_count':employee_count,'founded':founded,'cotype':cotype, 'ticker':ticker,'industry':industry, 'revenue':revenue,'benefits_rating':benefits_rating, 'benefits_n_reviews': benefits_n_reviews, 'interview_difficulty':interview_difficulty, 'interview_n_reviews':interview_n_reviews, 'positive_xp':positive_xp, 'neutral_xp':neutral_xp, 'negative_xp':negative_xp})

    def parse_reviews_page(self,response):
        start_date = response.meta['start_date']
        end_date = response.meta['end_date']
        year = response.meta['year']
        company = response.meta['company']
        website = response.meta['website']
        location = response.meta['location']
        employee_count = response.meta['employee_count']
        founded = response.meta['founded']
        cotype = response.meta['cotype']
        ticker = response.meta['ticker']
        industry = response.meta['industry']
        revenue = response.meta['revenue']
        benefits_rating = response.meta['benefits_rating']
        benefits_n_reviews = response.meta['benefits_n_reviews']
        interview_difficulty = response.meta['interview_difficulty']
        interview_n_reviews = response.meta['interview_n_reviews']
        positive_xp = response.meta['positive_xp']
        neutral_xp = response.meta['neutral_xp']
        negative_xp = response.meta['negative_xp']
        

        culture_score = response.xpath('//div[@class="common__EIReviewsRatingsStyles__ratingNum mb-sm mb-md-0"]/text()').extract_first()

        recommendation = response.xpath('//tspan[@class="donut__DonutStyle__donutchart_text_val"]/text()').extract()[0]

        try:
            ceo_score = response.xpath('//tspan[@class="donut__DonutStyle__donutchart_text_val"]/text()').extract()[1]
        except:
            ceo_score = ''

        number_reviews = response.xpath('//div[@class="common__EIReviewSortBarStyles__sortsHeader row justify-content-between mt-md-xl mt-sm"]/h2/span/strong/text()').extract_first()

        reviews = response.xpath('//p[@class="common__EIReviewHighlightsStyles__highlightText my-0"]/span//text()').extract()

        reviews = re.sub('\(([^\)]+)\)',',,,', str(reviews)).split(',,,')

        reviewspro = (' '.join(re.findall('\w+', reviews[0]))) + ' '+ (' '.join(re.findall('\w+', reviews[1])))

        reviewscon = (' '.join(re.findall('\w+', reviews[2]))) + ' '+ (' '.join(re.findall('\w+', reviews[3])))

        review_item = GlassdoorItem()
        review_item['reviewspro'] = reviewspro
        review_item['reviewscon'] = reviewscon
        review_item['number_reviews'] = number_reviews
        review_item['recommendation'] = recommendation
        review_item['ceo_score'] = ceo_score
        review_item['culture_score'] = culture_score
        review_item['positive_xp'] = positive_xp
        review_item['neutral_xp'] = neutral_xp
        review_item['negative_xp'] = negative_xp
        review_item['interview_difficulty'] = interview_difficulty
        review_item['interview_n_reviews'] = interview_n_reviews
        review_item['benefits_n_reviews'] = benefits_n_reviews
        review_item['benefits_rating'] = benefits_rating
        review_item['year'] = year
        review_item['start_date'] = start_date
        review_item['end_date'] = end_date
        review_item['company'] = company
        review_item['website'] = website
        review_item['location'] = location
        review_item['employee_count'] = employee_count
        review_item['founded'] = founded
        review_item['cotype'] = cotype
        review_item['ticker'] = ticker
        review_item['industry'] = industry
        review_item['revenue'] = revenue

        yield review_item




