import pymongo
from sqlalchemy.orm import sessionmaker
from models import Items, db_connect, create_items_table


# from scrapy.conf import settings

class Pipeline(object):
    def __init__(self):
        # connection = pymongo.MongoClient(
        #     settings['MONGODB_SERVER'],
        #     settings['MONGODB_PORT']
        # )
        # db = connection[settings['MONGODB_DB']]
        # self.collection = db[settings['MONGODB_COLLECTION']]

        engine = db_connect()
        create_items_table(engine)
        self.Session = sessionmaker(bind=engine)

    # def process_item(self, item, spider):
    #     # self.collection.insert(dict(item))
    #     item2 = dict(item)
    #     self.collection.insert_one(item2)
    #     return item

    def process_item(self, item, spider):
        session = self.Session()
        new_item = Items(**item)
        try:
            session.add(new_item)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return item
