# pipelines.py
import mysql.connector
from datetime import datetime

class CommodityPipeline:
    def __init__(self):
        self.db_connection = None
        self.db_cursor = None

    def open_spider(self, spider):
        # Establish a connection to the MySQL database
        self.db_connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='finavulq_continentl'
        )
        self.db_cursor = self.db_connection.cursor()

    def process_item(self, item, spider):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # date_obj = datetime.strptime(item['date'], "%m/%d/%Y")
        # formatted_date = date_obj.strftime("%Y-%m-%d")

        # Check if the record exists based on the name
        self.db_cursor.execute("""
            SELECT id FROM commodities_exchange_rates
            WHERE name = %s
        """, (item['name'],))
        result = self.db_cursor.fetchone()

        if result:
            # Update the existing record
            self.db_cursor.execute("""
                UPDATE commodities_exchange_rates
                SET price = %s, unit = %s, date = %s, updated_at = %s
                WHERE id = %s
            """, (item['price'], item['unit'], item['date'], now, result[0]))
        else:
            # Insert a new record
            self.db_cursor.execute("""
                INSERT INTO commodities_exchange_rates (name, price, unit, date, updated_at)
                VALUES (%s, %s, %s, %s, %s)
            """, (item['name'], item['price'], item['unit'], item['date'], now))
        
        self.db_connection.commit()
        return item

    def close_spider(self, spider):
        # Close the database connection
        self.db_cursor.close()
        self.db_connection.close()
