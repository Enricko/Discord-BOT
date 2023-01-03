from random import choices
import random
import json
import datetime
import time
import locale
from datetime import datetime as date
import numpy as np

# # print("${:,}".format(1231321231231))
# obj  = json.load(open("json/bossraidBosses.json"))

# le = random.randint(0,len(obj['data'])-1)
# for i,l in zip(obj['data'],range(len(obj['data']))):
#     print(l)
#     print(le)
#     if l == le:
#         print(obj["data"][i])
#         break
    # print(obj["data"][i])
    # print(obj["data"][i])

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
a = "1-1-2"
b = a.split('-')
b.append('5')
print(1000 // 100 >= 2)