import mysql.connector
import os
from dotenv import load_dotenv

class MysqlPipeline:

    def __init__(self):
        load_dotenv() 
        self.conn = mysql.connector.connect(
            host = os.getenv('HOST'),
            user = os.getenv('USER'),
            password = os.getenv('PASSWORD'),
            database = os.getenv('DATABASE')
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



