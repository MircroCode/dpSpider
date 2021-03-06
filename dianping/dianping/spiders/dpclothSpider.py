# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from dianping.items import DianpingItem
from dianping.items import ShoppingMallItem, ShopsItem
from scrapy import log
from scrapy.http import Request


class DpshopsSpider(CrawlSpider):
    name = 'dpshops'
    allowed_domains = ['dianping.com']
    website = 'http://www.dianping.com'
    start_urls = [
        # 'http://www.dianping.com/search/category/2/20/g119', #北京综合商场
        'http://www.dianping.com/search/category/2/20/g120'  #北京服装鞋帽
    ]

    rules = (
        Rule(LinkExtractor(allow=r'/2/20/g120[p0-9]*'), callback='parse_shop_list', follow=True),
        Rule(LinkExtractor(allow=r'/shop/[0-9]+$'), callback='parse_shop', follow=True)
    )

    def parse_start_url(self, response):
        shop_list_pattern = re.compile("/category/2/20/g120[p0-9]*")
        shop_urls = response.xpath("//@href").extract()
        for url in shop_urls:
            if shop_list_pattern.findall(url):
                yield Request(self.website + url.encode('utf8'), cookies={'cye': 'beijing'},
                              callback=self.parse_shop_list)

    def parse_shop_list(self, response):
        shop_urls = response.xpath('//*[@id="shop-all-list"]/ul/li/div[2]/div[1]/a[1]/@href').extract()
        for url in shop_urls:
            yield Request(self.website + url.encode("utf8"), cookies={'cye': 'beijing'}, callback=self.parse_shop)

    def parse_shop(self, response):
        shop = ShopsItem()
        shop_url = response.url
        shop['shop_name'] = response.xpath('//h1[@class="shop-name"]/text()').extract()
        shop['street_address'] = response.xpath('//span[@itemprop="street-address"]/text()').extract()
        shop['shop_tel'] = response.xpath(
            '//p[@class="expand-info tel"]/span[text()="' + u"电话：" + '"]/..//text()[position()>1]').extract()
        shop['open_time'] = response.xpath(
            '//p[@class="info info-indent"]/span[text()="' + u"营业时间：" + '"]/..//text()[position()>1]').extract()
        shop['shop_tags'] = response.xpath(
            '//p[@class="info info-indent"]/span[text()="' + u"分类标签：" + '"]/..//text()[position()>1]').extract()
        scripts = response.xpath('//script/text()').extract()
        shop['shop_dianping_url'] = [shop_url]
        shop['shop_city'] = response.xpath("//div[@class='breadcrumb']/a[1]/text()").extract()
        shop['shop_district'] = response.xpath("//div[@class='breadcrumb']/a[2]/text()").extract()
        shop['shop_region'] = response.xpath("//div[@class='breadcrumb']/a[3]/text()").extract()
        shop['shop_category'] = response.xpath("//div[@class='breadcrumb']/a[4]/text()").extract()

        pat = re.compile('lng:[0-9.]+,lat:[0-9.]+')
        latAndLngList = [pat.findall(src)[0] for src in scripts if pat.findall(src)]
        latAndLng = latAndLngList[0] if len(latAndLngList) > 0 else ''
        latIdx = latAndLng.find('lat:')
        lat = latAndLng[latIdx + 4:]
        lng = latAndLng[4:latIdx - 1]
        shop['shop_lat'] = [lat]
        shop['shop_lng'] = [lng]
        if lat != '' and lng != '':
            yield shop