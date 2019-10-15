# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GlassdoorItem(scrapy.Item):
    reviewspro = scrapy.Field()
    reviewscon = scrapy.Field()
    number_reviews = scrapy.Field()
    recommendation = scrapy.Field()
    ceo_score = scrapy.Field()
    culture_score = scrapy.Field()
    positive_xp = scrapy.Field()
    neutral_xp = scrapy.Field()
    negative_xp = scrapy.Field()
    interview_difficulty = scrapy.Field()
    interview_n_reviews = scrapy.Field()
    benefits_n_reviews = scrapy.Field()
    benefits_rating = scrapy.Field()
    year = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    company = scrapy.Field()
    website = scrapy.Field()
    location = scrapy.Field()
    employee_count= scrapy.Field()
    founded = scrapy.Field()
    ticker = scrapy.Field()
    cotype = scrapy.Field()
    industry = scrapy.Field()
    revenue = scrapy.Field()