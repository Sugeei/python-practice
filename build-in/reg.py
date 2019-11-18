import re

str = """
author = {abc, efg, dge,    
bbb,nnn
mmmm
},
title = { the tile is }
"""

pattern = "author//s+=//s+"
print(re.search(pattern, str))
# 对换行的识别不太友好

# https://www.cnblogs.com/dreamer-fish/p/5282679.html
# ‘(?:)’ 无捕获组
text = '1.2.3.4.5'
matches = re.findall('\d+(?:\.\d+)+', text)  # 0.13%
