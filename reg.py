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

