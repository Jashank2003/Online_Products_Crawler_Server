import scrapy
import json

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.in']

    def start_requests(self):
        product_name = getattr(self, 'product_name', 'realme')
        product_category = getattr(self, 'product_category', 'aps')

        url = f'https://www.amazon.in/s?k={product_name}&crid={product_category}&ref=nb_sb_noss_2'

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        scraped_data = []

        for product in response.css('div.s-result-item'):
            item = {
                'title': product.css('span.a-size-medium.a-color-base.a-text-normal::text').get(default=''),
                'price': product.css('span.a-price-whole::text').get(default=''),
                'image_link': product.css('img.s-image::attr(src)').get(default=''),
               'link_to_product': product.css('a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal::attr(href)').get(default=''),
            }
            scraped_data.append(item)

        # Save the scraped data to output.json
        with open('output.json', 'w', encoding='utf-8') as json_file:
            json.dump({'data': scraped_data}, json_file, ensure_ascii=False, indent=2)

        # Yield the scraped data for further processing (optional)
        yield {'data': scraped_data}
