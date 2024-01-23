import scrapy
import json

class FlipkartSpider(scrapy.Spider):
    name = 'flipkart'
    allowed_domains = ['flipkart.com']

    def start_requests(self):
        product_name = getattr(self, 'product_name', 'realme')
        # product_category = getattr(self, 'product_category', 'aps')

        url = f'https://www.flipkart.com/search?q={product_name}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        scraped_data = []

        for product in response.css('div.s-result-item'):
            item = {
                'title': product.css('div._4rR01T::text').get(default=''),
                'price': product.css('div._30jeq3::text').get(default=''),
                'image_link': product.css('div.CXW8mj img._396cs4::attr(src)').get(default=''),
               'link_to_product': product.css('a.s1Q9rs::attr(href)').get(default=''),
            }
            scraped_data.append(item)

        # Save the scraped data to output.json
        with open('output2.json', 'w', encoding='utf-8') as json_file:
            json.dump({'data': scraped_data}, json_file, ensure_ascii=False, indent=2)

        # Yield the scraped data for further processing (optional)
        yield {'data': scraped_data}
