#!/usr/local/bin python
import pymysql.cursors
import os


class DataBase():
    def __init__(self):
        try:
            self.connection = pymysql.connect(
                host=os.getenv('MYSQL_HOST'),
                user=os.getenv('MYSQL_USER'),
                password=os.getenv('MYSQL_PASSWORD'),
                database=os.getenv('MYSQL_DATABASE'),
                cursorclass=pymysql.cursors.DictCursor
            )      
        except Exception as error:
            raise(error)
    
    def get_connection(self):
        return self.connection
