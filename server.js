const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const bodyParser = require('body-parser');
const fs = require('fs');

const app = express();
const PORT = 5000;

app.use(bodyParser.json());
app.use(cors());

app.post('/api/home/amazon', (req, res) => {
  const { product_name, product_category } = req.body;
  console.log("The product name is ", product_name);

  const spider = spawn('scrapy', [
    'runspider',
    './amazon_scraper/spiders/amazon_spider.py',
    '-a',
    `product_name=${product_name}`,
    '-a',
    `product_category=${product_category}`,
  ]);

  spider.stdout.on('data', (data) => {
    // Do nothing or handle the spider output if needed
  });

  spider.on('close', (code) => {
    console.log(`Spider process closed with code ${code}`);

    if (code === 0) {
      try {
        // Read the contents of output.json and filter out empty values
        const jsonData = JSON.parse(fs.readFileSync('./output.json', 'utf-8'));
        const filteredData = jsonData.data.filter(item => item.title !== '' && item.price !== '' && item.image_link !== '' && item.link_to_product !== '');
        res.json({ data: filteredData, message: 'Scraping completed!' });
      } catch (error) {
        console.error('Error reading output.json:', error);
        res.status(500).json({ message: 'Error reading output.json' });
      }
    } else {
      res.status(500).json({ message: `Spider process closed with code ${code}` });
    }
  });
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
