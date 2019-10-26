# -*- coding: utf-8 -*-
# 递归构建目录层级的操作

from bs4 import BeautifulSoup, NavigableString
import re
import os
import json
import time
import subprocess
import shutil
import requests
import jpype
import os.path
from urllib import quote
from conf.logger import ELKlogger, funlogger as logger
from conf.config import special_titles, title_order_1, title_pattern_1, title_order_2, title_pattern_2

from conf.config_consul import pdfengine_path
from conf.config_consul import cfg

# from util.chinese_char_detector import ChDetector

# 设置logger
from cases.task import Task
import util

origin_dir = cfg.origin_pdf_dir
dest_dir = cfg.target_htm_dir
requests.adapters.DEFAULT_RETRIES = 5

import re


class ChDetector(object):
    def __init__(self, filename):
        self.filename = filename
        self.ratio = 0
        self.detect_bad_code()

    def detect_bad_code(self):
        try:
            with open(self.filename, 'r') as f:
                content = f.read()
                self.ratio = self.get_chinese_ratio(content)
        except:
            pass

    def get_chinese_ratio(self, check_str):
        """
        :param check_str: string read from the file(.html) converted from pdf by solid or other tools.
        :return: A ratio represents how many Chinese characters are detected in the given string.
        """
        try:
            check_str = check_str.decode('utf-8')
            # 去除空白字符
            check_str = re.sub('\\s', '', check_str)  #
            # 去除html 标记
            check_str = re.sub("<.*?>", "", check_str)
            # 去除英文字母与数字
            check_str = re.sub('\\w', '', check_str)  #
            # 去除中文标点符号
            check_str = re.sub(u"[、。，；“”\"?：;:\-（）{｝{},.，。]", '', check_str)  #

            chrsum = len(check_str)
            target = 0
            for ch in check_str:
                if u'\u4e00' <= ch <= u'\u9fff':
                    target += 1
            # if target > 2:
            #     return 100
            # else:
            #
            #     return 0
            return float(int(float(target) / chrsum * 10000)) / 100
        except:
            return 0


def is_empty_content(htmlstring):
    """判断除去标签字符后，整个htm的内容是否为空
            u'<html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        </meta>
        </head>
        <body>
        </body>
        </html>
        '
    :return:
    """
    htmlstring = "".join(htmlstring.split())
    pattern = re.compile('<.*?>') # 这里要用非贪心匹配
    detagstr = re.sub(pattern, '', htmlstring)
    if len(detagstr) == 0:
        return True
    return False


dot_placeholder = u'ol@#$'


# 读取CSS文件中所有ol节点的编号定义
def get_ol_defines(bsHander):
    """
    解析如下格式
     #l3 {padding-left: 0pt;counter-reset: d1 2; }
     #l3> li:before {counter-increment: d1; content: counter(d1, decimal)" "; color: black; font-style: normal; font-weight: normal; text-decoration: none; }
     #l4 {padding-left: 0pt;counter-reset: d2 0; }
     #l4> li:before {counter-increment: d2; content: counter(d1, decimal)"."counter(d2, decimal)" "; color: black; font-family:"Times New Roman", serif; font-style: normal; font-weight: bold; text-decoration: none; font-size: 10.5pt; }
     #l4> li:first-child:before {counter-increment: d2 0;  }  //这行可能没有!
    :param bsHandler:
    :return:
    """
    ol_mark = u'#l'
    ol_first_child_mark = u'> li:first-child'
    ol_defines = {}
    cl_defines = {}
    styles = bsHander.findAll("style")
    reset_mark = u'counter-reset: '
    content_mark = u'content: '
    incr_mark = u'counter-increment: '
    for style in styles:
        if style is None or style.text is None or len(style.text) == 0:
            continue
        lines = style.text.split("\n")
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith(ol_mark):
                reset_mark_ind = line.find(reset_mark)
                if reset_mark_ind > 0:
                    ol_id = line[1:line.find(u' ')]
                    reset_text = line[reset_mark_ind + len(reset_mark):line.find(u';', reset_mark_ind)]
                    reset_text_parts = reset_text.split(u' ')
                    cl_defines[reset_text_parts[0]] = int(reset_text_parts[1])
                    i += 1
                    # 获取拼接的方式
                    content_ind = lines[i].find(content_mark)
                    content = lines[i][content_ind + len(content_mark):lines[i].find(u';', content_ind)]
                    content_format, params = parse_content_format(content)
                    i += 1
                    # 默认每个tag每次自增1
                    incr = 1
                    if i < len(lines) and lines[i].strip().startswith(u'#' + ol_id + ol_first_child_mark):
                        incr_ind = lines[i].find(incr_mark)
                        if incr_ind > 0:
                            incr_str = lines[i][incr_ind + len(incr_mark):lines[i].find(u';', incr_ind)].split(u' ')[1]
                            incr = int(incr_str)
                        i += 1
                    ol_defines[ol_id] = {"counter": reset_text_parts[0],
                                         "value": int(reset_text_parts[1]),
                                         "format": content_format,
                                         "params": params,
                                         "first_increment": incr,
                                         "formatted": False}
                else:
                    i += 1
            else:
                i += 1
    return ol_defines, cl_defines


def parse_content_format(format):
    prefix = u"counter("
    suffix = u', decimal)'
    params = []
    pre_ind = format.find(prefix)
    while pre_ind >= 0:
        suffix_ind = format.find(suffix, pre_ind)
        param = format[pre_ind + len(prefix):suffix_ind]
        params.append(param)
        pre_ind = format.find(prefix, suffix_ind)
    format_new = format.replace(prefix, u'').replace(suffix, u'').replace(u'"', u'')
    for param in params:
        format_new = format_new.replace(param, u'%s')
    return format_new, params


def format_ol_according_defines(bsHander):
    try:
        ol_defines, cl_defines = get_ol_defines(bsHander)
        ols = bsHander.findAll("ol")
        for ol in ols:
            format_ol(ol_defines, cl_defines, ol)
        return True
    except Exception as e:
        logger.error("Error while format_ol_according_defines")
        logger.error(e, exc_info=True)
        return False


def format_ol(ol_defines, cl_defines, ol):
    if ol_defines[ol.attrs['id']]["formatted"] is True:
        return
    else:
        ol_defines[ol.attrs['id']]["formatted"] = True
    ol_define = ol_defines[ol.attrs['id']]
    counter = ol_define["counter"]
    value = ol_define["value"]
    cl_defines[counter] = value
    tags = ol.findAll(["ol", "li"], recursive=False)

    for tag_i in range(0, len(tags)):
        tag = tags[tag_i]
        if tag.name == 'li':
            # 只有当li是ol下第一个子元素时css中li:first-child:before {counter-increment: d1 0;  }这种配置才有效
            if tag_i == 0:
                cl_defines[counter] += ol_define['first_increment']
            else:
                cl_defines[counter] += 1
            sub_tags = tag.findAll(recursive=False)
            formatted = False
            for i in range(0, len(sub_tags)):
                if sub_tags[i].name == "ol":
                    format_ol(ol_defines, cl_defines, sub_tags[i])
                elif sub_tags[i].name != "ol" and not formatted:
                    content_format = ol_define["format"]
                    content_params = ol_define["params"]
                    content_params_values = []
                    for content_param in content_params:
                        content_params_values.append(cl_defines[content_param])
                    if content_format is not None and content_format.replace(' ', '') == u'%s':
                        used_format = content_format.replace(u'%s', u'%s' + dot_placeholder)
                    else:
                        used_format = content_format
                    sub_tags[i].insert(0, used_format % tuple(content_params_values))
                    formatted = True
        elif tag.name == 'ol':
            format_ol(ol_defines, cl_defines, tag)


