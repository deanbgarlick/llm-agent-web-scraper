## What is this repo

This repo is provides MVP LLM agent web scraper functionality. The user in main.py instantiates:
- an LLM agent with access to a search, scrape and update data point tool
- data points that they would like the agent to search for
- a data point persistance object

The LLM agent then performs web search and scraping using the firecrawl API and calls to the OpenAI LLM to parse the scraped data.


## How to run this repo

To run this program
1. install the requirements in requirements.txt
2. add your openai key in .env
3. run python -m app

