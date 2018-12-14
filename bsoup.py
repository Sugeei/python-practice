# coding=utf-8
from bs4 import BeautifulSoup

markup = '<a href="http://example.com/">I linked to ' \
         '<i>example.com</i>' \
         '</a>'

soup = BeautifulSoup(markup, 'lxml')
tag = soup.new_tag("p")
tag.string = "to insert"

soup.a.insert_after(tag)
print soup
# <html>
# <body>
# <a href="http://example.com/">I linked to
# <i>example.com</i>
# </a>
# <p>to insert</p>
# </body>
# </html>

tag = soup.new_tag("p")
tag.string = "to append"

soup.a.append(tag)
print soup
# <html>
# <body>
# <a href="http://example.com/">I linked to
# <i>example.com</i>
# <p>to append</p>
# </a>
# <p>to insert</p>
# </body>
# </html>


html_doc = """
            <div>
                <p class="story">Once upon a time there were three little sisters; and their names were
                    <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
                    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
                    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
                    and they lived at the bottom of a well.
                </p>
                <p class="story">...</p>
            </div>
           """
soup = BeautifulSoup(html_doc, 'lxml')
if soup.a is not None:
    print(soup.a)

if soup.span is None:
    print(soup.span)


# # 根据标题层级关系构建一棵dom树
# # 将 title list 做为入参
# # 判断有的内容是正文还是目录， 看这些条目是否在同一页
# def dom_tree_title(self, title_list):
#     """
#     构建的目录树结构示例：
#     <p>
#         <div class_="5">
#             <p class_="5" href="51" id="0">第一节释义</p>
#             <p class_="5" href="54" id="1">第二节概览
#                 <div class_="14">
#                     <p class_="14" href="55" id="0">一、发行人简介</p>
#                     <p class_="14" href="56" id="1">二、发行人控股股东和实际控制人简介</p>
#                     <p class_="14" href="57" id="2">三、发行人主要财务数据及财务指标
#                         <div class_="18"><p class_="18" href="58" id="0">（一）合并资产负债表主要数据</p><p class_="18" href="59" id="1">（二）合并利润表主要数据</p><p class_="18" href="60" id="2">（三）合并现金流量表主要数据</p><p class_="18" href="61" id="3">（四）主要财务指标</p></div>
#                     </p>
#                 </div>
#             </p>
#             <p class_="5" href="60" id="2">第三节</p>
#         </div>
#     </p>
#     结构说明：
#         1. 每个标题包上<p>标签
#         2. 同级的所有目录外层包上<div>
#         3. 次一级目录作为兄弟结点与其父级标题放在同一个<p>标签中
#     :param title_list:
#     :return:
#     """
#     if len(title_list) == 0:
#         return None
#     title_soup = BeautifulSoup("<body><p></p></body", 'lxml', from_encoding="utf-8")
#     soup = title_soup
#     next_idx = 0
#     next_gid = -1
#     for i, node in enumerate(title_list):
#         if i == 51:  # for debug
#             pass
#         if i == 582:  # for debug
#             pass
#         if i == 510:  # for debug
#             pass
#         gid, idx, mark = self.identify_group(node)
#         if gid >= 0:  # or node in special_titles:
#             title_tag = title_soup.new_tag("p", class_=gid, id=idx, href=i)
#             title_tag.string = node
#             if idx == 0:
#                 new_tag = title_soup.new_tag("div", class_=gid)
#                 title_soup.find_all('p')[-1].append(new_tag)
#                 soup = new_tag
#                 next_idx = 1
#                 next_gid = gid
#                 soup.append(title_tag)
#                 # self.logger.info(
#                 #     "dom_tree_title (gid=%s, idx=%s, mark=%s) for node :%s, expect next : next_id=%s, next_gid=%s" % (
#                 #         gid, idx, mark, node, next_idx, next_gid))
#             elif gid == next_gid and idx == next_idx:
#                 # soup相当于一个动态的指针， 它指向当前目录组的<div>标签。
#                 # 这样append才能将title_tag放置到正确的位置
#                 soup.append(title_tag)
#                 next_idx += 1
#                 # next_gid = gid
#                 # self.logger.info(
#                 #     "dom_tree_title (gid=%s, idx=%s, mark=%s) for node :%s, expect next : next_id=%s, next_gid=%s" % (
#                 #         gid, idx, mark, node, next_idx, next_gid))
#             else:
#                 # 分支走到这里需要先保存next_idx 与next_gid的值，
#                 # 如果此分支未找到适配的位置说明此节点的值有问题，属于需要舍弃的
#                 # 那么可以在向上搜寻结束后仍然回到上一个结点的下一个期待值上
#                 # t_next_idx = next_idx
#                 # t_next_gid = next_gid
#
#                 # 当前结点为上一个结点的父级的后续结点时，需要用find_all去查找到距离最近的且满足条件{"class_":gid, "id":idx-1}的结点
#                 # 判断他们为同一组目录的前后两个标题
#                 # 当前结点为上面的例子中的<p class_="5" href="60" id="2">第三节</p>时，会走到本分支进行处理
#                 matches = title_soup.find_all('p', attrs={"class_": gid, "id": idx - 1})
#                 if len(matches) > 0:
#                     targetnode = matches[-1]
#                     # 更严格的，需要判断找到的targetnode没有跟当前结点相同标记的兄弟结点
#                     if targetnode.find_next_sibling('p', attrs={"class_": gid, "id": idx}) is None:
#                         targetnode.insert_after(title_tag)
#                         # 这里需要调整soup指针的指向位置，将其指向父级的<div>标签
#                         soup = targetnode.parent
#                         next_idx = idx + 1
#                         next_gid = gid
#                 #
#                 # for prenode in soup.parents:
#                 #     if prenode.name == "body":
#                 #         break
#                 #     if prenode is not None and prenode.name == 'div' and prenode.attrs["class_"] == gid:
#                 #         soup = prenode
#                 #         last_child = prenode.find_all("p", recursive=False)[-1]
#                 #         next_idx = last_child["id"] + 1
#                 #         next_gid = gid
#                 #         if next_idx == idx:
#                 #             prenode.append(title_tag)
#                 #             next_idx = idx + 1
#                 #             next_gid = gid
#                 #             soup = prenode
#                 #             self.logger.info(
#                 #                 "dom_tree_title (gid=%s, idx=%s, mark=%s) for node :"
#                 #                 "%s, expect next : next_id=%s, next_gid=%s"
#                 #                 % (gid, idx, mark, node, next_idx, next_gid))
#                 #
#                 #             break
#                 #         else:
#                 #             pass
#     return title_soup
