import json
import random

# mydb = mysql.connector.connect(
#     host = "localhost",
#     user = "root",
#     password = "",
#     database = "level_discord"
# )

# cursor = mydb.cursor(dictionary=True)

def level_up(id,xp_gain):
    with open('json/users.json', 'r') as f:
        data = json.load(f)
    user = data['users']

    name = user[str(id)]['name']
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
    # return 
    # print(id)
    # print(xp_gain)