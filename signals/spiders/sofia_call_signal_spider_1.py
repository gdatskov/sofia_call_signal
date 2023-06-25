import codecs
import datetime
import json
import os
import random
import shutil
import time
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy_splash import SplashRequest


class SignalSpider(scrapy.Spider):
    name = "signal_spider"
    start_url = "https://call.sofia.bg/bg/Signal/Details/"
    output_directory = "scraped_data"

    # Get the current date and time
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    # Set the output directory path with date and time appended
    output_directory_path = os.path.join(output_directory, formatted_datetime)

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory_path, exist_ok=True)

    def start_requests(self):
        for number in range(339036, 395000):
            url = self.start_url + str(number)
            delay = 2
            yield SplashRequest(url, self.parse, args={'wait': delay}, meta={"number": number})

    def parse(self, response):
        number = response.meta["number"]

        # Extract the signal field from the HTML using XPath
        signal = response.xpath('/html/body/div[2]/div[2]/div[2]/section[1]/div/h3/text()').get()

        # Check if the signal field is empty
        if not signal:
            return  # Skip saving the data and move on to the next number

        # Extract the other fields from the HTML using XPath
        fields = {
            'signal': signal,
            'category': response.xpath(
                '/html/body/div[2]/div[2]/div[2]/section[1]/div/h4/i[1]/following-sibling::text()').get(),
            'sub_category': response.xpath('/html/body/div[2]/div[2]/div[2]/section[1]/div/h4/i[3]/text()').get(),
            'extraction_time': self.formatted_datetime,
            'title': response.xpath("/html/body/div[2]/div[2]/div[2]/section[2]/div[4]/div/h2/text()").get(),
            'description': response.xpath(
                "/html/body/div[2]/div[2]/div[2]/section[2]/div[5]/div[2]/div/p/text()").get(),
            'geolocation': response.xpath(
                "/html/body/div[2]/div[2]/div[2]/section[2]/div[6]/div[2]/div/div[1]/div/text()").get(),
            'address': response.xpath(
                "/html/body/div[2]/div[2]/div[2]/section[2]/div[6]/div[2]/div/div[2]/div/text()").get(),
            'district': response.xpath(
                "/html/body/div[2]/div[2]/div[2]/section[2]/div[6]/div[2]/div/div[3]/div/text()").get(),
            'zone': response.xpath(
                "/html/body/div[2]/div[2]/div[2]/section[2]/div[6]/div[2]/div/div[4]/div/text()").get(),
            'status': response.xpath(
                "/html/body/div[2]/div[2]/div[2]/section[2]/div[8]/div[2]/div[1]/div[1]/text()").get(),
            'user': response.xpath("/html/body/div[2]/div[2]/div[2]/section[2]/div[8]/div[2]/div[2]/div/text()").get(),
        }

        # Clean the fields
        cleaned_fields = {
            'number': number,
            'url': response.url
        }
        for key, value in fields.items():
            cleaned_fields[key] = value.strip().replace('\r', '').replace('\n', '') if value else ""

        # Extract the comment details and descriptions
        comment_rows = response.xpath('//table[@id="comments"]/tbody/tr[td]')
        comment_set = set()
        for row in comment_rows:
            details = row.xpath('.//td[1]/text()').get()
            description = row.xpath('.//td[2]/div/text()').get()

            if details and description:
                comment = (details.strip(), description.strip())
                comment_set.add(comment)

        # Convert the set of comments to a list
        comment_data = []
        for comment in comment_set:
            comment_data.append({
                "number": number,
                "comment_details": comment[0],
                "comment_description": comment[1]
            })

        # Create dictionaries with the extracted and cleaned data
        signal = {key: cleaned_fields[key] for key in ['signal', 'category', 'sub_category', 'extraction_time']}
        data = {key: cleaned_fields[key] for key in ['number', 'url', 'title', 'description']}
        address_data = {key: cleaned_fields[key] for key in
                        ['number', 'title', 'geolocation', 'address', 'district', 'zone', 'url']}
        status_data = {key: cleaned_fields[key] for key in ['number', 'title', 'status', 'user']}

        answers_data = {
            'number': number,
            'answers': []
        }
        history = {
            'number': number,
            'history': []
        }

        answer_rows = response.xpath('//table[@id="clerkAnswers"]/tbody/tr[td]')
        for row in answer_rows:
            documents = row.xpath('.//td[2]/text()').get()
            registration_date = row.xpath('.//td[3]/text()').get()
            registration_number = row.xpath('.//td[4]/text()').get()
            annotation = row.xpath('.//td[5]/text()').get()

            # Exclude the first empty answer
            if documents:
                answer_data = {
                    'documents': documents.strip(),
                    'registration_date': registration_date.strip() if registration_date else "",
                    'registration_number': registration_number.strip() if registration_number else "",
                    'annotation': annotation.strip() if annotation else ""
                }

                answers_data['answers'].append(answer_data)

        answers = {key: answers_data[key] for key in ['number', 'answers']}

        # Extract the history
        history_rows = response.xpath('//*[@id="gview_statushistory"]/div/div/table/tbody/tr[position() > 1]')

        for row in history_rows:
            timestamp_from = row.xpath('.//td[1]/text()').get()
            timestamp_to = row.xpath('.//td[2]/text()').get()
            reason = row.xpath('.//td[3]/text()').get()
            change = row.xpath('.//td[4]/text()').get()

            history_entry = {
                'timestamp_from': timestamp_from.strip() if timestamp_from else "",
                'timestamp_to': timestamp_to.strip() if timestamp_to else "",
                'reason': reason.strip() if reason else "",
                'change': change.strip() if change else ""
            }

            history['history'].append(history_entry)

        # Save the data as JSON files in the output directory
        yield {
            'item': signal,
            'file_name': os.path.join(self.output_directory_path, 'signal.json')
        }
        yield {
            'item': data,
            'file_name': os.path.join(self.output_directory_path, 'data.json')
        }
        yield {
            'item': address_data,
            'file_name': os.path.join(self.output_directory_path, 'address.json')
        }
        yield {
            'item': status_data,
            'file_name': os.path.join(self.output_directory_path, 'status.json')
        }
        yield {
            'item': comment_data,
            'file_name': os.path.join(self.output_directory_path, 'comments.json')
        }
        yield {
            'item': answers,
            'file_name': os.path.join(self.output_directory_path, 'answers.json')
        }
        yield {
            'item': history,
            'file_name': os.path.join(self.output_directory_path, 'history.json')
        }


