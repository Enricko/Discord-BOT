import json
import random
import datetime
from datetime import datetime as date

def level_up(id,xp_gain,name):
    with open('json/users.json', 'r') as f:
        data = json.load(f)
    user = data['users']

    names = user[str(id)]['name']
    level = user[str(id)]['level']
    xp = user[str(id)]['xp']
    attack = user[str(id)]['attack'] 
    defense = user[str(id)]['defense']
    health = user[str(id)]['health']
    max_health = user[str(id)]['max_health']

    need_xp = (int(level) * 100 * 1.35) 

    level_up = 0
    level_up_text = ''
    if xp >= need_xp:
        for x in range(10000):
            if int(xp) - need_xp <= 0:
                break
            level_up += 1
            need_xp += (int(level) + level_up) * 100 * 1.35
            
        level_up_text = ""if level_up <= 0 else f"\n**{name}** leveled up {level_up} times"

        newData = {
            "level" : level + level_up,
            "xp" : (((level + level_up) * 100 * 1.35) - need_xp) + int(xp),
            "attack" : attack + (level_up * 1),
            "defense" : defense + (level_up * 1),
            "health" : health,
            "max_health" : max_health + (level_up * 5)
        }

        data['users'][str(id)].update(newData)

        with open('json/users.json', 'w') as f:
            json.dump(data, f, indent=4)
    return f"{level_up_text}"
    
def cooldown_error(cmd,cooldown):
    
    cd = {
        "hunt" : "You already hunting try again in",
        "cooldown" : "~=~",
        "dungeon" : "You already dungeon you need rest for"
    }
    cd_left = cooldown - datetime.datetime.now() 
    seconds = int(cd_left.seconds)
    days = seconds // 86400
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    text = f"{f'{days}d' if days > 0 else ''} {f'{hours}h' if hours > 0 else ''} {f'{minutes}m' if minutes > 0 else ''} {f'{seconds}s' if seconds > 0 else ''}"
    return f"{cd[cmd]} {text}"

def boost(boost = 'xp boost',id = 491905790966235136):
    with open('json/users.json', 'r') as f:
        data = json.load(f)
    user = data['users'][str(id)]

    with open('json/buff.json', 'r') as f:
        buff = json.load(f)

    with open('json/item.json', 'r') as f:
        item = json.load(f)
    buffItemSmall = item['data']['item']['consumables'][f"small {boost}"]['buff']['boost']
    buffItemMedium = item['data']['item']['consumables'][f"medium {boost}"]['buff']['boost']
    buffItemLarge = item['data']['item']['consumables'][f"large {boost}"]['buff']['boost']
    small = date.strptime(buff['data'][str(id)][boost]['small']['time'], '%Y-%m-%d %H:%M:%S')
    medium = date.strptime(buff['data'][str(id)][boost]['medium']['time'], '%Y-%m-%d %H:%M:%S')
    large = date.strptime(buff['data'][str(id)][boost]['large']['time'], '%Y-%m-%d %H:%M:%S')
    current = 0
    if datetime.datetime.now() <= small:
        current += buffItemSmall
    if datetime.datetime.now() <= medium:
        current += buffItemMedium
    if datetime.datetime.now() <= large:
        current += buffItemLarge
    
    return 1 + (current / 100)
boost()

