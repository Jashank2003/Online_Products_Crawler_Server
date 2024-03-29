const express = require('express');
const cors = require('cors');
const { spawn , exec } = require('child_process');
const bodyParser = require('body-parser');
const fs = require('fs');

const app = express();
const PORT = 5000;

app.use(bodyParser.json());
app.use(cors());

//  AMAZON SCRAPER AND RESPONSE
app.post('/api/home/amazon', (req, res) => {
  const { product_name, product_category } = req.body;
  console.log("The product name is ", product_name);

  const spider = spawn('scrapy', [
    'runspider',
    './scrapers/spiders/amazon_spider.py',
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
        res.json({ data: filteredData, message: 'Scraping completed1!' });
      } catch (error) {
        console.error('Error reading output.json1:', error);
        res.status(500).json({ message: 'Error reading output.json1' });
      }
    } else {
      res.status(500).json({ message: `Spider process closed with code1: ${code}` });
    }
  });
});

//  FLIPKART SCRAPER AND RESPONSE

app.post('/api/home/flipkart', (req, res) => {
  const { product_name, product_category } = req.body;
  console.log("The product name is ", product_name);

  // Execute the Python script using the python command
  const command = `python ./flipkart_scraper.py ${product_name}`;
  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing command: ${error.message}`);
      res.status(500).json({ message: `Error executing command: ${error.message}` });
      return;
    }
    if (stderr) {
      console.error(`Command stderr: ${stderr}`);
      res.status(500).json({ message: `Command stderr: ${stderr}` });
      return;
    }

    console.log(`Command stdout: ${stdout}`);

    // Read the contents of output.json and filter out empty values
    try {
      const jsonData = JSON.parse(fs.readFileSync('./output2.json', 'utf-8'));
      const filteredData = jsonData.data.filter(item => item.title !== '' && item.price !== '' && item.image_link !== '' && item.link_to_product !== '');
      res.json({ data: filteredData, message: 'Scraping completed2!' });
    } catch (error) {
      console.error('Error reading output.json:', error);
      res.status(500).json({ message: 'Error reading output.json' });
    }
  });
});


app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
