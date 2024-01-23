from flask import Flask, request, jsonify
from flask_cors import CORS
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
import threading

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.in']

    def start_requests(self):
        product_name = getattr(self, 'product_name', 'realme')
        product_category = getattr(self, 'product_category', 'aps')

        url = f'https://www.amazon.in/s?k={product_name}&crid={product_category}&ref=nb_sb_noss_2'

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for product in response.css('div.s-result-item'):
            yield {
                'title': product.css('span.a-size-medium.a-color-base.a-text-normal::text').get(),
                'price': product.css('span.a-price-whole::text').get(),
                'image_link': product.css('img.s-image::attr(src)').get(),
            }

@app.route('/api/home/amazon', methods=['POST'])
def scrape_amazon():
    data = request.get_json()

    if data and 'product_name' in data and 'product_category' in data:
        product_name = data['product_name']
        product_category = data['product_category']
        print(f"Received request with product_name: {product_name}, product_category: {product_category}")

        # Run the Scrapy spider with the provided parameters
        process = CrawlerProcess()
        scraped_data = []

        def spider_results(item):
            scraped_data.append(item)

        process.crawl(AmazonSpider, product_name=product_name, product_category=product_category)
        process.crawler.signals.connect(spider_results, signal=scrapy.signals.item_scraped)
        process.start()

        return jsonify({'data': scraped_data, 'message': 'Data scraped successfully'})

    return jsonify({'error': 'Invalid data format'}), 400

if __name__ == '__main__':
    app.run(debug=True)
