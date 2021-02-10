import scrapy
from scrapy.exceptions import CloseSpider

from scrapy.loader import ItemLoader
from ..items import CdpItem
from itemloaders.processors import TakeFirst


class CdpSpider(scrapy.Spider):
	name = 'cdp'
	start_urls = ['https://www.cdp.it/sitointernet/it/news_e_progetti.page']
	last_post = ''
	page = 1

	def parse(self, response):
		post_links = response.xpath('//div[@class="slide"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		self.page += 1
		next_page = f'https://www.cdp.it/sitointernet/it/news_e_progetti.page?2_item={self.page}&#tabellaricerca-progetti'

		if self.last_post == post_links[-1]:
			raise CloseSpider('no more pages')

		self.last_post = post_links[-1]

		yield response.follow(next_page, self.parse)


	def parse_post(self, response):
		with open('asd.html', 'wb') as f:
			f.write(response.body)
		title = response.xpath('//h1//text()').get()
		description = response.xpath('//div[@data-attr-id="Abstract"]//text()[normalize-space()]|//div[@class="text-large-secondary"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="text-extra-small-main text-bluegrey"]/text()').get()

		item = ItemLoader(item=CdpItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
