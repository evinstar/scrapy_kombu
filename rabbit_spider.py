import datetime
import json
import re
import time
from typing import Dict

from kombu.transport.pyamqp import Channel
from parsel import Selector
from scrapy import signals, Spider, Request
from scrapy.exceptions import DontCloseSpider
from scrapy.settings import Settings
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError

from .constants import DELIVERY_TAG, URL
from .message import KombuConnection


class Utils:
    @staticmethod
    def strip(data: Dict):
        for k, v in data.items():
            if v and isinstance(v, str):
                data[k] = v.strip()
        return data

    @staticmethod
    def extract(selector: Selector, rule, method='css', first=False):
        if method not in ('css', 'xpath'):
            raise ValueError('method should be css or xpath')

        extract_results = getattr(selector, method)(rule).extract()
        results = []
        for mid_result in extract_results:
            mid_result = mid_result.strip()
            if mid_result:
                results.append(mid_result)

        if first:
            return results and results[0]
        return results

    def package_item(self, item, meta=None):
        data = {}
        if isinstance(item, dict):
            if 'type' not in item.keys():
                data['data'] = [item]
            else:
                data.update(item)
        else:
            data['data'] = item
        if 'type' not in data.keys():
            data['type'] = self.name
        if 'crawledTime' not in data.keys():
            data['crawledTime'] = str(datetime.datetime.now())[:19]
        if 'meta' not in data.keys() and meta:
            data['meta'] = meta
        meta = self.clean_meta(data.get('meta'))
        data['meta'] = meta
        return data

    @staticmethod
    def clean_meta(meta: dict):
        new_meta = {**meta}
        for k in ['delivery_tag', 'download_timeout', 'proxy', 'download_slot', 'download_latency', 'retry_times', 'depth']:
            if k in new_meta:
                new_meta.pop(k)
        return new_meta

    @staticmethod
    def extract_meta(response):
        keywords = None
        description = None
        for meta in response.xpath('//meta'):
            for k, v in meta.attrib.items():
                if v.lower() == 'keywords':
                    keywords = meta.attrib.get('content')
                if v.lower() == 'description':
                    description = meta.attrib.get('content')
        return keywords, description

    @staticmethod
    def filter_item(entity):
        """
        得到带有标签的文本内容
        """
        content = entity
        content = re.sub(r'<script.+?</script>', '', content, flags=re.S)  # 删除文章中的js代码
        content = re.sub(r'<style.+?</style>', '', content, flags=re.S)  # 删除文章中的css代码
        content = re.sub(r'(?<=<)[iI][Mm][Gg]', 'img', content)  # 把img标签统一
        content = re.sub(r'P(?=>)', 'p', content)
        # print(2,self.content)
        content = re.sub(r'<div.*?>', '<div>', content)  # 把div前标签的属性统统删除
        content = re.sub(r'<(?!/?(p|img|br|div|hr|spilt|strong|h1|h2|h3|h4|h5|h6)).*?>', '', content)  # 删除除了这些标签外的所有标签
        content = re.sub(r'<p.*?>', '<p>', content)  # 同上
        content = re.sub(r'✎ ', '', content)  # 删除不需要的字符
        content = re.sub(r'&[a-zA-Z]{3,7};|▲|▽|(?<=<p>)\s+?(?!\s)', '', content)  # 删除不需要的标签
        content = re.sub(r'\u3000+?', '', content)  # 删除不需要的标签
        content = re.sub(r'\xa0+?', '', content)  # 删除不需要的标签
        content = re.sub(r'<p><br></p>', '', content)  # 删除不需要的标签
        content = re.sub(r'<p><br/></p>', '', content)  # 删除不需要的标签
        content = re.sub(r'<p>\r\n<br>\r\n</p>', '', content)  # 删除不需要的标签
        content = re.sub(r'&nbsp;&nbsp;', '', content)  # 删除不需要的标签
        plain_text = re.sub(r'<.+?>', '', content)
        return plain_text

    @staticmethod
    def extract_json(text):
        brackets = []
        in_str = False
        start = None
        for i, char in enumerate(text):
            if char == '"':
                in_str = not in_str
            if not in_str:
                if char == "{":
                    if start is None:
                        start = i
                    brackets.append(char)
                if char == "}":
                    brackets.pop()
            if not brackets:
                result = text[start:i + 1]
                data = json.loads(result)
                return data


