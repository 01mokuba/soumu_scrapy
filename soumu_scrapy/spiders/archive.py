# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from soumu_scrapy.items import ArchiveItem, ClipItem

class ArchiveSpider(CrawlSpider):
    name = 'archive'
    allowed_domains = ['www.soumu.go.jp']
    start_urls = ['http://www.soumu.go.jp/menu_news/s-news/index.html']
    custom_settings = {
        'DOWNLOAD_DELAY' : 1,
    }
    rules = (
        Rule(LinkExtractor(
                allow=['http://www.soumu.go.jp/menu_news/s-news/[\d]+m\.html'],
                restrict_xpaths=['//div[@class=\'contentsBody\']']
            ), callback='parse_archive_list', follow=True),
    )

    def parse_archive_list(self, response):
        item = ArchiveItem()
        item['links'] = []
        item['month'] = response.url.split('/')[-1].replace('m.html','')
        for linkitem in response.xpath('//div[@class=\"contentsBody\"]//a'):
            item['links'].append({
                'href' : linkitem.xpath('@href').extract_first(),
                'text' : linkitem.xpath('text()').extract_first()
            })

        return item