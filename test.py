from random import choices
import random
import json
import datetime
import time
import locale
from datetime import datetime as date
import numpy as np

# print("${:,}".format(1231321231231))
# obj  = json.load(open("json/shop.json"))

# for i in obj['data']:
#     if i == "wooden sword":
#         print(obj["data"][i])
#         del obj["data"][i]
#         break
#     # print(obj["data"][i])
#     # print(obj["data"][i])

# # Output the updated file with pretty JSON                                      
# open("json/shop.json", "w").write(
#     json.dumps(obj, sort_keys=True, indent=2)
# )
# seconds = 1929123919
# days = seconds // 86400
# hours = (seconds % 86400) // 3600
# minutes = (seconds % 3600) // 60
# seconds = seconds % 60

# totalBuff = f"{f'{days}d' if days > 0 else ''}{f'{hours}h' if hours > 0 else ''}{f'{minutes}m' if minutes > 0 else ''}{f'{seconds}s' if seconds > 0 else ''}"
# print(totalBuff)      
# xy = []
# for d in range(20):
#     xy += [[random.randint(0,9),random.randint(0,9)]]
# if [5,5] in xy:
#     print(xy)
text = ''
# for y in range(9):
#     text += '\n'
#     for x in range(9):
#         text += f"[{x},{y}],"
knockback = [[0,0],[1,0],[2,0],[3,0],[4,0],[5,0],[6,0],[7,0],[8,0],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[0,8],[1,8],[2,8],[3,8],[4,8],[5,8],[6,8],[7,8],[8,8],[8,1],[8,2],[8,3],[8,4],[8,5],[8,6],[8,7]]

# for x in knockback:
#     print(x[0])
x = {
    'item' : 1,
    'data':5
}
for t,y in x.items():
    print(t,y)
