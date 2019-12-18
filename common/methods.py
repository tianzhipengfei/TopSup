# -*- coding: utf-8 -*-

# @Author  : Skye
# @Time    : 2018/1/9 10:39
# @desc    :

import requests
import webbrowser
import urllib.parse
import time
from queue import Queue

# # 颜色兼容Win 10
from colorama import init,Fore
init()

def open_webbrowser(question):
    webbrowser.open('https://baidu.com/s?wd=' + urllib.parse.quote(question))

def open_webbrowser_count(question,choices):
    print('\n-- 方法2： 题目+选项搜索结果计数法 --')

    not_words = ['不是', '不可能', '不属于']
    not_flag = False
    for not_word in not_words:
        if not_flag == False and not_word in question:
            not_flag = True
            break
    if not_flag:
        print(Fore.YELLOW + "\n!!**请注意此题为否定题,选计数最少的**!!\n" + Fore.RESET)

    kv = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
    counts = []
    baidu_url = 'https://www.baidu.com/s?wd='
    choices_q = Queue()
    for choice in choices:
        choices_q.put(baidu_url+question+choice)

    t = time.perf_counter()
    while choices_q.empty() != True:
        url = choices_q.get()
        req = requests.get(url=url, headers=kv)
        r = req.content
        content = str(r, encoding='utf-8', errors='ignore')
        index = content.find('百度为您找到相关结果约') + 11
        content = content[index:]
        index = content.find('个')
        count = content[:index].replace(',', '')
        counts.append(count)
    output(choices, counts)

def count_base(question,choices):
    print('\n-- 方法3： 题目搜索结果包含选项词频计数法 --')

    not_words = ['不是', '不可能', '不属于']
    not_flag = False
    for not_word in not_words:
        if not_flag == False and not_word in question:
            not_flag = True
            break
    if not_flag:
        print(Fore.YELLOW + "\n!!**请注意此题为否定题,选计数最少的**!!\n" + Fore.RESET)

    # 请求
    kv = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
    req = requests.get(url='https://www.baidu.com/s?wd='+question, headers=kv)
    r = req.content
    content = str(r, encoding='utf-8', errors='ignore')
    #print(content)
    counts = []
    for i in range(len(choices)):
        counts.append(content.count(choices[i]))
        #print(choices[i] + " : " + str(counts[i]))
    output(choices, counts)

def output(choices, counts):
    counts = list(map(int, counts))
    #print(choices, counts)

    # 计数最高
    index_max = counts.index(max(counts))

    # 计数最少
    index_min = counts.index(min(counts))

    if index_max == index_min:
        print(Fore.RED + "高低计数相等此方法失效！" + Fore.RESET)
        return

    for i in range(len(choices)):
        if counts[i] == counts[index_max]:
            # 绿色为计数最高的答案
            print(Fore.GREEN + "{0} : {1} ".format(choices[i], counts[i]) + Fore.RESET)
        elif counts[i] == counts[index_min]:
            # 红色为计数最低的答案
            print(Fore.MAGENTA + "{0} : {1}".format(choices[i], counts[i]) + Fore.RESET)
        else:
            print("{0} : {1}".format(choices[i], counts[i]))


def run_algorithm(al_num, question, choices):
    if al_num == 0:
        open_webbrowser(question)
    elif al_num == 1:
        open_webbrowser_count(question, choices)
    elif al_num == 2:
        count_base(question, choices)

if __name__ == '__main__':
    question = '新装修的房子通常哪种化学物质含量会比较高?'
    choices = ['甲醛', '苯', '甲醇']
    run_algorithm(1, question, choices)


