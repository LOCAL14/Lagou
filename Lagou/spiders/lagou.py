# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import FormRequest, Request
from urllib.parse import quote, urlencode
from scrapy.http.cookies import CookieJar
from scrapy.loader import ItemLoader
from Lagou.items import LagouItem
from Lagou.utils.common import get_md5
import json
import time


# from Lagou.email import EmailSender

class LagouSpider(scrapy.Spider):
    # 爬虫启动时间
    start = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    name = 'lagou'
    allowed_domains = ['laogu.com']
    # 主页URL
    homepage = 'https://www.lagou.com/'
    # 职位列表页URL
    position_list_page = 'https://www.lagou.com/jobs/list_{}?'
    # 职位详细信息API
    json_api = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'

    def start_requests(self):
        """
        获取拉勾主页源码
        """
        return [Request(url=self.homepage, callback=self.get_all_position_name, errback=self.error_back)]

    def get_all_position_name(self, response):
        """
        构造所有职位列表页URL
        """
        self.crawler.stats.inc_value("Success_Reqeust")
        if response.status == 200:
            # 获取所有职位名称
            position_name_list = []
            category_list = response.css('.mainNavs .menu_box .menu_main.job_hopping')

            for category in category_list:
                category_name_list = category.css('h3::text').extract()
                position_name_list.extend(category_name_list)
                self.logger.debug('POSITION_NAME_LIST: %s' % str(category_name_list))

            # 构造职位列表页URL
            data = {
                'labelWords': '',
                'fromSearch': 'true',
                'suginput': ''
            }
            position_url_list = [self.position_list_page.format(quote(name)) + urlencode(data) for name in
                                 position_name_list]
            self.logger.debug(position_url_list)

            # 请求职位列表首页获取Cookies
            for position_url in position_url_list:
                for pn in range(0, 4):  # 01234
                    cookiejar = CookieJar()
                    yield Request(url=position_url,
                                  callback=self.get_position_data,
                                  errback=self.error_back,
                                  dont_filter=True,
                                  priority=8,
                                  meta={'kd': position_name_list.pop(0), 'pn': str(pn), 'cookiejar': cookiejar})
                                  # meta={'kd': 'iOS', 'pn': str(pn), 'cookiejar': cookiejar})
                    # 测试仅请求第一页
                    # break
                    self.logger.debug("1 page crawling completed!")

                # 测试仅请求第一个职位
                # break

        else:
            self.logger.error('Something Wrong!')

    # 旧版 Cookies不变化
    def get_all_position_name2(self, response):
        """
        构造所有职位列表页URL
        """
        self.crawler.stats.inc_value("Success_Reqeust")
        if response.status == 200:
            # 获取所有职位名称
            position_name_list = []
            category_list = response.css('.mainNavs .menu_box .menu_main.job_hopping')

            for category in category_list:
                category_name_list = category.css('h3::text').extract()
                position_name_list.extend(category_name_list)
                self.logger.debug('POSITION_NAME_LIST: %s' % str(category_name_list))

            # 构造职位列表页URL
            data = {
                'labelWords': '',
                'fromSearch': 'true',
                'suginput': ''
            }
            position_url_list = [self.position_list_page.format(quote(name)) + urlencode(data) for name in
                                 position_name_list]
            self.logger.debug(position_url_list)

            # 请求职位列表首页获取Cookies
            for position_url in position_url_list:
                cookiejar = CookieJar()
                yield Request(url=position_url,
                              callback=self.get_position_data,
                              errback=self.error_back,
                              dont_filter=True,
                              priority=10,
                              meta={'kd': position_name_list.pop(0), 'cookiejar': cookiejar})
                # 测试仅请求第一个职位
                break
        else:
            self.logger.error('Something Wrong!')

    def get_position_data(self, response):
        """
        获取职位数据
        """
        self.crawler.stats.inc_value("Success_Reqeust")
        if response.status == 200:
            for pn in range(1, 9):
                post_data = {
                    'first': 'true',
                    'pn': str(int(response.meta['pn'])+pn),
                    'kd': response.meta['kd']
                }
                # 测试ProxyIP
                url = 'http://test.abuyun.com/'
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, priority=8)

                yield FormRequest(url=self.json_api,
                                  formdata=post_data,
                                  meta={'cookiejar': response.meta['cookiejar']},
                                  callback=self.parse_datas,
                                  errback=self.error_back,
                                  dont_filter=True,
                                  priority=9)

    # 旧版 Cookies不变化
    def get_position_data2(self, response):
        """
        获取职位数据
        """
        self.crawler.stats.inc_value("Success_Reqeust")
        if response.status == 200:
            for pn in range(1, self.settings.get('MAX_PAGES') + 1):
                post_data = {
                    'first': 'true',
                    'pn': str(pn),
                    'kd': response.meta['kd']
                }
                # 测试ProxyIP
                url = 'http://test.abuyun.com/'
                yield scrapy.Request(url=url, callback=self.parse, dont_filter=True, priority=8)

                yield FormRequest(url=self.json_api,
                                  formdata=post_data,
                                  meta={'cookiejar': response.meta['cookiejar']},
                                  callback=self.parse_datas,
                                  errback=self.error_back,
                                  dont_filter=True,
                                  priority=8)
                # 测试仅获取第一页数据
                # break
            self.logger.debug("50 page crawling completed!")

    def parse(self, response):
        ip = response.xpath('/html/body/table/tr[3]/td/text()').extract_first()
        userAgent = response.xpath('/html/body/table/tr[10]/td/text()').extract_first()
        print('IP: ' + ip)
        print('userAgent: ' + userAgent)
        # print(response.text)

    def parse_datas(self, response):
        """
        获取数据
        """
        # 转换为JSON数据
        datas = json.loads("[{}]".format(response.text))
        base_url = '/'.join(self.position_list_page.split('/')[0:-1])
        try:
            for positioninfo in datas[0]['content']['positionResult']['result']:
                loader = ItemLoader(item=LagouItem(), response=response)
                # 构造职位ID
                loader.add_value('id', get_md5(base_url + '/{}.html'.format(str(positioninfo['positionId']))))
                # 职位详情页URL
                loader.add_value('position_detail_url', base_url + '/{}.html'.format(str(positioninfo['positionId'])))
                # 职位
                loader.add_value('position_name', positioninfo['positionName'])
                # 第一/二/三类型
                loader.add_value('first_type', positioninfo['firstType'])
                loader.add_value('second_type', positioninfo['secondType'])
                loader.add_value('third_type', positioninfo['thirdType'])
                # 发布时间
                loader.add_value('publish_time', positioninfo['createTime'])
                # 薪水
                loader.add_value('salary', positioninfo['salary'])
                loader.add_value('avg_salary', positioninfo['salary'])
                # 工作经验
                loader.add_value('workyear', positioninfo['workYear'])
                # 学历
                loader.add_value('education', positioninfo['education'])
                # 类型（全职/兼职）
                loader.add_value('job_nature', positioninfo['jobNature'])
                # 职位优势
                loader.add_value('position_advantage', positioninfo['positionAdvantage'])
                # 工作城市
                loader.add_value('city', positioninfo['city'])
                # 工作城区
                loader.add_value('district', positioninfo['district'])
                # 纬度
                loader.add_value('latitude', positioninfo['latitude'])
                # 经度
                loader.add_value('longitude', positioninfo['longitude'])
                # 招聘公司
                loader.add_value('company_fullname', positioninfo['companyFullName'])
                # 公司详情页URL
                loader.add_value('company_url',
                                 'https://www.lagou.com/gongsi/{}.html'.format(str(positioninfo['companyId'])))
                # 公司图标URL
                loader.add_value('company_logo_url',
                                 'https://www.lgstatic.com/thumbnail_120x120/{}'.format(
                                     str(positioninfo['companyLogo'])))

                # 公司领域
                loader.add_value('company_field', positioninfo['industryField'])
                # 公司规模
                loader.add_value('company_size', positioninfo['companySize'])
                # 公司标签（JSON array）
                if positioninfo['companyLabelList']:
                    loader.add_value('company_label_list', positioninfo['companyLabelList'])
                else:
                    loader.add_value('company_label_list', 'NULL')
                # 知名公司标记 （1-知名）
                loader.add_value('company_famous', positioninfo['famousCompany'])

                yield loader.load_item()
            self.crawler.stats.inc_value("Success_Reqeust")
        except Exception as e:
            self.logger.debug("GET ERROR: {}".format(e))
            self.crawler.stats.inc_value('Failed_Request')

    def error_back(self, failure):
        """
        错误回调
        """
        self.logger.error("Error: %s" % str(failure.args))
        self.crawler.stats.inc_value('Failed_Request')

    def close(self, reason):
        """
        爬虫关闭发送通知邮件
        """
        # email = EmailSender()
        spider_name = self.settings.get('BOT_NAME')
        start_time = self.start
        success_request = self.crawler.stats.get_value("Success_Reqeust")
        failed_request = self.crawler.stats.get_value("Failed_Request")
        # 若没有失败的请求则默认为0
        if failed_request == None:
            failed_request = 0
        insert_into_success = self.crawler.stats.get_value("Success_Inserted_DB")
        failed_db = self.crawler.stats.get_value("Failed_Insert_DB")
        # 若没有插入失败的数据则默认为0
        if failed_db == None:
            failed_db = 0
        fnished_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        body = "爬虫名称：{}\n\n 开始时间：{}\n\n 请求成功总量：{}\n 请求失败总量：{}\n\n 数据库存储总量：{}\n 数据库存储失败总量：{}\n\n 结束时间  : {}\n".format(
            spider_name,
            start_time,
            success_request,
            failed_request,
            insert_into_success,
            failed_db,
            fnished_time
        )
        # try:
        #     email.sendEmail(self.settings.get('RECEIVE_LIST'), subject=self.settings.get('SUBJECT'), body=body)
        # except:
        #     pass
