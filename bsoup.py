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