# # Delete existing JSON files if they exist
# files_to_delete = ['signal.json', 'data.json', 'address.json', 'status.json', 'comments.json']
#
# for file_name in files_to_delete:
#     if os.path.exists(file_name):
#         os.remove(file_name)


# Define the pipeline to write items to JSON files



import json
import codecs

class JsonWriterPipeline:
    def __init__(self, backup_interval=100, backup_time_interval=300):
        self.backup_interval = backup_interval
        self.backup_time_interval = backup_time_interval
        self.processed_items = 0
        self.last_backup_time = time.time()

    def open_spider(self, spider):
        self.files = {}

    def close_spider(self, spider):
        for file in self.files.values():
            file.close()

    def process_item(self, item, spider):
        file_name = item['file_name']
        item_data = item['item']

        if file_name not in self.files:
            self.files[file_name] = codecs.open(file_name, 'w', encoding='utf-8')

        file = self.files[file_name]
        if isinstance(item_data, list):
            for data in item_data:
                json.dump(data, file, ensure_ascii=False)
                file.write('\n')
        else:
            json.dump(item_data, file, ensure_ascii=False)
            file.write('\n')

        self.processed_items += 1

        # Create a backup of the file based on the backup interval or backup time interval
        current_time = time.time()

        if self.processed_items % self.backup_interval == 0 or current_time - self.last_backup_time >= self.backup_time_interval:
            self.last_backup_time = current_time

            # Create the backup directory if it doesn't exist
            os.makedirs("backup", exist_ok=True)

            backup_file_name = os.path.join("backup", os.path.basename(file_name) + '.bak')
            shutil.copyfile(file_name, backup_file_name)

        return item


# Run the spider and export the data to JSON
process = CrawlerProcess(settings={
    'ITEM_PIPELINES': {'__main__.JsonWriterPipeline': 1},
    'DOWNLOADER_MIDDLEWARES': {
        'scrapy_splash.SplashCookiesMiddleware': 723,
        'scrapy_splash.SplashMiddleware': 725,
        'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    },
    'SPIDER_MIDDLEWARES': {
        'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
    },
    'SPLASH_URL': 'http://localhost:8050',
    'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
    'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',
    'CONCURRENT_REQUESTS': 1,  # Limit concurrent requests to 1
    'DOWNLOAD_DELAY': 2,  # Delay between consecutive requests in seconds
    'FEED_EXPORT_ENCODING': 'utf-8'  # Export encoding for JSON files
})

process.crawl(SignalSpider)
process.start()
