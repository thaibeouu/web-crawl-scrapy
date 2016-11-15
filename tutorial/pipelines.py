import pymongo

from scrapy.conf import settings

class CurrencyPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        # connection = pymongo.MongoClient('localhost', 27017)
        # db = connection.resultsScrapy
        # collection = db.questions
        # self.collection = collection


    def process_item(self, item, spider):
        # self.collection.insert(dict(item))
        item2 = dict(item)
        self.collection.insert_one(item2)
        return item
