import scrapy


class RankItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    year = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    company_rank = scrapy.Field()
    company_list = scrapy.Field()
    company_score= scrapy.Field()

