# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import codecs
import json

class DianpingPipeline(object):
    def __init__(self):
        self.file = codecs.open('DianpingData.json', mode='wb', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(line.decode("unicode_escape"))
        return item
    def open_spider(self,spider):
        print '======================  OPEN SPIDER  ======================='
    def close_spider(self,spider):
        print '======================  CLOSE SPIDER  ======================='


class FileterPipeline(object):
    words_to_filter = ['politics', 'religion']
    def process_item(self, item, spider):
        for word in self.words_to_filter:
            if word in unicode(item['description']).lower():
                raise DropItem("Contains forbidden word: %s" % word)
        else:
            return item
        return item

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            return item

class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open('items.jl', 'wb')

    def process_item(self, item, spider):
        import json
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item