class PostConverter(object):
    def __init__(self, htmlPath, taskId="", title="", zsAutoCategory="", heading_set="", htmlString="",
                 bsfeature='lxml'):
        """

        :param htmlPath:  the absolute path of the source html
                the images and other sources of this html is saved in a fold with same name
        :param title:  the title of the source html
        :param zsAutoCategory:
        :param heading_set:
        """
        self.bsfeature = bsfeature
        self.logger = logger
        self.taskid = taskId
        self.conclusion = {}
        self.reserve = "hidden"
        self.status = False
        self.response_msg = ""
        self.htmlPath = htmlPath
        self.htmlresultPath = ""
        self.htmlString = htmlString
        self.htmlfoldername = os.path.basename(self.htmlPath).replace(".htm", "")
        self.title = title
        self.zsAutoCategory = zsAutoCategory
        self.soup_handler = BeautifulSoup("<html></html>", self.bsfeature, from_encoding="utf-8")
        self.identifiers, self.identifiers_previous = self.get_identifier_list()

        self.category_list = []
        self.category_tag_list = []
        self.category_dict = {}
        self.flag_cateogry_end = False
        self.title_soup = BeautifulSoup("<body><p></p></body", self.bsfeature, from_encoding="utf-8")
        self.first_heading_idx = 0
        # 保存标题text及原格式索引值
        self.potential_title_dict = {}
        self.potential_title_list = []
        self.idx_diff = 0
        self.potential_title_tag_list = []
        self.max_title_gid = 0
        # 保存目录结点用于文章识别完成后回填
        self.category_class = []
        self.category_status = False
        self.title_group = {}
        self.hmap = {}

        self.start_timestamp = 0
        self.end_timestamp = 0

        self.potential_title_tag = 'p'
        # 重大事项提示, 目录，释义等
        self.special_title_list = []
        self.special_title_tag_list = []
        try:
            self.heading_set = json.loads(heading_set)
        except:
            self.heading_set = None
        # self.logger = Logger(self._id, logging.DEBUG).get()
        self.potential_identifiers = []  # 需要动态添加的标题模版, 1.2 此类型的标题
        self.head_levels = ['h2', 'h3', 'h4', 'h5', 'h6']  # 指示哪些标题级别需要最后保留下来。之前只保留到h5, 现在添加到h6

    def is_empty(self, soup):
        if self.status is True:
            return
        for item in soup.contents:
            # if item.is_empty_element is False:
            if self.status is True:
                break
            if isinstance(item, NavigableString) and len(item.string) > 0:
                self.status = True
                # self.response_msg = "not an empty html"
                self.response_msg = ""
            else:
                self.is_empty(item)

    def parse_heading(self):
        pass

    # def get_heading_set(self):
    #     if len(self.heading_set) > 0:
    #         heading_set = json.loads(self.heading_set)
    #
    #         if self.varify_title_list(title_tag_list):
    #             for node in title_tag_list:
    #                 idx = node.attrs["href"]
    #                 self.potential_title_tag_list[idx + self.idx_diff].name = 'h' + str(tagflag)
    #                 if node.find("div") is not None:
    #                     self.set_title_tag(node.find("div"), tagflag + 1)
    #
    #         else:
    #             self.logger.debug("set_title_tag failed varify_title_list for %s" % (
    #                 ';'.join([title.contents[0] for title in title_tag_list])))

    @staticmethod
    def get_identifier_list():
        cata_group = []

        # 这里标题模版的顺序不能轻易调整，因为在做标题识别的时候出于实际情况的考虑，给予了部分标题以优待，如果它们的索引有调整那么其对应的列表也要调整
        # identifiers_previous的值要对应 第%s节,第%s部分,第%s条,第%s章,第%s、这几个标题模版
        number = title_order_2
        format_li = title_pattern_2
        for i in format_li:
            cata_group.append([i.replace('%s', n) for n in number])

        number = title_order_1
        format_li = title_pattern_1
        for i in format_li:
            cata_group.append([i.replace('%s', n) for n in number])
        identifiers_previous = [1, 2, 3, 4, 5]
        return cata_group, identifiers_previous

    @property
    def convert_msg(self):
        return self.response_msg

    @property
    def convert_status(self):
        return self.status

    def get_soup_handler(self):
        """
                TGet DOM tree
        :return:
        """

        try:
            self.soup_handler = BeautifulSoup(self.htmlString, self.bsfeature, from_encoding="utf-8")
            # TODO 检查soup 是否为空的函数未成功检测
            self.status = False
            self.response_msg = "empty html"
            self.is_empty(self.soup_handler.find("body"))

            if self.status is False:
                self.logger.debug("[ empty html detected ] %s" % self.htmlPath)

            # TODO 检查 soup 中的body标签中的内容是否为空
            body = self.soup_handler.find("body")
            # if body.string is None or len(body.string) <= 10:
            if len(str(body)) <= 10:
                self.status = False
                self.response_msg = "empty html"
                logger.debug("get_soup_handler stopped %s " % (self.taskid))
        except Exception as err:
            logger.debug("-*- post converter exception %s" % (err))
            pass

    def __format_ol(self):
        """
                提取ol相关格式是根据原文中的换行符逐行处理的
                所以在处理完ol之前， <br> 不能移除
        :return:
        """
        # 格式化所有的ol标签相关的编号，
        # 用到了style属性
        formatted = format_ol_according_defines(self.soup_handler)
        if formatted is False:
            self.logger.warning("Format_ol_according_defines failed for %s" % self.htmlPath)

        # ul, dl 去掉, 发现会影响二级标题的识别
        # 如“二、限制性股票的授予价格”在p下面，和“一、xxx”在ol下面，ol在p下面
        for x in self.soup_handler.findAll(["ul", "ol", "li"]):
            x.unwrap()

    def identify_group(self, text):
        """
                # 返回匹配到的标题的组位置索引、组内位置索引、标号
                # 如 2、xxx， 返回的是 [0, 1, 2、] ，(结合config.properties一起看)

        :param text:
        :return:
        """
        text = text.replace("\n", "").replace(" ", "").strip()
        # TODO for debug
        # if '7.4.1' in text:
        #     pass
        if len(text) > 0:
            for groupNum in range(len(self.identifiers)):
                for groupItem in self.identifiers[groupNum][::-1]:
                    if text.startswith(groupItem) is True:
                        return groupNum, self.identifiers[groupNum].index(groupItem), groupItem
        return None, None, None

    def identify_groups(self, text):
        """
                了解为什么内层for循环要倒序了。 类似十一、这种标题正序的话一定先识别出 一、
                # 返回匹配到的标题的组位置索引、组内位置索引、标号
                # 返回list, 文本中有多少个标题标识就返回多少个

        # TODO 2019-10-17 需要匹配类似 1.2， 4.3.3 这类子标题
        # 遇到一个 3.4.5格式的标题，将其最低级别的子标题改成1， 最后统一添加到identifiers中去
        :param text:
        :return:
        """

        # <p>邮编：4300153、承销团</p>
        # potential_identifiers = []  # 需要动态添加的标题模版
        gids = []
        startflag = 0
        category_flag = 0
        markflag = ""
        if len(text) > 0:
            # 这一部分是为了排除文本中一些统计数字及电话号码的干扰， 但一般出来在开头的数字应该是标题，所以下面加了判断并跳过它们
            # matches = re.findall(u'\d+\.\d+', text)  # 0.13%
            matches = re.findall('\d+(?:\.\d+)+', text)  # 0.13%
            for m in matches:
                if text.startswith(m):
                    # self.potential_identifiers.append(m)
                    continue
                text = re.sub(m, "-" * len(m), text)  # 用相同长度字符替换，不影响整体字符长度
            matches = re.findall(u'\d+、\s?\d+', text)  # 电话号码
            for m in matches:
                text = re.sub(m, "-" * len(m), text)

            for gid in range(len(self.identifiers)):
                for groupItem in self.identifiers[gid][::-1]:
                    if text.startswith(groupItem) is True:
                        startflag = 1
                        gids.append({"gid": gid,
                                     "idx": self.identifiers[gid].index(groupItem),
                                     "mark": groupItem})
                    elif groupItem in text:
                        if u"见" + groupItem in text:
                            text.replace(groupItem, "")
                        else:
                            markflag = groupItem
                            gids.append({"gid": gid,
                                         "idx": self.identifiers[gid].index(groupItem),
                                         "mark": groupItem})
                    text = ''.join(text.split(groupItem))
            if re.search('\d$', text):
                category_flag = re.findall('\d+$', text)[-1]
                category_flag = int(category_flag)

        return startflag, gids, markflag, category_flag

    def extract_identifiers(self):
        # 根据遍历全文找出来的有可是标题的行， 从中提取出3.3这种类型的标题， 添加identifiers中， 这部分这样动态处理比较好
        """
        TODO 需要对标题级别做排序， 1.2.3.4为4级标题， 1.2.3.4.5为5级标题， 5级标题需要位于4级标题前面
        :return:
        """

        def unify_idx(i):
            flag = '.'.join(i.split('.')[:-1]) + '.1'
            return flag

        # 只筛选出级别为1.1.1以下的目录级别
        potentialflags = [x for x in self.potential_identifiers if len(x.split('.')) > 2]
        flags = set(map(unify_idx, potentialflags))
        constant = range(40)[1:]
        # 排序，按级别正序
        flag_dict = {}
        for i in list(flags):
            flag_dict[i] = len(i.split('.'))
        flag_dict = sorted(flag_dict.items(), key=lambda x: x[1])
        flags = [x[0] for x in flag_dict]
        for item in list(flags):
            # lambda x, '.'.join(item.rpartition('.').pop() +[x])
            # TODO 这一批标题模版需要插在config.cfg中title_pattern_1变量里1.1这一批标题之前，不然匹配的时会先匹配到这里的二级标题，低级别的仍然匹配不到
            # TODO 最好的是不要把索引10 hard code
            self.identifiers.insert(10,
                                    list(map(lambda x: '.'.join(list(item.split('.'))[:-1] + [str(x)]), constant)))

    def move_node_top(self, node):
        body_tag = self.soup_handler.find("body")
        for parent in node.parents:
            if parent.parent == body_tag:
                parent.insert_before(node)

    # def split_multi_title(self, text):
    #     """
    #             一般最多只有两个标题边成一行。
    #     :param text:
    #     :return:
    #     """
    #     # groupids = []
    #     # marks = []
    #     text = text.replace("\n", "").replace(" ", "").strip()
    #     if len(text) > 0:
    #         for groupNum in range(len(self.identifier_list)):
    #             for groupItem in self.identifier_list[groupNum]:
    #                 try:
    #                     if groupItem in text and text.startswith(groupItem) is not True:
    #                         s = text.split(groupItem)
    #                         return s[0], groupItem + s[1]
    #                 except:
    #                     return None, None

    def rewrap_tag(self, node, tag):
        """

        :param node:  <a>test</a>
        :param tag:  <p></p>
        :return:  <p>test</p>
        """
        new_tag = self.soup_handler.new_tag(tag)
        node.wrap(new_tag)
        node.unwrap()

    def split_text(self, node, mark, name1, name2):
        """

        :param node: <tag> abc mark 123</tag>
        :param mark:
        :param name1:
        :param name2:
        :return: <name1> abc</name1>
                  <name2>mark 123</name2>
        """
        splits = node.text.split(mark)
        # report_id = 913509 , 直接父结点：十、报告期内公司重要事项公告索引
        if len(splits[-1]) <= 1:
            return
        idx = node.text.rfind(mark)
        new_tag = self.soup_handler.new_tag(name2)
        new_tag.string = node.text[idx:]  # mark + ts[1]

        node.string = node.text[0:idx]
        node.name = name1
        node.insert_after(new_tag)  # new_tag插入到node后
        self.move_node_top(new_tag)

    def dynamic_title(self):
        # 有部分样式为1.1, 1.2, 1.1.1, 1.1.2这类模式的标题动态添加到标题识别模版集中
        for node in self.soup_handler.find("body").children:
            try:
                # TODO 对全文的处理要特别小心， 一定要过滤掉所有表格
                if self.is_contained_in_table(node):
                    continue
                node.string = node.get_text("", strip=True).replace(" ", "")
                text = node.text
                if len(text) > 0:
                    # 这一部分是为了排除文本中一些统计数字及电话号码的干扰， 但一般出来在开头的数字应该是标题，所以下面加了判断并跳过它们
                    # matches = re.findall(u'\d+\.\d+', text)  # 0.13%
                    matches = re.findall('\d+(?:\.\d+)+', text)  # 0.13%
                    for m in matches:
                        if text.startswith(m):
                            self.potential_identifiers.append(m)
                            continue
            except:
                pass
        # 这部分处理动态添加的标题标识符
        self.extract_identifiers()

    def potential_title(self):
        """
                提取标题文本与索引
                全文扫描，分别提取目录， 正文标题， 与special title
                目录结构结束的识别条件： 当前检查的文本在category_list中存在相同文本。
        :return:
        """
        # “详见，参见第九章” 这种情况的处理。决策方法不添加了标题列表中去
        idx = 0
        for node in self.soup_handler.find("body").children:
            # if isinstance(NavigableString, node):
            try:
                #     continue
                if self.is_contained_in_table(node):
                    continue
                if node.name == self.reserve:
                    continue
                if node.text.strip() == "" and node.img is None and node.name is not self.reserve:
                    node.name = 'del'
                    continue
                # if u"养成分" in node.text:
                #     pass
                node.name = 'p'
                if node.img is not None:
                    continue
                # node.string = " ".join(node.text.replace("\n", "").split())
                node.string = node.get_text("", strip=True).replace(" ", "")
                # map(lambda item: " ".join(item.text.replace("\n", "").split()).replace(" ", ""), node.contents)
                startflag, gids, markflag, category_flag = self.identify_groups(node.text)
                if node.text in self.category_list and category_flag == 0:
                    self.flag_cateogry_end = True
                if len(gids) == 0:
                    if node.text in special_titles:
                        node.name = self.potential_title_tag
                        self.potential_title_dict[node.text] = idx
                        self.special_title_list.append(node.text)
                        self.special_title_tag_list.append(node)
                        self.logger.debug("potential_title() special title : %s" % (node))

                elif startflag == 0 and len(gids) == 1:
                    self.split_text(node, gids[0]['mark'], node.name, self.potential_title_tag)

                elif startflag == 1 and len(gids) == 2:
                    self.split_text(node, markflag, self.potential_title_tag, self.potential_title_tag)

                else:
                    node.name = self.potential_title_tag
                    self.move_node_top(node)
                    # self.logger.debug("potential_title() get title tag [ %s ] with length of gids=%s: %s" % (
                # 可能存在标题拆分的情况，需要等拆分过程结束后再放入list中
                if len(gids) > 0 and startflag == 1:
                    if category_flag > 0 and self.flag_cateogry_end is False:
                        node.name = 'p'
                        self.category_list.append(node.text.split(str(category_flag))[0])
                        self.category_tag_list.append(node.text)
                        self.category_dict[node.text.split(str(category_flag))[0]] = category_flag
                        self.logger.debug("potential_title() get category %s, with %s " % (node, json.dumps(gids)))

                    else:
                        self.potential_title_dict[node.text] = idx
                        self.potential_title_list.append(node.text)
                        self.potential_title_tag_list.append(node)
                        self.logger.debug("potential_title() get title %s, with %s " % (node, json.dumps(gids)))

            except:
                self.logger.debug("potential_title() exception : %s" % node)
            idx += 1
            # self.log_category(self.potential_title_list, "potential_title")
            # self.output_htm(self.htmlPath, "done_potential_title")

            # self.output_result_htm()

    def potential_category(self):
        if len(self.category_list) > 0:
            # mutual improve heading detection
            pass
        else:
            self.select_top_gid_by_idx_range()
            # if no category exists, choose the group of title with largest page range

    def select_top_gid_by_idx_range(self):
        """
        将potential_title_list中备选标题按层级构建成目录
        title_group是按照不同的标题格式分组得到的一个dict, 其中每一项标识出了该类标题第一次及最后一次出来的索引值，以此估计其跨越了多少页
        做为识别出一级目录的重要依据
        :return:
        """

        # potential_title中的key是无序的。
        for i, title in enumerate(self.potential_title_list):
            if re.search('\d$', title):
                continue
            gid, idx, mark = self.identify_group(title)
            # if gid not in self.title_group.keys():
            #     self.title_group[gid] = []
            # else:
            #     self.title_group[gid].append(i)
            # relatedindex = self.potential_title_dict[title]
            try:
                if idx == 0:
                    self.title_group[gid] = {
                        "index": [i],
                        "mark": mark,
                        "startidx": self.potential_title_dict[title],
                        "endidx": -1,
                        "idxrange": 0
                    }
                else:
                    self.title_group[gid]["endidx"] = self.potential_title_dict[title]
                    self.title_group[gid]["index"].append(i)
            except:
                pass

        for gid in self.title_group.keys():
            try:
                self.title_group[gid]["idxrange"] = \
                    self.title_group[gid]["endidx"] - self.title_group[gid]["startidx"]
                # self.title_group[gid] = self.title_group[gid]["endidx"] - self.title_group[gid]["startidx"]
            except:
                pass
        # TODO to remove confused title group
        # TODO 这里的初衷是为了给类似“第一节”，“第一章”这类标题有更高一级的优先级，这样当发现从原文中搜出来的标题列表中包含只类标题时
        # TODO 把它们做为第一级标题。
        # 问题是现在由于这个操作引入了异常数据，来了一个不知道从哪里匹配上的“第一、”， 误把它当作标题，而实际上它又不是标题。
        # 加上数据限制吧。
        # if any(g in self.title_group.keys() for g in self.identifiers_previous):
        # TODO 2019-10-17 修改， 优先查找那5个标题模版， 没匹配到标题的话作为标题备选的标题id结果会是-1， 然后再走下面的if判断。重新先一级标题
        self.max_range_with_limit_key(self.identifiers_previous)

        if self.max_title_gid < 0:  # 说明上面没有找到靠谱的标题
            top_gid = -1
            top_range = -1
            for gid, ran in self.title_group.items():
                if ran["idxrange"] > top_range:
                    top_range = ran["idxrange"]
                    top_gid = gid
            self.max_title_gid = top_gid
            if top_gid == -1:
                self.logger.warning("select_top_gid_by_idx_range top_gid is -1 %s" % json.dumps(self.title_group))
            else:
                self.logger.debug(
                    "select_top_gid_by_idx_range top_gid=%s is %s" % (
                        self.max_title_gid, json.dumps(self.title_group[self.max_title_gid])))
                # 可能还要加上只出现过一次的gid这个限制条件
                # return top_gid

    def max_range_with_limit_key(self, keys):
        top_gid = -1
        top_range = -1
        for gid, ran in self.title_group.items():
            if ran["idxrange"] > top_range and gid in keys:
                top_range = ran["idxrange"]
                top_gid = gid
        self.max_title_gid = top_gid
        if top_gid == -1:
            self.logger.warning("select_top_gid_by_idx_range top_gid is -1 %s" % json.dumps(self.title_group))
        else:
            self.logger.debug(
                "select_top_gid_by_idx_range top_gid=%s is %s" % (
                    self.max_title_gid, json.dumps(self.title_group[self.max_title_gid])))

    def log_category(self, category, name):
        new_file_Path = \
            self.htmlPath[0:self.htmlPath.rfind('.')] + "_" + name + self.htmlPath[self.htmlPath.rfind('.'):]
        with open(new_file_Path, 'wb') as htmlHandler:
            htmlHandler.write(str(category))
            #
        self.logger.debug("category list %s" % new_file_Path)

    def build_soup_for_category(self):

        # if len(self.category_list) > 0:
        #     # set up first level category soup
        # else:
        #     #
        pass

    def build_soup_title(self, top_gid, flag):
        if len(self.category_list) == 0:
            self.idx_diff = 0
            flag = 0
        self.title_soup = BeautifulSoup("<body><p></p></body", self.bsfeature, from_encoding="utf-8")
        soup = self.title_soup
        next_idx = 0
        next_gid = -1
        for i, node in enumerate(self.potential_title_list[flag:]):
            gid, idx, mark = self.identify_group(node)
            # self.logger.info("build_soup_title (gid=%s, idx=%s, mark=%s) for node :%s" % (
            #     gid, idx, mark, node))
            if gid >= 0:  # or node in special_titles:
                title_tag = self.title_soup.new_tag("p", class_=gid, id=idx, href=i)
                title_tag.string = node
                # To deal with duplication
                # if self.title_soup.find('p', attrs={"class_": gid, "id": idx}, recursive=False) is not None:
                #     exist_node = self.title_soup.find('p', attrs={"class_": gid, "id": idx}, recursive=False)
                #         try:
                #             exist_node.previous_sibling.append(exist_node.contents[0])
                #         except:
                #             pass
                #         soup.append(title_tag)
                #         exist_node.decompose()
                #         self.logger.debug(
                #             "build_soup_title gid == next_gid len(%s) < len(%s)" % (node, exist_node.text))
                #         continue
                if idx == 0:
                    new_tag = self.title_soup.new_tag("div", class_=gid)
                    soup.find_all('p')[-1].append(new_tag)
                    soup = new_tag
                    next_idx = 1
                    next_gid = gid
                    soup.append(title_tag)
                    self.logger.info("build_soup_title (gid=%s, idx=%s, mark=%s) for node :%s,"
                                     "expect next : next_id=%s, next_gid=%s" % (gid, idx, mark, node,
                                                                                next_idx, next_gid))
                    # self.logger.debug("expect next : next_id=%s, next_gid=%s" % (next_idx, next_gid))
                elif gid == next_gid and idx == next_idx:
                    soup.append(title_tag)
                    next_idx += 1
                    next_gid = gid
                    self.logger.info("build_soup_title (gid=%s, idx=%s, mark=%s) for node :%s,"
                                     "expect next : next_id=%s, next_gid=%s" % (gid, idx, mark, node,
                                                                                next_idx, next_gid))
                else:
                    for prenode in soup.parents:
                        if prenode.name == "body":
                            break
                        if prenode is not None and prenode.name == 'div' and prenode.attrs["class_"] == gid:
                            soup = prenode
                            last_child = soup.find_all("p", recursive=False)[-1]
                            next_idx = last_child["id"] + 1
                            next_gid = gid
                            if next_idx == idx:
                                soup.append(title_tag)
                                next_idx = idx + 1
                                next_gid = gid
                                self.logger.info(
                                    "build_soup_title (gid=%s, idx=%s, mark=%s) for node :"
                                    "%s, expect next : next_id=%s, next_gid=%s"
                                    % (gid, idx, mark, node, next_idx, next_gid))
                                break
                            else:
                                pass

    def soup_title_tag(self, startidx, endidx, soup):
        if startidx >= endidx:
            return
        titles = []
        for item in self.potential_title_list[startidx:endidx]:
            if item in special_titles:
                title_tag = self.title_soup.new_tag("p")
                title_tag.string = item
                titles.append(title_tag)
        if len(titles) > 0:
            new_tag = self.title_soup.new_tag("div", class_=1000)
            soup.append(new_tag)
            soup = new_tag
            for item in titles:
                soup.append(item)
            return

        next_idx = 0
        next_gid = -1
        for item in self.potential_title_list[startidx:endidx]:
            gid, idx, mark = self.identify_group(item)
            self.logger.debug("soup_title_tag [1](gid=%s, idx=%s, mark=%s) for node :%s" % (
                gid, idx, mark, item))
            if gid >= 0:
                title_tag = self.title_soup.new_tag("p", class_=gid, id=idx)
                title_tag.string = item
                if idx == 0:
                    new_tag = self.title_soup.new_tag("div", class_=gid)
                    # soup.append(new_tag)
                    soup.find_all('p')[-1].append(new_tag)
                    soup = new_tag
                    next_idx = 1
                    next_gid = gid
                    soup.append(title_tag)
                    self.logger.debug("soup_title_tag [idx == 0] : next_gid=%s, next_id=%s" % (next_gid, next_idx))
                elif gid == next_gid and idx >= next_idx:
                    next_idx = next_idx + 1 if next_idx is not None else None
                    soup.append(title_tag)
                    self.logger.debug("soup_title_tag [idx != 0] : next_id=%s, next_gid=%s" % (next_gid, next_idx))
                else:
                    for prenode in soup.parents:
                        if prenode.name == "body":
                            break
                        if prenode is not None and prenode.name == 'div' and prenode.attrs["class_"] == gid and \
                                prenode.find_all("p", recursive=False)[-1].attrs["id"] + 1 == idx:
                            next_idx = idx + 1
                            next_gid = gid
                            soup = prenode
                            soup.append(title_tag)

                            self.logger.debug("prenode %s " % prenode.contents[0])
                            break

    def soup_title_hierachy(self):
        # To creat a dom tree from potential title list,
        # with title hierachy reserved
        if len(self.category_list) == 0:
            self.idx_diff = 0
            flag = 0
        self.title_soup = BeautifulSoup("<body><p></p></body", self.bsfeature, from_encoding="utf-8")
        soup = self.title_soup
        next_idx = 0
        next_gid = -1
        for i, node in enumerate(self.potential_title_list[self.idx_diff:]):
            gid, idx, mark = self.identify_group(node)
            # self.logger.debug("build_soup_title (gid=%s, idx=%s, mark=%s) for node :%s" % (
            #     gid, idx, mark, node))
            if gid >= 0:  # or node in special_titles:
                title_tag = self.title_soup.new_tag("p", class_=gid, id=idx, href=i)
                title_tag.string = node

                if idx == 0:
                    new_tag = self.title_soup.new_tag("div", class_=gid, page=i)
                    soup.find_all('p')[-1].append(new_tag)
                    soup = new_tag
                    next_idx = 1
                    next_gid = gid
                    soup.append(title_tag)
                    self.logger.debug("build_soup_title (gid=%s, idx=%s, mark=%s) for node :%s,"
                                      "expect next : next_id=%s, next_gid=%s" % (gid, idx, mark, node,
                                                                                 next_idx, next_gid))
                    # self.logger.debug("expect next : next_id=%s, next_gid=%s" % (next_idx, next_gid))
                elif gid == next_gid and idx == next_idx:
                    soup.append(title_tag)
                    next_idx += 1
                    next_gid = gid
                    self.logger.debug("build_soup_title (gid=%s, idx=%s, mark=%s) for node :%s,"
                                      "expect next : next_id=%s, next_gid=%s" % (gid, idx, mark, node,
                                                                                 next_idx, next_gid))
                else:
                    for prenode in soup.parents:
                        if prenode.name == "body":
                            break
                        if prenode is not None and prenode.name == 'div' and prenode.attrs["class_"] == gid:
                            soup = prenode
                            last_child = soup.find_all("p", recursive=False)[-1]
                            next_idx = last_child["id"] + 1
                            next_gid = gid
                            if next_idx == idx:
                                soup.append(title_tag)
                                next_idx = idx + 1
                                next_gid = gid
                                self.logger.debug(
                                    "build_soup_title (gid=%s, idx=%s, mark=%s) for node :"
                                    "%s, expect next : next_id=%s, next_gid=%s"
                                    % (gid, idx, mark, node, next_idx, next_gid))
                                break
                            else:
                                pass

    def set_special_title(self):
        if len(self.potential_title_dict) == 0:
            return
        first_heading_idx = self.potential_title_dict[self.title_soup.find('div').contents[0].contents[0]]
        last_heading_idx = self.potential_title_dict[self.title_soup.find('div').contents[-1].contents[0]]
        # soup1 = self.title_soup.find('div').contents[0]
        # soup2 = soup1.div.contents[0]
        # if soup2 is not None:
        # if soup2 is None:
        #     soup2 = soup1.append(self.title_soup.new_tag('div'))
        #     soup2.append(self.title_soup.new_tag('p', class_="anchor"))
        #     soup2 = soup2.div.p

        for item in self.special_title_tag_list:
            # new_tag = self.title_soup.new_tag('h2')
            # new_tag.string = item
            idx = self.potential_title_dict[item.text]
            if idx < first_heading_idx:
                item.name = 'h2'
            elif idx > last_heading_idx:
                item.name = 'h2'
                # soup1.insert_before(new_tag)
            else:
                item.name = 'h3'

        try:
            self.title_soup.find(attrs={"class_": "anchor"}).decompose()
        except:
            pass

    def soup_title(self):
        """
                The way to select heading is by combining category list and potential title list
        :return:
        """
        #  mutual support

        self.select_top_gid_by_idx_range()
        try:
            #
            self.idx_diff = self.title_group[self.max_title_gid]["index"][0]
            self.build_soup_title(self.max_title_gid, self.idx_diff)
            # self.soup_title_hierachy()
        except:
            pass

    def pre_prepare(self):
        """
                To remove all <a> , <b> and <span class='h\d'>
                Do pre_prepare before mark all titles.
                Find out all potential title tags, make them a new node
        :return:
        """
        # self.set_page_atag()

        # body_tag = self.soup_handler.find("body")
        # 先处理<a>
        # 1. 将表示分页的<a name='a1'>标签变为hidden标签
        # 2. 标题<a name='bookmark0'>
        # 3. 目录<a class='h4' href='#bookmark1'>
        category_set = []
        title = ''

        # 处理分页<a>
        for item in self.soup_handler.find_all("img"):
            if "height" in item.attrs and int(item["height"]) <= 1:
                item.decompose()

        for item in self.soup_handler.findAll("a"):
            if "name" in item.attrs:  # 仅处理有name属性的标签
                pattern = re.compile(r'a\d{1,}$')  # 匹配a0,a1,a2...等分页标签
                a_name = item.attrs["name"]
                m = pattern.match(a_name)
                if m:
                    a_content = item.get_text("", strip=True)
                    imgs = item.find_all('img')
                    # # 若content不为空，删除name属性
                    if a_content != "" or len(imgs) > 0:
                        del item['name']
                        item.name = 'p'
                    # # 若content为空，看是否有兄弟节点，若有则删除item，没有则删除父节点
                    else:
                        if item.next_sibling is None and item.previous_sibling is None:
                            item.name = self.reserve
                            item.contents = []
                            self.move_node_top(item)
                else:
                    self.logger.debug(u"pre_prepare 处理分页 not an a tag : %s" % item)
            else:
                self.logger.debug(u"pre_prepare 处理分页 no name attrs found : %s" % item)
                self.rewrap_tag(item, 'span')

    def __get_dict_value(self, key):
        return self.hmap[key]

    def get_clean_soup(self):

        # self.htmlString = self.soup_handler.encode()
        self.htmlString = self.soup_to_html()

        self.htmlString = re.sub('\\n', '', self.htmlString)
        self.htmlString = re.sub('\\t', '', self.htmlString)
        # 去掉br标签
        # self.htmlString = re.sub("<br.*?>", "", self.htmlString)
        # self.htmlString = re.sub("<br/>", "", self.htmlString)
        # &zwnj;
        self.htmlString = re.sub("&zwnj;", "", self.htmlString)
        # 去掉标签内除了标签名之外的style属性值
        self.htmlString = re.sub(" style=\".*?\"", "", self.htmlString)  # 非贪心匹配
        # 去年head标签之间的内容
        self.htmlString = re.sub("<head>.*</head>", "<head></head>", self.htmlString)

        # self.htmlString = re.sub("<a.*?></a>", "", self.htmlString)
        # self.htmlString = re.sub("<p.*?></p>", "", self.htmlString)
        # 去掉空标签
        # self.htmlString = re.sub("<(?P<tag>\w+)></(?P=tag)>", "", self.htmlString)
        # self.htmlString = re.sub("<(?P<tag>\w+)>&zwnj;</(?P=tag)>", "", self.htmlString)
        self.htmlString = re.sub("\\u200c", "", self.htmlString)
        # \u200c
        self.soup_handler = BeautifulSoup(self.htmlString, self.bsfeature, from_encoding="utf-8")

    def map_to_index(self, title_list):
        """
        :param title_list: [0, 1, 2, 4, 7]
        :return: [1, 1, 1, 0, 1, 0, 0, 1]
        """
        map_list = [0] * (max(title_list) + 1)
        for i in title_list:
            map_list[i] = 1
        return map_list

    def get_missing_idx(self, title_list):
        """
        :param title_list: [0, 1, 2, 4, 7]
        :return: [3, 5, 6]
        """
        map_list = self.map_to_index(title_list)
        missing_list = []
        for i, v in enumerate(map_list):
            if v == 0:
                missing_list.append(i)
        return missing_list

    def varify_title_list(self, title_tag_list):
        """
                1.根据标题个数判断
                2.获取各标题索引，如果任一标题都无子结点则将其标签名修改为p
        :param title_tag_list:
        :return:
        """
        # 本组标题长度为一时去掉标题标签
        if len(title_tag_list) <= 1:
            return False

        if any(u"。" in title.contents[0] for title in title_tag_list):
            return False
        if any(u"；" in title.contents[0] for title in title_tag_list):
            return False

        gid, idx, mark = self.identify_group(title_tag_list[-1].text)
        while gid is not None and len(title_tag_list) > idx + 1:
            for i, title in enumerate(title_tag_list):
                sgid, sidx, smark = self.identify_group(title.text)
                if not i == sidx:
                    self.logger.debug("varify_title_list with unexpected title for %s" % title)
                    del title_tag_list[i]
                    break
        return True

    def set_title(self, title, subtitle, title_list):
        """
                找到所有标签为tag.name == title的结点，将不在给定的title_list中的结点标签名改为tag.name == subtitle
                将title_list中的结点标签名改为tag.name == title
        :param title:
        :param subtitle:
        :param title_list:
        :param souphandler:
        :param self.identifier_list:
        :return:
        """
        for item in self.soup_handler.findAll(title):
            if item not in title_list:
                # new_tag = souphandler.new_tag(subtitle)
                # item.wrap(new_tag)
                item.name = subtitle  # item.unwrap()

        for item in title_list:
            if item.name is None:  # title_list中可能会有重复元素
                continue
            # new_tag = souphandler.new_tag(title)
            item.string = item.text.replace("\n", "").replace(" ", "").strip()
            # new_tag.append(inner_text)
            item.name = title  # item.replace_with(new_tag)
            # 检查tag.name == title 的前后sibling, 做相应调整
            self.filter_title(item, title, subtitle)

    def is_contained_in_table(self, tag):
        if tag.name == 'table':
            return True
        for x in tag.parents:
            if x.name == u"table":
                return True
        # if tag is None or tag.parents is None:
        #     return False
        return False

    def output_result_htm(self):

        # 判断结果是否符合最终输出，如果内容为空则返回false，
        self.htmlString = self.soup_to_html()
        # 通过正则，去除 <!DOCTYPE>标签
        self.htmlString = re.sub("<!DOCTYPE.*?>", "", self.htmlString)
        # 根据中间结果样式进行格式化
        if self.htmlString is None or self.status is False:
            return
        self.htmlresultPath = \
            self.htmlPath[0:self.htmlPath.rfind('.')] + "_result" + self.htmlPath[self.htmlPath.rfind('.'):]
        try:
            with open(self.htmlresultPath, 'wb') as htmlHandler:
                if type(self.htmlString) == unicode:
                    htmlHandler.write(self.htmlString.encode("utf8"))
                else:
                    htmlHandler.write(self.htmlString)
        except Exception as err:
            logger.warning('convert save htm as a file %s' % err)

        self.logger.debug("[ post convert done ] %s Successfully postConvert html" % (self.htmlresultPath))
        self.end_timestamp = time.time()

        # return self.htmlString
        self.htmlPath = self.htmlresultPath

    def output_htm(self, htmlPath, debug_flag):
        html = str(self.soup_handler)
        if html is None:
            return "", False
        new_filePath = os.path.join(os.path.dirname(htmlPath),
                                    debug_flag + '.htm')
        # htmlPath[0:htmlPath.rfind('.')] # + "_result" + htmlPath[htmlPath.rfind('.'):]
        # new_filePath = htmlPath
        with open(new_filePath, 'wb') as htmlHandler:
            htmlHandler.write(html)

        self.logger.debug('%s file write to disk' % debug_flag)

    def set_title_tag(self, categorynode, tagflag=2):
        # to mark title tag in original title list
        # tagflag will be "h2, h3, ... and so on"
        # start from h2
        """
        递归处理传入的目录，一层一层处理，按层级尝试设置其标题序号，层级越深，标题序号越大
        :param categorynode:
        :param tagflag:
        :return:
        """
        if categorynode is None:
            return
        title_tag_list = categorynode.find_all('p', recursive=False)
        # 同一组标题个数小于等于1的不做考虑
        if len(title_tag_list) <= 1:
            return
        elif len(title_tag_list) > 5:
            # when length of candidate title is more than 5
            # 1. to see where each title with comma
            # 2. to see where the min length among these title is more than 30(by experience)
            comma = []
            chars = []
            for title in title_tag_list:
                if u"。" in title.contents[0]:
                    comma.append(1)
                chars.append(len(title.contents[0]))
            # if all the element in current tag_list contains comma
            if comma.count(1) == len(title_tag_list):
                return
            if min(chars) > 30:
                return
        else:
            if any(u"。" in title.contents[0] for title in title_tag_list):
                self.logger.debug("set_title_tag comma detected in current title group %s" % title_tag_list[0])
                return
            if any(u"；" in title.contents[0] for title in title_tag_list):
                self.logger.debug("set_title_tag semicolon detected in current title group %s" % title_tag_list[0])
                return
        for node in title_tag_list:
            idx = node.attrs["href"]
            self.potential_title_tag_list[idx + self.idx_diff].name = 'h' + str(tagflag)
            if node.find("div") is not None:
                self.set_title_tag(node.find("div"), tagflag + 1)

    def set_title_direct(self, heading_list, tagflag):
        if heading_list is None:
            return
        if len(heading_list) > 0:
            for item in heading_list:
                flag = 0
                heading = item.get("title")
                for title in self.potential_title_tag_list:
                    if title.name == self.potential_title_tag and title.contents[0] == heading:
                        flag = 1
                        title.name = 'h' + str(tagflag)
                        self.set_title_direct(item.get("subtitles"), tagflag + 1)
                if flag == 0:
                    self.logger.debug("set_title_direct no match found for :%s" % item)

    def add_div_wrap(self, marker):
        try:
            for item in self.soup_handler.find_all(marker):
                title = item.text.strip().replace("\n", "").replace(" ", "").strip().replace(u'\u200c',
                                                                                             "")  # 本级 的title
                new_tag = self.soup_handler.new_tag("div", title=title)
                new_tag["type"] = "paragraph"
                for nitem in item.find_next_siblings():
                    if nitem.name != marker:
                        new_tag.append(nitem)
                    else:
                        break
                item.insert_after(new_tag)
                item.decompose()
                # item = new_tag
        except Exception as err:
            self.logger.error(err, exc_info=True)

    def add_header_div(self):
        try:
            # 在第一个h2的title之前，用paragraph包起来, 否则整个都包起来
            h2first = self.soup_handler.find("h2")
            new_tag = self.soup_handler.new_tag("div", type="paragraph")
            if h2first is None:
                self.soup_handler.body.wrap(new_tag)
            else:
                h2first_list = h2first.find_previous_siblings()
                h2first_list.reverse()
                for item in h2first_list:
                    new_tag.append(item)
                h2first.insert_before(new_tag)

            for h in self.head_levels:
                self.add_div_wrap(h)
                # self.add_div_wrap("h3")
            # self.add_div_wrap("h4")
            # self.add_div_wrap("h5")
            # self.add_div_wrap("h6")

            return True
        except Exception as err:
            self.logger.error(err, exc_info=True)
            return False

    def merge_horizontal_td(self, td, tds):
        next_td = None
        for next_brother in td.next_siblings:
            if next_brother in tds:
                next_td = next_brother
                break

        if next_td is None or 'style' not in next_td.attrs or 'border-left:none;' not in next_td['style']:
            return 0
        if 'border-right:none;' in next_td['style']:  # 递归的合并右边合适的td
            conflict_time = self.merge_horizontal_td(next_td, tds)
        else:
            conflict_time = 0

        td_rowspan = int(td.get("rowspan", "1"))
        next_td_rowspan = int(next_td.get("rowspan", "1"))
        if td_rowspan != next_td_rowspan:
            return conflict_time + 1

        td_colspan = int(td.get("colspan", "1"))
        next_td_colspan = int(next_td.get("colspan", "1"))

        td.attrs['colspan'] = next_td_colspan + td_colspan

        if 'border-right:none;' not in next_td['style']:
            style = td['style'].replace("border-right:none;", "")
            td['style'] = style

        for child in next_td.contents:
            td.append(child)
        next_td.decompose()
        return conflict_time

    def merge_vertical_td(self, td, td_dict):
        next_td = None
        index_x = -1
        index_y = -1
        for i, row in sorted(td_dict.items()):
            find_item = False
            for j, item in sorted(row.items()):
                if item is td:
                    find_item = True
                    index_x = i
                    index_y = j
                    break
            if find_item:
                break

        try:
            for k in range(index_x + 1, len(td_dict)):
                if td_dict[k][index_y] is not td:
                    next_td = td_dict[k][index_y]
                    break
        except Exception as err:
            self.logger.error(err, exc_info=True)

        if next_td is None or 'style' not in next_td.attrs or 'border-top:none;' not in next_td['style']:
            return 0
        if 'border-bottom:none;' in next_td['style']:
            merge_time = self.merge_vertical_td(next_td, td_dict)
        else:
            merge_time = 0

        td_colspan = int(td.get("colspan", "1"))
        next_td_colspan = int(next_td.get("colspan", "1"))
        if td_colspan != next_td_colspan:
            return merge_time
        td_rowspan = int(td.get("rowspan", "1"))
        next_td_rowspan = int(next_td.get("rowspan", "1"))

        td.attrs['rowspan'] = next_td_rowspan + td_rowspan
        if 'border-bottom:none;' not in next_td['style']:
            style = td['style'].replace("border-bottom:none;", "")
            td['style'] = style
        for child in next_td.contents:
            td.append(child)
        next_td.decompose()
        return merge_time + 1

    def format_html(self):
        try:
            # self.htmlString = str(self.soup_handler)
            # self.htmlString = self.soup_to_html()
            # 添加title
            # TODO ascii can't decode error
            if type(self.title) == str:
                title = self.title.decode('utf8')
            else:
                title = self.title
            new_tag = self.soup_handler.new_tag("div", type="pdf", title=title)  #
            self.soup_handler.body.wrap(new_tag)

            for x in self.soup_handler.findAll(["del"]):
                x.decompose()
            for x in self.soup_handler.findAll("script"):
                x.remove()

            # 在所有的都完成之后再做
            # ul, dl 去掉
            for x in self.soup_handler.findAll(["ul", "dl", "ol", "span", "b"]):
                x.unwrap()

            # li, dt/dd 去掉
            for x in self.soup_handler.findAll(["li", "dt", "dd"]):
                new_tag = self.soup_handler.new_tag("p")
                x.wrap(new_tag)
                x.unwrap()

            # # 将p下面的p保留
            # # 将table下面所有的p都去掉
            # 2019-01-18 移除此操作

            # # TODO 将 h6变成p ， 这里注释掉，6级标题就可以保留了
            # for x in self.soup_handler.findAll(['h6']):
            #     tag = self.soup_handler.new_tag("p")
            #     x.wrap(tag)
            #     x.unwrap()

            # 针对h1, 添加pdf_title，并删除h1标签
            for h1 in self.soup_handler.findAll("h1"):
                pre_nodes = h1.find_previous_siblings()
                status = True
                for pre_node in pre_nodes:
                    if pre_node.name == "p" and pre_node.text.strip() == "":
                        pass
                    else:
                        status = False
                        break

                if status:
                    new_tag = self.soup_handler.new_tag("div", type="pdf-title")
                    h1.wrap(new_tag)
                    h1.unwrap()
                else:
                    new_tag = self.soup_handler.new_tag("p")
                    h1.wrap(new_tag)
                    h1.unwrap()

            # TODO 根据 h1, h2, h3 等的header, 添加paragraph
            status = self.add_header_div()

            if not status:
                return None

            # 去掉无用的属性
            uselessLists = ['height', "id", "class", "bgcolor", "style", "width", "valign"]
            for uselessOne in uselessLists:
                for x in self.soup_handler.findAll(attrs={uselessOne: re.compile('.')}):
                    del x[uselessOne]

            for item in self.soup_handler.findAll("a"):
                item.unwrap()
            #
            self.get_clean_soup()

            for x in self.soup_handler.findAll(["table"]):
                # 如果table被p包括，则不作处理，否则添加<p>
                # TODO 正式上线时需要注释掉
                x["border"] = 'solid 1px'
                names = [t.name for t in x.parents]
                if "p" in names:  # or "table" in names:
                    continue
                # tag = self.soup_handler.new_tag("p")
                x.wrap(self.soup_handler.new_tag("p"))
                # x.replace_with(x.wrap(self.soup_handler.new_tag("p")))

            # 添加content div
            # 如果p的父节点有div，则不作处理
            for x in self.soup_handler.findAll(["p"]):
                skip_flag = False
                for t in x.parents:
                    leaf_name = t.name
                    # if leaf_name == "div" and t['type'] == "content":
                    if leaf_name == "div" and "type" in t.attrs.keys() and t['type'] == "content":
                        skip_flag = True
                        break
                if skip_flag:
                    continue
                tag = self.soup_handler.new_tag("div", type="content")
                x.wrap(tag)
                x.unwrap()

            # 删除h2, h3, h4, h5
            for x in self.soup_handler.findAll(self.head_levels):
                x.decompose()

            # for item in self.soup_handler.findAll(["hidden"]):
            for item in self.soup_handler.findAll(self.reserve):
                if "name" not in item.attrs:
                    item.decompose()
                else:
                    next_nodes = item.find_next_siblings()
                    if len(next_nodes) > 0:
                        for next_node in next_nodes:
                            if 'type' in next_node.attrs and next_node['type'] == 'content':
                                next_node.insert(0, item)
                                break
                    else:
                        new_tag = self.soup_handler.new_tag("div")
                        new_tag["type"] = 'content'
                        item.wrap(new_tag)

            # 将其余的页码替换成<a>标签
            # html = self.soup_to_html()
            # self.htmlString = html.replace("$$PAGE_", "<a name=\"").replace("_PAGE$$", "\"/>")
            # self.soup_handler = BeautifulSoup(self.htmlString, 'html.parser', from_encoding="utf-8")
            # 将<a>标签提前到父节点的前一个兄弟节点
            for item in self.soup_handler.find_all("a"):
                mark_name = item.attrs["name"]
                parent_node = item.parent
                new_tag = self.soup_handler.new_tag(self.reserve)
                new_tag["name"] = mark_name
                parent_node.insert_before(new_tag)
                item.decompose()

            try:
                # 去掉head
                # souphandler.head.decompose()
                # 去掉html 标签
                self.soup_handler.html.unwrap()
                # 去掉body 标签
                self.soup_handler.body.unwrap()
                # 标识sectionCode
                self.mark_section_code(self.soup_handler)
            except:
                pass
                # return html
        except Exception as err:
            self.logger.error(err, exc_info=True)

    def soup_to_html(self):
        # html = self.soup_handler.prettify('utf8')
        html = self.soup_handler.prettify(self.soup_handler.original_encoding)
        # html = self.soup_handler.encode()
        return html

    def str2date(self, s):
        # default = "20180101"
        s = s.replace(u'于', '')
        try:
            year = s.split(u'年')[0]
        except:
            return None
        try:
            month = s.split(u'年')[1].split(u'月')[0]
        except:
            return None
        try:
            day = s.split(u'月')[1].split(u'日')[0]  # 去掉中间十
        except:
            return None
        if (len(day)) > 2:
            day = day[0] + day[2]
        nm = {u'十': '10', u'○': '0', u'零': '0', u'一': '1', u'二': '2', u'三': '3', u'四': '4', u'五': '5',
              u'六': '6', u'七': '7', u'八': '8', u'九': '9', u'〇': '0'}
        year = ''.join([nm.get(i, i) for i in year])
        month = ''.join([nm.get(i, i) for i in month])
        day = ''.join([nm.get(i, i) for i in day])
        if (len(month)) == 3:
            month = month[0] + month[2]
        elif (len(month) == 1):
            month = '0' + month[0]
        if (len(day) == 3):
            day = day[0] + day[2]
        elif len(day) == 1:
            day = '0' + day[0]
        year = re.search('\d{4}', year).group()
        if re.search('\d', day) is None:
            # day = "01"
            return None
        # ndate = year + '-' + month + '-' + day;
        ndate = year + month + day
        return ndate

    def number_convert(self, chinese):

        CN_NUM = {
            u'〇': 0,
            u'一': 1,
            u'二': 2,
            u'三': 3,
            u'四': 4,
            u'五': 5,
            u'六': 6,
            u'七': 7,
            u'八': 8,
            u'九': 9,
            u'十': 9,

            u'零': 0,
            u'壹': 1,
            u'贰': 2,
            u'叁': 3,
            u'肆': 4,
            u'伍': 5,
            u'陆': 6,
            u'柒': 7,
            u'捌': 8,
            u'玖': 9,

            u'貮': 2,
            u'两': 2,
        }
        CN_UNIT = {
            u'十': 10,
            u'拾': 10,
            u'百': 100,
            u'佰': 100,
            u'千': 1000,
            u'仟': 1000,
            u'万': 10000,
            u'萬': 10000,
            u'亿': 100000000,
            u'億': 100000000,
            u'兆': 1000000000000,
        }
        lcn = list(chinese)
        unit = 0  # 当前的单位
        ldig = []  # 临时数组

        for key in lcn:
            value = CN_NUM.get(key, key)
            ldig.append(unicode(value))
        return "".join(ldig)

    def mark_section_code(self, souphandler):
        parent_tag = souphandler.find(name='div', attrs={'type': 'pdf'}, recursive=False)
        self.mark_section_code_recursive(parent_tag, None)

    def mark_section_code_recursive(self, cur_tag, parent_code):
        pgs = cur_tag.findAll(name="div", attrs={'type': 'paragraph'}, recursive=False)
        if pgs is not None and len(pgs) > 0:
            prefix = 'SectionCode_'
            if parent_code is not None and parent_code != '':
                prefix = parent_code + '-'
            level = 1
            for pg in pgs:
                section_code = prefix + str(level)
                pg.attrs['id'] = section_code
                self.mark_section_code_recursive(pg, section_code)
                level += 1

    # 将图片内嵌到html中
    def embed_image(self):
        dest_folder = os.path.join(os.path.dirname(self.htmlPath), self.htmlfoldername)
        # bs_handler = BeautifulSoup(self.htmlString, 'html.parser', from_encoding='utf-8')
        for img_tag in self.soup_handler.find_all("img"):
            origin_img = img_tag['src']
            if '/' in origin_img:
                origin_img = origin_img.split("/")[-1]
            if origin_img.replace(" ", "").startswith("data:"):
                continue
            img_path = os.path.join(dest_folder, origin_img)
            if not os.path.exists(img_path):
                continue
            img_handler = open(img_path, 'rb')
            img_contents = img_handler.read().encode("base64")
            img_handler.close()
            if ".jpg" in origin_img:
                img_tag['src'] = "data:image/jpg;base64,%s" % img_contents
            elif ".png" in origin_img:
                img_tag['src'] = "data:image/png;base64,%s" % img_contents
            elif ".gif" in origin_img:
                img_tag['src'] = "data:image/gif;base64,%s" % img_contents
            elif ".jpeg" in origin_img:
                img_tag['src'] = "data:image/jpeg;base64,%s" % img_contents
            elif ".bmp" in origin_img:
                img_tag['src'] = "data:image/bmp;base64,%s" % img_contents
            elif ".tif" in origin_img:
                img_tag['src'] = "data:image/tif;base64,%s" % img_contents
        # with open(self.htmlresultPath, "wb") as html_handler:
        #     html_handler.write(self.htmlString)

    def pre_format(self):
        # unwrap all the <div>
        for item in self.soup_handler.body.find_all("div"):
            item.unwrap()
        # while len(self.soup_handler.body.contents) == 1:
        #     self.soup_handler.body.contents[0].unwrap()

    def run(self):
        """
        :return:
        """
        self.start_timestamp = time.time()

        if len(self.htmlString) == 0:
            with open(self.htmlPath, 'rb') as htmlHandler:
                self.htmlString = htmlHandler.read()
        # https://www.zhihu.com/question/32980641
        # logger.debug("debug01")
        # self.soup_handler = BeautifulSoup(self.htmlString, 'html5lib', from_encoding="utf-8")
        # logger.debug("debug02")

        self.get_soup_handler()
        # 判断<body>的子结点是否只有一个， 如果是，则unwrap, 直到使得<body>子结点下是文本内容，不被其它标签包裹
        self.pre_format()

        if self.status is False:
            # how to track exception like: print self.message, as no attribute "message" at all
            # TODO how to track exception like:  self.message, as no attribute "message" at all
            self.logger.debug(
                "[ PostConverter.run ] status=%s message=%s detected, return" % (self.status, self.response_msg))
            return "", ""

        self.__format_ol()
        self.get_clean_soup()

        self.pre_prepare()

        self.dynamic_title()
        self.potential_title()

        if self.heading_set is not None:
            self.set_title_direct(self.heading_set.get("subtitles"), 2)
        else:
            self.soup_title()
            if self.title_soup.find('div') is not None:
                #
                self.set_title_tag(self.title_soup.find('div'), 2)
                # add special title to category soup
                self.set_special_title()

        for item in self.potential_title_tag_list:
            if item.name == self.potential_title_tag:
                item.name = 'p'

        # self.log_category(self.title_soup, "category")
        self.format_html()
        try:
            self.embed_image()
        except:
            pass
        self.output_result_htm()

        self.logger.debug("[ finish post convert ], costs: %s" % (self.end_timestamp - self.start_timestamp))
        self.logger.debug("[ finish post convert ], path: %s" % (self.htmlresultPath))
        # self.response_msg = "post convert done"
        return self.htmlString, self.htmlresultPath


