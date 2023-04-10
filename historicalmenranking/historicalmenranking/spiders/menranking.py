import scrapy
import json
from datetime import datetime


class MenrankingSpider(scrapy.Spider):
    name = 'menranking'
    allowed_domains = ['fifa.com']
    start_urls = ['https://www.fifa.com/fifa-world-ranking/men?dateId=id13974']

    def parse(self, response):
        script_content = response.xpath('//script[contains(., "dates")]/text()').extract_first()
        date_list = json.loads(script_content)
        date_list = date_list['props']['pageProps']['pageData']['ranking']['dates']
        for item_id in date_list:
            url = f"https://www.fifa.com/api/ranking-overview?locale=en&dateId={item_id['id']}"
            date_text = item_id['text'].replace('Sept', 'sep')
            date_obj = datetime.strptime(date_text, '%d %b %Y')
            date = date_obj.strftime('%Y-%m-%d')
            yield scrapy.Request(url=url, callback=self.parse_ranking_data, meta={'url': url,'date':date})

    def parse_ranking_data(self, response):
        data = json.loads(response.body)
        for ranking_data in data['rankings']:
            yield {
                'url' : response.meta['url'],
                'date': response.meta['date'],
                'team': ranking_data['rankingItem']['name'],
                'rank': ranking_data['rankingItem']['rank'],
                'totalPoints': ranking_data['rankingItem']['totalPoints'],
                'flagUrl': ranking_data['rankingItem']['flag']['src'],
                'conf': ranking_data['tag']['text'] # or id
          }

            
 
            
            



