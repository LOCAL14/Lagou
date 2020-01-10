# -*- coding: utf-8 -*-

from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from fake_useragent import UserAgent
import base64

class RandomUAMiddleware(object):

    def process_request(self, request, spider):

        request.headers['User-Agent'] = UserAgent().random

class ProxyMiddleware(object):
    # 阿布云 Proxy
    # def __init__(self, proxy_server, proxy_user, proxy_pass):
    #     self.proxy_server = proxy_server
    #     self.proxy_user = proxy_user
    #     self.proxy_pass = proxy_pass
    #     self.proxy_auth = "Basic " + base64.urlsafe_b64encode(bytes((self.proxy_user + ":" + self.proxy_pass), "ascii")).decode("utf8")
    #
    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(
    #         proxy_server = crawler.settings.get('PROXY_SERVER'),
    #         proxy_user = crawler.settings.get('PROXY_USER'),
    #         proxy_pass = crawler.settings.get('PROXY_PASS')
    #     )
    #
    # def process_request(self, request, spider):
    #     request.meta["proxy"] = self.proxy_server
    #     request.headers["Proxy-Authorization"] = self.proxy_auth

    # 蜻蜓Proxy
    def process_request(self, request, spider):
        proxyUser = "O0G71654325870702114"
        proxyPass = "BPg09arvAf9D7yNT"
        proxyHost = "dyn.horocn.com"
        proxyPort = "50000"

        request.meta['proxy'] = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }



    def process_response(self, request, response, spider):
        return response

class DownloadRetryMiddleware(RetryMiddleware):
    def process_response(self, request, response, spider):
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            return self._retry(request, exception, spider)