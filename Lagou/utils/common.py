# -*- coding:utf-8 -*-

import hashlib
import math


def get_md5(url):
    # md5
    if isinstance(url, str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def get_avg_salary(value):
    a, b = value.replace('k', '').split('-')
    return str(math.ceil((int(a) + int(b)) / 2))


def bool_to_int(value):
    if value:
        return '1'
    else:
        return '0'


def workyear_filter(value):
    workyear_dict = {'不要求': '1',
                     '不限': '1',
                     '应届毕业生': '2',
                     '1-3年': '3',
                     '3年以下': '3',
                     '3-5年': '4',
                     '5-10年': '5',
                     '10年以上': '6'}
    if value in workyear_dict:
        return workyear_dict[value]
    else:
        return '0'


def education_filter(value):
    education_dict = {'不要求': '1',
                      '不限': '1',
                      '大专': '2',
                      '本科': '3',
                      '硕士': '3',
                      '博士': '4'}
    if value in education_dict:
        return education_dict[value]
    else:
        return '0'


def company_size_filter(value):
    company_size_dict = {'少于15人': '1',
                         '15-50人': '2',
                         '50-150人': '3',
                         '150-500人': '3',
                         '500-2000人': '4',
                         '2000人以上': '5'}
    if value in company_size_dict:
        return company_size_dict[value]
    else:
        return '0'


def job_nature_filter(value):
    job_nature_dict = {'全职': '1',
                       '兼职': '2',
                       '实习': '3'}
    if value in job_nature_dict:
        return job_nature_dict[value]
    else:
        return '0'





if __name__ == '__main__':
    pass
