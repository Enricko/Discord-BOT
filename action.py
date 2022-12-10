import json
import random
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "level_discord"
)

cursor = mydb.cursor(dictionary=True)

def level_up(id,xp_gain,name):
    cursor.execute(f"SELECT * FROM user WHERE id_user = {id}")
    user = cursor.fetchone()
    sql = f"UPDATE user SET xp = {int(user['xp']) + xp_gain} WHERE id_user = {id}"
    cursor.execute(sql)
    mydb.commit()
    cursor.execute(f"SELECT * FROM user WHERE id_user = {id}")
    user_up = cursor.fetchone() 
    need_xp = int(user_up['level']) * 100 * 1.35
    level_up = 0
    level_up_text = ''
    if user_up['xp'] >= need_xp:
        for x in range(10000):
            if int(user_up['xp']) - need_xp <= 0:
                break
            level_up += 1
            need_xp += (int(user_up['level']) + level_up) * 100 * 1.35
        sql_up = f"UPDATE user SET level = {int(user['level']) + level_up},xp = {(((int(user_up['level']) + level_up) * 100 * 1.35) - need_xp) + int(user_up['xp'])},attack = {user_up['attack'] + (level_up * 1)},defense = {user_up['defense'] + (level_up * 1)},max_health = {user_up['max_health'] + (level_up * 5)} WHERE id_user = {id}"
        # print(f"{((int(user_up['level']) + level_up) * 100 * 1.35) - need_xp} + {int(user_up['xp'])} = {(((int(user_up['level']) + level_up) * 100 * 1.35) - need_xp) + int(user_up['xp'])}")
        cursor.execute(sql_up)
        mydb.commit()
        level_up_text = ""if level_up <= 0 else f"\n**{name}** leveled up {level_up} times"
    return f"{level_up_text}"
    # print(id)
    # print(xp_gain)