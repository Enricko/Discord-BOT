import random
import mysql.connector
import discord
from discord.ext import commands
import action
import json

def run_discord_bot():
    TOKEN = 'OTEzNzgzNTMyMTg1MzU0MjYx.GdHpBW.YxbdM1AneC540-FePihIjoXWSrGQIGSCbOY_kU'
    prefix = "."
    client = commands.Bot(command_prefix=prefix,intents=discord.Intents.all())


    mydb = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "level_discord"
    )

    cursor = mydb.cursor(dictionary=True)

    @client.event
    async def on_ready():
        print(f'{client.user} in now running!')


    # @client.event
    # async def on_message(message):
        # if message.author == client.user:
        #     return
        # username = str(message.author)
        # user_message = str(message.content)
        # channel = str(message.channel)

        # if user_message[0] == ".": 
        #     m = user_message.replace(".","")
        #     print(f"{username} said: '{m}' ({channel})")
        #     await send_message(message,m)

    @client.command()
    async def start(ctx):
        with open('users.json', 'r') as f:
          user = json.load(f)
        member = ctx.author

        if str(member.id) in user['users']:
            await ctx.send("Your account has already existed!")
        elif str(member.id) not in user['users']:
            user['users'][str(member.id)] = {}
            user['users'][str(member.id)]['name'] =  member.name
            user['users'][str(member.id)]['level'] =  1
            user['users'][str(member.id)]['xp'] =  0
            user['users'][str(member.id)]['attack'] =  1
            user['users'][str(member.id)]['defense'] =  1
            user['users'][str(member.id)]['health'] =  100
            user['users'][str(member.id)]['max_health'] =  100

            with open('users.json', 'w') as f:
                json.dump(user, f, indent=4)
    
            await ctx.send(f"Welcome **{member.name}** to our game **Dungeon Adventure**!")

    @client.command()
    async def xp(ctx,a:int = 0, member:discord.member = None):
        if member == None:
            member = ctx.author

        id = member.id
        name = member.display_name
        
        if a <= 0:
            await ctx.send('Give some value of number!')
            return
        cursor.execute(f"SELECT * FROM user WHERE id_user = {id}")
        user = cursor.fetchone()
        xp_gain = a
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
        await ctx.send(f"**{name}** gain {xp_gain} xp {level_up_text}")

    @client.command(name= "profile",aliases=['p','pr'])
    async def profile(ctx,member : commands.MemberConverter = None):
        if member == None:
            member = ctx.author

        id = member.id
        name = member.display_name
        pfp = member.display_avatar

        with open('users.json', 'r') as f:
          data = json.load(f)

        if str(member.id) not in data['users']:
            await ctx.send(f'`{prefix}start` to register')
            return

        user = data['users'][str(id)]

        level_persentage = "0.00" if None else f"{((int(user['xp']) / (int(user['level']) * 100 * 1.35)) * 100):.2f}"
        xp_range = f"{int(user['xp'])} / {int(user['level'] * 100 * 1.35)}"

        embed = discord.Embed(title="Adventure Lover",colour=discord.Colour.random())
        embed.set_author(name=f"{name}")
        embed.set_thumbnail(url=f"{pfp}")
        embed.add_field(name="PROGRESS",value=f"**Level** : {user['level']} ({level_persentage}%)\n**Xp** : {xp_range}")
        embed.add_field(name="STATS",value=f"**:crossed_swords: Att** : {user['attack']}\n** :shield: Def** : {user['defense']}\n**:heart: Hp** : {user['health']} / {user['max_health']}",inline=False)

        await ctx.send(embed=embed)
        
    @client.command(name='hunt')
    async def hunt(ctx):
        member = ctx.author

        id = member.id
        name = member.display_name

        with open('users.json', 'r') as f:
          data = json.load(f)

        if str(member.id) not in data['users']:
            await ctx.send(f'`{prefix}start` to register')
            return
            
        user = data['users']

        level = user[str(id)]['level']
        xp = user[str(id)]['xp']
        attack = user[str(id)]['attack'] 
        defense = user[str(id)]['defense']
        health = user[str(id)]['health']
        max_health = user[str(id)]['max_health']

        file = open('monster.json','r')
        r = json.load(file)

        for i in r['data']['underground f1']:
            monster = (i[f'{(random.randint(1, 3))}'])

        if random.randint(monster['damage'] - 5,monster['damage'] + 5) - int(user[str(id)]['attack'] + user[str(id)]['defense'] * 0.95) <= 0:
            damage = 0
        else:
            damage = random.randint(monster['damage'] - 5,monster['damage'] + 5) - int(user[str(id)]['attack'] + user[str(id)]['defense'] * 0.95)
        health_taken = health - damage
        xp_gain = (random.randint(monster['xp'] - 5,monster['xp'] + 5))
        xp_earn = xp + xp_gain
        die = ''
        
        if int(user[str(id)]['health']) <= damage:
            if int(user[str(id)]['level']) > 1:
                level = user[str(id)]['level'] - 1
                xp_earn = 0
                attack = user[str(id)]['attack'] - 1
                defense = user[str(id)]['defense'] - 1
                health_taken = user[str(id)]['max_health'] - 5
                max_health = user[str(id)]['max_health'] - 5
            else:
                health_taken = user[str(id)]['max_health']
                xp_earn = 0
                
            die = (f"**{name}** died while hunting {(monster['name']).upper()}\nand lose a level")
            

        user[str(id)] = {}
        user[str(id)]['name'] = name
        user[str(id)]['level'] = level
        user[str(id)]['xp'] = xp_earn
        user[str(id)]['attack'] = attack
        user[str(id)]['defense'] = defense
        user[str(id)]['health'] =  health_taken
        user[str(id)]['max_health'] =  max_health

        with open('users.json', 'w') as f:
            json.dump(data, f, indent=4)

        level_up = action.level_up(id,xp_earn)

        await ctx.send(die if die != '' else f"**{name}** found and kill **{(monster['name']).upper()}** \nEarn {xp_gain} XP\nLost {damage} HP, remaining {health_taken}/{max_health} HP left {level_up}")

    @client.command(name='heal')
    async def heal(ctx):
        member = ctx.author

        id = member.id
        name = member.display_name

        with open('users.json', 'r') as f:
          data = json.load(f)

        if str(member.id) not in data['users']:
            await ctx.send(f'`{prefix}start` to register')
            return
            
        user = data['users']

        level = user[str(id)]['level']
        xp = user[str(id)]['xp']
        attack = user[str(id)]['attack'] 
        defense = user[str(id)]['defense']
        health = user[str(id)]['health']
        max_health = user[str(id)]['max_health']
        full = ''
        if health < max_health:
            health = max_health
            full = (f"**{name}** health been restored")

        user[str(id)] = {}
        user[str(id)]['name'] = name
        user[str(id)]['level'] = level
        user[str(id)]['xp'] = xp
        user[str(id)]['attack'] = attack
        user[str(id)]['defense'] = defense
        user[str(id)]['health'] =  health
        user[str(id)]['max_health'] =  max_health

        with open('users.json', 'w') as f:
            json.dump(data, f, indent=4)
        await ctx.send(full if full != '' else f"**{name}** health is maxed out")
        
        

    client.run(TOKEN)