class RabbitMixin:
    max_idle_time = 30
    no_ack = False

    def init(self):
        settings = self.settings
        self.concurrent_requests = max(int(settings.get('CONCURRENT_REQUESTS') / 2), 1)
        self.connection = KombuConnection(settings.get('MQ_PARAMETERS'))
        self.channel: Channel = None
        queue_name = settings.get('MQ_QUEUE')
        self.queue_name = queue_name
        self.get_channel(self.settings)

    def get_channel(self, reacquire=False):
        if self.channel and reacquire:
            try:
                self.channel.close()
            except Exception as e:
                self.logger.warning(f'try close channel failed for {e}')
            finally:
                self.channel = None
        if self.channel:
            return self.channel
        settings = self.settings
        exchange_name = settings.get('MQ_EXCHANGE')
        queue_name = settings.get('MQ_QUEUE')
        routing_key = settings.get('MQ_ROUTING_KEY')
        self.channel: Channel = self.connection.acquire()
        self.channel.exchange_declare(exchange_name, 'direct', durable=True, auto_delete=False)
        self.channel.queue_declare(queue_name, durable=True, auto_delete=False)
        self.channel.queue_bind(queue_name, exchange_name, routing_key)
        return self.channel

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        for k in ('_job', '_version'):
            if k in kwargs:
                kwargs.pop(k)
        obj = super(RabbitMixin, cls).from_crawler(crawler, *args, **kwargs)
        obj.init()
        crawler.signals.connect(obj.spider_idle, signal=signals.spider_idle)
        return obj

    def schedule_next_requests(self):
        """Schedules a request if available"""
        for req in self.next_requests():
            self.crawler.engine.crawl(req, self)

    def make_request_from_data(self, data) -> Request:
        url = data.get(URL)
        if url:
            return Request(
                url,
                meta=data,
                errback=self.errback,
                dont_filter=True
            )

    def next_requests(self):
        has_message = True
        for i in range(self.concurrent_requests):
            try:
                msg = self.get_channel().basic_get(self.queue_name, no_ack=self.no_ack)
                if msg:
                    message = msg.body
                    message = message.encode('utf-8').decode("unicode_escape")
                    self.logger.info(message)
                    data = json.loads(message)
                    # _url = data.get('url')
                    data[DELIVERY_TAG] = msg.delivery_tag
                    _request = None
                    try:
                        _request = self.make_request_from_data(data)
                    except Exception as e:
                        self.logger.warning(f'make request error for {e}, from {data}')
                    if _request:
                        yield _request
                    else:
                        self.ack(msg.delivery_tag)
                else:
                    has_message = False
                    break
            except (BrokenPipeError, ConnectionResetError, TimeoutError):
                self.logger.warning(f'Broken pipe error')
                self.get_channel(reacquire=True)
            except Exception as e:
                self.logger.exception(f'next request error for {e}')
        if not has_message:
            time.sleep(5)

    @classmethod
    def update_settings(cls, settings: Settings):  # 更新中间件配置到custom_settings中
        for k, v in cls.custom_settings.items():
            if isinstance(v, dict):
                old_v = settings.getdict(k, {})
                old_v.update(v)
                settings.set(k, old_v, priority='spider')
            else:
                settings.set(k, v)
        # settings.setdict(cls.custom_settings or {}, priority='spider')

    def spider_idle(self):
        self.spider_idle_start_time = int(time.time())
        self.schedule_next_requests()
        idle_time = int(time.time()) - self.spider_idle_start_time
        # if self.max_idle_time != 0 and idle_time >= self.max_idle_time:
        #     return
        raise DontCloseSpider

    def start_requests(self):
        for req in self.next_requests():
            yield req

    def ack(self, delivery_tag):
        try:
            self.get_channel().basic_ack(delivery_tag)
            self.logger.info(f'ack message {delivery_tag}')
        except (BrokenPipeError, ConnectionResetError, TimeoutError):
            self.logger.warning(f'Broken pipe error')
            self.get_channel(reacquire=True)

    def reject(self, delivery_tag):
        try:
            self.get_channel().basic_reject(delivery_tag, True)
            self.logger.warning(f'reject message {delivery_tag}')
        except (BrokenPipeError, ConnectionResetError, TimeoutError):
            self.logger.warning(f'Broken pipe error')
            self.get_channel(reacquire=True)


class RabbitSpider(RabbitMixin, Spider, Utils):
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        obj = super(RabbitSpider, cls).from_crawler(crawler, *args, **kwargs)
        obj._set_crawler(crawler)
        return obj

    # spider = cls(*args, **kwargs)
    # spider._set_crawler(crawler)
    # return spider
    def errback(self, failure):
        _request = failure.request
        delivery_tag = _request.meta.get(DELIVERY_TAG)
        if isinstance(failure.value, (DNSLookupError, HttpError)):
            self.ack(delivery_tag)
        else:
            self.logger.warning(f'{type(failure.value)}, {failure.value}')
            self.reject(delivery_tag)