class Converter(object):
    """
    # 两种情况 ， 一种是提供pdf的路径， 一种是url

    """

    def __init__(self, task):
        """

        :param task:  必须提供的key
        self.addressurl = task.get("s3_address")
        self.pdfaddress = task.get("pdf_address")

        """
        self.logger = logger

        # 用于返回转换结果状态及失败消息
        self.conclusion = {}
        self.logger.debug("[ Converter init ]")
        self.task = task
        self.start_timestamp = self.get_current_time()
        self.end_timestamp = self.get_current_time()
        self.time_consume = 0
        self.status = True
        self.solidstatus = True
        self.message = ""
        self.pure_image = False

        self.title = task.get("title")
        self.report_id = task.get("reportId")
        # logger.debug("[ convert ] started for task=%s" % taskId)
        self.taskId = task.get("taskId")
        self.pdf_size = task.get("pdfSize") or 1
        self.tool = task.get("tool")
        self.addressurl = task.get("s3_address")
        # self.addressurl = task.get("address")
        # self.pdfaddress = task.get("pdf_address")
        self.mode = task.get("mode")
        self.zsAutoCategory = task.get("zsAutoCategory")
        self.doc_type = task.get("docType") or 9  # ["doc_type"]
        self.heading_set = task.get("heading_set")  # ["heading_set"]
        # self.origin_dir = task.get("origin_dir")
        self.pdf_path = os.path.join(origin_dir, '%s.pdf' % self.taskId)
        self.dest_dir = dest_dir

        # 如果传入的参数中存在key = dst_filename, 则最终生成的htm结果的文件名为dst_filename.htm
        if task.get("dst_filename"):
            self.dest_file = os.path.join(self.dest_dir, "%s.htm" % task.get("dst_filename"))
        else:
            self.dest_file = os.path.join(self.dest_dir, "%s.htm" % self.taskId)
        self.basefile = os.path.basename(self.pdf_path)
        self.htmlString = ""
        self.continue_flag = True

        self.logger.debug("[ Converter init ] report_id = %s s3_address = %s" % (self.report_id, self.addressurl))
        self.logger.debug("[ Converter init ] pdf_path = %s dest_file = %s" % (self.pdf_path, self.dest_file))
        # self.heading_set = task.get("heading_set")  # ["heading_set"]

    def __exit__(self):
        self.logger.debug("[ current status ] %s %s" % (self.status, self.message))

    def file_init(self):
        """
        验证pdf文件是否存在， 不存在则下载, key = "pdf_path"
        获取文件大小
        :param task:
        :return:
        """
        if self.pdf_path is None or (not os.path.exists(self.pdf_path)):
            logger.info("task_init, pdf do not exist, downloading %s" % self.addressurl)
            status, message = util.get_s3_file(self.addressurl, self.pdf_path)
            if status is False:
                self.continue_flag = False
                self._update_status(False, False, message)

    def _is_continue(self):
        return self.continue_flag
        # continue even failed before post_convert
        # return True

    def _update_status(self, ifcontinue, status, message=""):
        self.continue_flag = ifcontinue
        self.status = status
        self.message = message
        self.conclusion = {
            'status': status,
            'message': message
        }
        # self.logger.debug("taskID is %s, status=%s, message=%s" % (self.taskId, self.status, self.message))
        self.logger.info("[ update_status ] taskID=%s message=%s status=%s pure_image=%s" % (
            self.taskId, self.message, self.status, self.pure_image))

    def _valid_path(self):
        if self._is_continue():
            if not os.path.exists(self.pdf_path):
                self._update_status(False, False, "pdf do not exists")

    def _valid_mode(self):
        if self._is_continue():
            if self.mode in [0, 1] and os.path.isfile(self.dest_file):
                self._update_status(False, True, "html already exists")

    def _valid_decrypt(self):
        if self._is_continue():
            try:
                tmp_pdf_file = str(self.pdf_path) + "_2"
                batcmd2 = 'decrypt%sqpdf --password= --decrypt "%s" "%s"' % (os.path.sep, self.pdf_path,
                                                                             tmp_pdf_file)
                subprocess.check_output(batcmd2, shell=True, stderr=subprocess.STDOUT, )
                # self.pdf_path = tmp_pdf_file
                shutil.move(tmp_pdf_file, self.pdf_path)  # 往ceph共享中写时被拒绝。 直接转换tmp.pdf
                self._update_status(True, True, "decrypt finished")
            except Exception as err:
                self._update_status(True, True, "decrypt failed")
                # self._update_status(False, False, "decrypt failed")
            finally:
                if os.path.exists(tmp_pdf_file):
                    os.remove(tmp_pdf_file)

    def _valid_contents(self):
        """To see if it is pure image"""
        if self._is_continue():
            self.pure_image = util.is_pure_image_pdf(self.pdf_path)
            # self._update_status(False, False, "Target pdf is pure image")

    def write_to_htm(self):
        try:
            # logger.info("get origin htm from java engine, path is %s " % self.dest_file)
            with open(self.dest_file, "w") as f:
                f.write(self.htmlString.encode('utf8'))
        except Exception as e:
            self._update_status(False, False,
                                "write_to_htm exception with dest file %s %s" % (self.dest_file, e))

    def _valid_pdf_2_html(self):
        # if code !=200:
        try:
            # "-Xmx2056m" 设置最大占用内存
            jpype.startJVM(jpype.getDefaultJVMPath(), "-Xms32m", "-Xmx2056m",
                           "-mx256m", "-Djava.class.path=%s" % pdfengine_path)
        except Exception as err:
            pass
            # self.logger.warning("_valid_pdf_2_html", err.message)
        # jpype.shutdownJVM()
        try:
            # 两种情况 ， 一种是提供pdf的路径， 一种是url
            # if self.addressurl is not None and len(self.addressurl) > 0:
            try:
                logger.info("pdf address %s" % (self.addressurl))
                encoded_url = self.addressurl[:self.addressurl.rfind("/")] + quote(
                    self.addressurl[self.addressurl.rfind("/"):].encode('utf-8'))
                if len(encoded_url) == 0:
                    encoded_url = self.pdf_path
                address = encoded_url
            # else:
            except:
                address = self.pdf_path
            # encoded_url = quote(self.addressurl.encode('utf-8'))
            # To call pdf-engine
            JDClass = jpype.JClass("com.datayes.pdf.util.HtmlOutputUtils")
            content = JDClass.toHtml(address)
            # batcmd2 = "java -jar pdf-engine.jar %s" % (self.addressurl)
            self.htmlString = content
            if is_empty_content(content):
                self._update_status(False, False, "_valid_pdf_2_html empty content from by pdf-engine")
                return False, content
            # pdfengine = True
            self.write_to_htm()
            self._update_status(True, True, "_valid_pdf_2_html done convert by pdf-engine")
            return True, content

        except Exception as err:
            # pdfengine = False
            self._update_status(False, False, "_valid_pdf_2_html exception with pdf-engine: %s" % err.message)
            # return False
            return False, ''
        #
        #
        # self.logger.info("[ destfile ]%s %s" % (self.dest_file, self.taskId))
        # if len(content) > 0:
        #     self.logger.info("[ content ]%s %s" % (self.taskId, content[:50]))
        #     try:
        #         with open(self.dest_file, "w") as f:
        #             f.write(content)
        #     except Exception, e:
        #         self._update_status(False, False,
        #                             "exception with dest file %s %s" % (self.dest_file, e))
        #     return True, content
        # else:
        #     return False, ''

    def _valid_convert(self):
        if self._is_continue():
            # contents = {}
            try:
                if self.tool == "office":
                    batcmd = '%s pdf %s FilteredHTML' % (self.task.get("exe_location_office"), self.pdf_path)
                    contents = subprocess.check_output(batcmd, shell=True, stderr=subprocess.STDOUT, )
                    contents = contents.strip().replace("\\", "/")
                    contents = util.handle_office_contents(contents, self.dest_dir)

                elif self.tool == "datayes_api":
                    self.logger.debug("start tool == datayes_api")
                    status, self.htmlString = self._valid_pdf_2_html()
                    if status:
                        self._update_status(True, True, "%s _valid_pdf_2_html get html done" % self.tool)
                    else:
                        self._update_status(False, False, "%s _valid_pdf_2_html get empty html" % self.tool)

            except Exception as err:
                self._update_status(False, False,
                                    "_valid_convert fail: %s" % (err.message or "none"))

    def _valid_code(self):
        if self._is_continue():
            bad_code_detector = ChDetector(self.dest_file)
            if 0 < bad_code_detector.ratio < 60:
                # shutil.move(dest_file, os.path.join(bad_case, "%s.htm" % taskId))
                # os.remove(dest_file)
                self._update_status(False, False, "tool convert done, but with unexpected special code.")
            else:
                self._update_status(True, True, "[ _valid_code pass ]")

    def _valid_post_convert(self):
        self.logger.debug("[ _valid_post_convert ]  _is_continue=%s" % self._is_continue())

        if self._is_continue():
            self.logger.debug("[ _valid_post_convert ] : doctype=%s, taskID is %s,"
                              " status=%s, message=%s" % (
                                  self.task.get("docType"), self.taskId, self.status, self.message))
            status = False
            try:
                postconverter = PostConverter(self.dest_file, self.taskId, self.title,
                                              self.task.get("zsAutoCategory"),
                                              self.task.get("heading_set"), self.htmlString, bsfeature='html5lib')
                self.htmlString, self.dest_file = postconverter.run()
                status = postconverter.convert_status
                self.message = postconverter.convert_msg
                self.logger.debug("[ _valid_post_convert done ] status=%s message=%s" % (status, self.message))
            except Exception as err:
                self.message = 'post converting fail'
                self.logger.debug("[ debug 5 ] post_convert new instance failed %s %s " % (self.taskId, err))

            if status:
                self.logger.debug("[ util.embed_image done ] dest_dir=%s" % (self.dest_dir))
                util.embed_image(self.taskId, self.dest_dir)
                self.logger.debug("[ util.embed_image done ]")
            # else:
            #     self.message = postconverter.convert_msg
            if postconverter.convert_msg == "empty html" and self.pure_image is True:
                # set status=False for pure image report
                self.message = "Target pdf is pure image"
            self.logger.debug("[ debug03 ] post_convert fail message %s " % (self.message))

            self._update_status(False, status, self.message)

    # def get_html(self):
    #     resp = requests.get("%s?url=%s" % (pdftohtmlprefix, self.addressurl))
    #     code, content = resp.status_code, resp.json()
    #     with open(self.dest_file, "a") as f:
    #         f.write(content)
    #     return code

    def converting(self):
        self.file_init()
        self._valid_path()
        self._valid_convert()
        self._valid_code()
        self._valid_post_convert()

        self.logger.debug("[ I am still ok here ]")
        self.end_timestamp = self.get_current_time()
        try:
            ELKlogger.info(self.convert_status)
        except Exception as err:
            self.logger.debug("[ class converter exception] err=%s" % (err.message))
        # self.logger.debug("[ converting done ] ", self.taskId, self.status, self.dest_file, self.message)
        return self.taskId, self.status, self.dest_file, self.message, self.htmlString

    def feedback(self):
        return self.status, self.dest_file, self.message

    def get_current_time(self):
        return time.time()

    def get_time_consumed(self):
        if type(self.end_timestamp) is not float and self.start_timestamp is not float:
            self.logger.warning("get_time_consumed the type of timestamp is unexpected")
            return 0.9
        return int((self.end_timestamp - self.start_timestamp + 0.01) * 1000)

    @property
    def convert_status(self):

        status_dict = {
            "status": self.status,
            "report_id": self.report_id,
            "title": self.title,
            "task_id": self.taskId,
            "message": self.message,
            "file_size": self.pdf_size,
        }

        if self.status:
            consume = self.get_time_consumed()
            speed = self.pdf_size / consume
            status_dict["convert_speed"] = speed
            status_dict["time_consumed"] = consume

        # 日志需要保留key的引号， 保证kibana可以正确解析。
        return json.dumps(status_dict, ensure_ascii=False)  # .replace('"', '')  # .decode("utf-8")
        """
        Key必须包含服务名称（module）、类型（type）、请求处理时长（cost）单位为毫秒、请求URL（url）非web服务不需要。
        """

    @property
    def pdf_size(self):
        return self._pdf_size

    @pdf_size.setter
    def pdf_size(self, value):
        self._pdf_size = value

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    @property
    def start_timestamp(self):
        return self._start_time

    @start_timestamp.setter
    def start_timestamp(self, value):
        self._start_time = value

    @property
    def end_timestamp(self):
        return self._end_time

    @end_timestamp.setter
    def end_timestamp(self, value):
        self._end_time = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value


