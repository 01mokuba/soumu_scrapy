# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from soumu_scrapy.items import ArchiveItem, ClipItem

class ArchiveSpider(CrawlSpider):
    name = 'archive'
    allowed_domains = ['www.soumu.go.jp'] #対象ドメイン
    start_urls = ['http://www.soumu.go.jp/menu_news/s-news/index.html'] #開始URL
    custom_settings = {
        'DOWNLOAD_DELAY' : 1,
    }
    rules = (
        Rule(
                LinkExtractor(
                    allow=['http://www.soumu.go.jp/menu_news/s-news/[\d]+m\.html'], #リンク抽出をするURL - 月ごとの報道資料一覧
                    restrict_xpaths=['//div[@class=\'contentsBody\']'] #リンク抽出をするエリア
                ), 
                callback='parse_archive_list', #リンク抽出後に実行されるコールバック
                follow=True
            ),
        Rule(
                LinkExtractor(
                    allow=['http://www.soumu.go.jp/menu_news/s-news/[\d\w]+\.html'], #リンク抽出をするURL - 報道資料詳細
                    restrict_xpaths=['//div[@class=\'contentsBody\']'] #リンク抽出をするエリア
                ), 
                callback='parse_archive_detail', #リンク抽出後に実行されるコールバック
                follow=True
            )
    )

    def parse_archive_list(self, response):
        item = ArchiveItem()
        item['links'] = []
        item['month'] = response.url.split('/')[-1].replace('m.html','') #抽出した月 例: 1809
        for linkitem in response.xpath('//div[@class=\"contentsBody\"]//a'): # メインコンテンツ内のリンクのリストでループ
            item['links'].append({
                'href' : linkitem.xpath('@href').extract_first(), #URLを抽出
                'text' : linkitem.xpath('text()').extract_first() #アンカーテキストを抽出
            })
        return item

    def parse_archive_detail(self, response):
        item = ClipItem()
        item['src'] = response.xpath('//body').extract_first()
        content_root = response.xpath('//div[@class=\'contentsBody\']')
        item['text'] = content_root.extract_first()
        item['attachments'] = []
        item['file_urls'] = []
        for d in response.xpath('//a'): #responseのaタグでループ
            dd = d.xpath('@href').extract_first() #hrefの値を抽出
            if dd is not None:  #hrefの値が存在する場合
                if re.match('^https?://', dd) is None: #URLにhttp[s]が含まれていない場合
                    dd = response.urljoin(dd) #responseのベースURLを組み合わせて完全なURLを作る
                if re.match('.*\.[Pp][Dd][Ff]$', dd) is not None: #大文字/小文字のPDF/pdfがURL内に存在するとき
                    item['attachments'].append({  
                        'href': dd,
                        'text': d.xpath('text()').extract_first()
                    })
                    item['file_urls'].append(dd)
        return item
