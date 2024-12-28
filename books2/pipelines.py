# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from itemadapter import ItemAdapter
import mysql.connector
import sqlite3
import re
from scrapy.pipelines.images import ImagesPipeline

class Books2Pipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        image_name = re.search(r'cache/(\S*/\S*)/',item.get("image_url")).group(1).replace('/','')
        return f"{image_name}.jpg"



# class JsonWriterPipeline:
#     def open_spider(self, spider):
#         self.file = open("items.json", "w")
#     def close_spider(self, spider):
#         self.file.close()
#     def process_item(self, item, spider):
#         line = json.dumps(ItemAdapter(item).asdict(),ensure_ascii=False)
#         self.file.write(f"{line}\n")
#         return item



class SqliteDemoPipeline:

    def __init__(self):

        ## Create/Connect to database
        self.con = sqlite3.connect(r'/home/percy/Documents/demo.db')

        ## Create cursor, used to execute commands
        self.cur = self.con.cursor()
        
        # self.cur.execute("""DROP TABLE book""")
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS book(
            title TEXT,
            price TEXT,
            rating TEXT,
            image_url TEXT
        )
        """)


    def process_item(self, item, spider):
        ## Check to see if text is already in database 
        self.cur.execute("select * from book where title = ?", (item['title'],))
        result = self.cur.fetchone()

        ## If it is in DB, create log message
        if result:
            spider.logger.warn("Item already in database: %s" % item['title'])
        
        ## If text isn't in the DB, insert data
        else:
        ## Define insert statement
            self.cur.execute("""
                INSERT INTO book (title, price, rating, image_url ) VALUES (?, ?, ?, ?)
            """,
            (
                item['title'],
                item['price'],
                item['rating'],
                item["image_url"]
            ))

            ## Execute insert of data into database
            self.con.commit()
        return item


class MysqlDemoPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'percy',
            password = 'Percy!?2961',
            database = 'books'
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()

        self.cur.execute("""DROP table book""")
        ## Create quotes table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS book(
            title text,
            price text,
            rating text,
            image_url VARCHAR(255)
        )
        """)


    def process_item(self, item, spider):
        ## Check to see if text is already in database 
        self.cur.execute("select * from book where title = %s", (item['title'],))
        result = self.cur.fetchone()

        ## If it is in DB, create log message
        if result:
            spider.logger.warn("Item already in database: %s" % item['title'])
        else:
            ## Define insert statement
            self.cur.execute(""" insert into book (title, price, rating, image_url) values (%s,%s,%s,%s)""", (
                item["title"],
                item["price"],
                item["rating"],
                item["image_url"]
            ))

            ## Execute insert of data into database
            self.conn.commit()
        return item

    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()