if __name__ == "__main__":
    #
    s = """<html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        </meta>
        </head>
        <body>
        </body>
        </html>"""
    print(is_empty_content(s))
    s = """<h1>abc</h1><p>cdb</p>"""
    print(is_empty_content(s))
    #
    # missing title between < >
    task = {
        "tried_count": 1,
        "report_type": 1,
        "title": "华正新材2019年第一次临时股东大会决议公告",
        "tool": "datayes_api",
        "site": "sh",
        "publishDate": "2019-05-15",
        "processTime": 1562057472.296,
        "taskId": "0_dnm-UpBX4iWk_7kabVJw",
        "s3_address": "http://cluster-s3nginx-inner.datayes.com:80/pipeline/report/2019-05-15/20190515_184b8fa11a414d74685bf3b5146c8f1ad970ccd07.pdf",
        "reportId": 29668719,
        "insertTime": "2019-07-02 16:50:19",
        "progress": "done",
        "receiveTime": "2019-05-14 18:16:51",
        "machine": "10.22.220.181",
        "converting": 1562057434.012,
        "message": "",
        "uploading": 1562057448.31,
        "s3key": "/pipeline/data_report_html_e3d3974b2da51669e39f54761df6448f.html",
        "informed": 1562057472.296
    }

    converter = Converter(task)
    converter.converting()
    with open(converter.dest_file, 'r') as f:
        htmlstring = f.read()
    postconverter = PostConverter(converter.dest_file, task.get("taskId"), 'title',
                                  task.get("zsAutoCategory"),
                                  task.get("heading_set"), htmlstring)

    #
    converter = Converter(taskobj.task)
    converter.converting()

    # convertStatus.status = True
