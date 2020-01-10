# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader.processors import TakeFirst, Join, MapCompose
from Lagou.utils.common import get_avg_salary
from Lagou.utils.common import bool_to_int
from Lagou.utils.common import workyear_filter
from Lagou.utils.common import education_filter
from Lagou.utils.common import company_size_filter
from Lagou.utils.common import job_nature_filter


class LagouItem(Item):
    table = 'position'
    id = Field(input_processor=Join())
    position_detail_url = Field(input_processor=Join())
    position_name = Field(input_processor=Join())
    first_type = Field(input_processor=Join())  # 新添加
    second_type = Field(input_processor=Join())  # 新添加
    third_type = Field(input_processor=Join())  # 新添加
    publish_time = Field(input_processor=Join())
    salary = Field(input_processor=Join())
    avg_salary = Field(input_processor=MapCompose(get_avg_salary))
    workyear = Field(input_processor=MapCompose(workyear_filter))
    education = Field(input_processor=MapCompose(education_filter))
    job_nature = Field(input_processor=MapCompose(job_nature_filter))
    position_advantage = Field(input_processor=Join())
    city = Field(input_processor=Join())
    district = Field(input_processor=Join())  # 新添加
    latitude = Field(input_processor=Join())  # 新添加
    longitude = Field(input_processor=Join())  # 新添加
    company_fullname = Field(input_processor=Join())
    company_url = Field(input_processor=Join())
    company_logo_url = Field(input_processor=Join())
    company_field = Field(input_processor=Join())  # 新添加
    company_size = Field(input_processor=MapCompose(company_size_filter))  # 新添加
    company_label_list = Field(input_processor=Join())  # 新添加
    company_famous = Field(input_processor=MapCompose(bool_to_int))  # 新添加 1/0
