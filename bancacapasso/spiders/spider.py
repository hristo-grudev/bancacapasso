import scrapy

from scrapy.loader import ItemLoader
from ..items import BancacapassoItem
from itemloaders.processors import TakeFirst


class BancacapassoSpider(scrapy.Spider):
	name = 'bancacapasso'
	start_urls = ['https://www.bancacapasso.it/news-dalla-banca/']

	def parse(self, response):
		post_links = response.xpath('//article/div/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="next page-numbers"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//h3[@class="title-news"]/text()').get()
		description = response.xpath('//div[@class="ba-page-content"]//text()[normalize-space() and not(ancestor::h3[@class="title-news"] | ancestor::date)]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//date/text()').get()

		item = ItemLoader(item=BancacapassoItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
