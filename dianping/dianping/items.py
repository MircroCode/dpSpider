# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class DianpingItem(Item):
    # define the fields for your item here like:
    # name = Field()
    shop_name = Field()
    street_address = Field()
    shop_tel = Field()
    open_time = Field()
    shop_tag = Field()
    shop_lat = Field()
    shop_lng = Field()
