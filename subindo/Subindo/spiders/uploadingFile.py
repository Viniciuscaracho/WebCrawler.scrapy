import os
from supabase import create_client, Client
from crawling2_spider import CrawlingSpider
import csv

url = "https://hkpumefttptiqeirzjia.supabase.co/rest/v1/jogadores-nba?some_column=eq.someValue"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhrcHVtZWZ0dHB0aXFlaXJ6amlhIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODcyOTM0NDAsImV4cCI6MjAwMjg2OTQ0MH0.BdoqtrQjJjpTmkPSgSHIli1nnbD4L0mzQ4z-JgakGhU"
supabase: Client = create_client(url, key)


def upload(filename, table_name):
    with open(filename, "r") as file:
        csv_data = csv.DictReader(file)
        for row in csv_data:
           supabase.table(table_name).insert(row).execute()

csv_file = 'file.csv'
table_name = 'jogadores-nba'

upload(csv_file, table_name)

if __name__ == '__main__':
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess()
    process.crawl(CrawlingSpider)
    process.start()