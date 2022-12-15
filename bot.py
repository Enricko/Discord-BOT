import random
import discord
from random import choices
from discord.ext import commands
from discord.ui import Button, View
import numpy as np
import json
import action
import asyncio

def run_discord_bot():
    TOKEN = 'OTEzNzgzNTMyMTg1MzU0MjYx.GZ8lzb.ZE6cA8Iw2uFM_PvXhQDvgXQsALa5ZJmjLJpwEY'
    prefix = "."
    client = commands.Bot(command_prefix=prefix,intents=discord.Intents.all())


    # mydb = mysql.connector.connect(
    #     host = "localhost",
    #     user = "root",
    #     password = "",
    #     database = "level_discord"
    # )

    # cursor = mydb.cursor(dictionary=True)

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
        with open('json/users.json', 'r') as f:
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
            user['users'][str(member.id)]['gold'] =  0
            user['users'][str(member.id)]['equipments'] = {}
            user['users'][str(member.id)]['equipments']['sword'] = None
            user['users'][str(member.id)]['equipments']['armor'] = None

            with open('json/users.json', 'w') as f:
                json.dump(user, f, indent=4)

            with open('json/inventory.json', 'r') as f:
                inv = json.load(f)
            
            inv['data'][str(member.id)] = {}
            inv['data'][str(member.id)]['equipments'] = {}
            inv['data'][str(member.id)]['items'] = {}
            inv['data'][str(member.id)]['consumables'] = {}

            with open('json/inventory.json','w') as i:
                json.dump(inv,i,indent=4)
    
            await ctx.send(f"Welcome **{member.name}** to our game **Dungeon Adventure**!")

    # @client.command()
    # async def xp(ctx,a:int = 0, member:discord.member = None):
        # if member == None:
        #     member = ctx.author

        # id = member.id
        # name = member.display_name
        
        # if a <= 0:
        #     await ctx.send('Give some value of number!')
        #     return
        # cursor.execute(f"SELECT * FROM user WHERE id_user = {id}")
        # user = cursor.fetchone()
        # xp_gain = a
        # sql = f"UPDATE user SET xp = {int(user['xp']) + xp_gain} WHERE id_user = {id}"
        # cursor.execute(sql)
        # mydb.commit()
        # cursor.execute(f"SELECT * FROM user WHERE id_user = {id}")
        # user_up = cursor.fetchone() 
        # need_xp = int(user_up['level']) * 100 * 1.35
        # level_up = 0
        # level_up_text = ''
        # if user_up['xp'] >= need_xp:
        #     for x in range(10000):
        #         if int(user_up['xp']) - need_xp <= 0:
        #             break
        #         level_up += 1
        #         need_xp += (int(user_up['level']) + level_up) * 100 * 1.35
        #     sql_up = f"UPDATE user SET level = {int(user['level']) + level_up},xp = {(((int(user_up['level']) + level_up) * 100 * 1.35) - need_xp) + int(user_up['xp'])},attack = {user_up['attack'] + (level_up * 1)},defense = {user_up['defense'] + (level_up * 1)},max_health = {user_up['max_health'] + (level_up * 5)} WHERE id_user = {id}"
        #     # print(f"{((int(user_up['level']) + level_up) * 100 * 1.35) - need_xp} + {int(user_up['xp'])} = {(((int(user_up['level']) + level_up) * 100 * 1.35) - need_xp) + int(user_up['xp'])}")
        #     cursor.execute(sql_up)
        #     mydb.commit()
        #     level_up_text = ""if level_up <= 0 else f"\n**{name}** leveled up {level_up} times"
        # await ctx.send(f"**{name}** gain {xp_gain} xp {level_up_text}")

    @client.command(name= "profile",aliases=['p','pr'])
    async def profile(ctx,member : commands.MemberConverter = None):
        if member == None:
            member = ctx.author

        id = member.id
        name = member.display_name
        pfp = member.display_avatar

        with open('json/users.json', 'r') as f:
          data = json.load(f)

        if str(member.id) not in data['users']:
            await ctx.send(f'`{prefix}start` to register')
            return

        user = data['users'][str(id)]

        level_persentage = "0.00" if None else f"{((int(user['xp']) / (int(user['level']) * 100 * 1.35)) * 100):.2f}"
        xp_range = f"{int(user['xp'])} / {int(user['level'] * 100 * 1.35)}"

        embed = discord.Embed(title="Adventure Lover",colour=discord.Colour.random())
        embed.set_author(name=f"{name}",icon_url=f"{pfp}")
        embed.set_thumbnail(url=f"{pfp}")
        embed.add_field(name="PROGRESS",value=f"**Level** : {user['level']} ({level_persentage}%)\n**Xp** : {xp_range}")
        embed.add_field(name="STATS",value=f"**:crossed_swords: Att** : {user['attack']}\n** :shield: Def** : {user['defense']}\n**:heart: Hp** : {user['health']} / {user['max_health']}",inline=False)

        await ctx.send(embed=embed)
        
    @client.command(name='hunt')
    async def hunt(ctx):
        member = ctx.author

        id = member.id
        name = member.display_name

        with open('json/users.json', 'r') as f:
          data = json.load(f)

        with open('json/inventory.json', 'r') as i:
            inv = json.load(i)

        with open('json/item.json', 'r') as i:
            item = json.load(i)

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
        gold = user[str(id)]['gold']

        file = open('json/monster.json','r')
        r = json.load(file)

        for i in r['data']['underground f1']:
            monster = (i[f'{(random.randint(1, 3))}'])

        if random.randint(monster['damage'] - 5,monster['damage'] + 5) - int(user[str(id)]['attack'] + user[str(id)]['defense'] * 0.95) <= 0:
            damage = 0
        else:
            damage = random.randint(monster['damage'] - 5,monster['damage'] + 5) - int(user[str(id)]['attack'] + user[str(id)]['defense'] * 0.95)
        health_taken = health - damage
        xp_gain = (random.randint(monster['xp'] - 5,monster['xp'] + 5))
        gold_gain = (random.randint(monster['gold'] - 7,monster['gold'] + 7))
        xp_earn = xp + xp_gain
        gold_earn = gold + gold_gain
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
            
        newData = {
            "level" : level,
            "xp" : xp_earn,
            "attack" : attack,
            "defense" : defense,
            "health" : health_taken,
            "max_health" : max_health,
            "gold" : gold_earn
        }

        data['users'][str(id)].update(newData)

        with open('json/users.json', 'w') as f:
            json.dump(data, f, indent=4)

        if die == '':
            rObtain = ''
            mDrops = ''
            mChance = ''
            droptext = ''
            with open('json/drops.json', 'r') as f:
                drop = json.load(f)

            if monster['name'] in drop['data']['monster']:
                # print(f"yes {monster['name']}")
                totalItem = 0
                for mDrop in drop['data']['monster'][monster['name']]:
                    # print(mDrop)
                    mDrops += f"{mDrop}-"
                    totalItem += 1
                mDrops = mDrops.split("-")
                mObtain = mDrops[random.randint(0,totalItem - 1)]
                mProb = random.randint(-50_000,50_000)
                mProbGet = random.randint(-50_000,50_000)
                mChance = drop['data']['monster'][monster['name']][mObtain]['chance']

                if mProb <= mProbGet + mChance and mProb >= mProbGet - mChance:
                    if mObtain in item['data']['item']['consumables']:
                        droptext += f"\n**{name}** obtained `{mObtain}{item['data']['item']['consumables'][mObtain]['icon']}`  from {monster['name']}"
                        typeDrop = "consumables"
                    elif mObtain in item['data']['item']['items']:
                        droptext += f"\n**{name}** obtained `{mObtain}{item['data']['item']['items'][mObtain]['icon']}`  from {monster['name']}"
                        typeDrop = "items"
                    qty = 1
                    if mObtain in inv['data'][str(member.id)][typeDrop]:
                        qty = inv['data'][str(member.id)][typeDrop][mObtain]['qty'] + 1
                    icon = item['data']['item'][typeDrop][mObtain]['icon']
                    inv['data'][str(member.id)][typeDrop][mObtain] = {}
                    inv['data'][str(member.id)][typeDrop][mObtain]['name'] = str(mObtain)
                    inv['data'][str(member.id)][typeDrop][mObtain]['icon'] = icon
                    inv['data'][str(member.id)][typeDrop][mObtain]['qty'] = qty
                    # inv.update(mInvDrop)
                    
                    with open('json/inventory.json', 'w') as f:
                        json.dump(inv, f, indent=4)

            for rDrop in drop['data']['random drop']:
                rChance = (drop['data']['random drop'][rDrop]['chance'])
                rProb = random.randint(-50_000,50_000)
                rProbGet = random.randint(-50_000,50_000)
                rObtain = rDrop
                if rProb <= rProbGet + rChance and rProb >= rProbGet - rChance:
                    if rObtain in item['data']['item']['consumables']:
                        droptext += f"\n**{name}** obtained `{rObtain}{item['data']['item']['consumables'][rObtain]['icon']}`"
                        rtypeDrop = "consumables"
                    elif rObtain in item['data']['item']['items']:
                        droptext += f"\n**{name}** obtained `{rObtain}{item['data']['item']['items'][rObtain]['icon']}`"
                        rtypeDrop = "items"
                    qty = 1
                    if rObtain in inv['data'][str(member.id)][rtypeDrop]:
                        qty = inv['data'][str(member.id)][rtypeDrop][rObtain]['qty'] + 1
                        print(qty)
                    icon = item['data']['item'][rtypeDrop][rObtain]['icon']
                    inv['data'][str(member.id)][rtypeDrop][rObtain] = {}
                    inv['data'][str(member.id)][rtypeDrop][rObtain]['name'] = str(rObtain)
                    inv['data'][str(member.id)][rtypeDrop][rObtain]['icon'] = icon
                    inv['data'][str(member.id)][rtypeDrop][rObtain]['qty'] = qty

                    with open('json/inventory.json', 'w') as f:
                        json.dump(inv, f, indent=4)

        level_up = action.level_up(id,xp_earn)

        await ctx.send(die if die != '' else f"**{name}** found and kill **{(monster['name']).upper()}** \nEarn {xp_gain} XP and {gold_gain} gold\nLost {damage} HP, remaining {health_taken}/{max_health} HP left {level_up} {droptext}")

    @client.command(name='heal')
    async def heal(ctx):
        member = ctx.author

        id = member.id
        name = member.display_name

        with open('json/users.json', 'r') as f:
          data = json.load(f)
          
        with open('json/inventory.json', 'r') as f:
          inv = json.load(f)

        if str(member.id) not in data['users']:
            await ctx.send(f'**{name}** `{prefix}start` to register')
            return

        user = data['users']

        health = user[str(id)]['health']
        max_health = user[str(id)]['max_health']
        text = f"**{name}** health is maxed out"
        if health < max_health:
            health = max_health
            text = (f"**{name}** health been restored")

        if "health potion" in inv['data'][str(id)]['consumables'] and inv['data'][str(id)]['consumables']['health potion']['qty'] > 0:

            invData = {
                "qty" : inv['data'][str(id)]['consumables']['health potion']['qty'] - 1,
            }
            inv['data'][str(id)]['consumables']['health potion'].update(invData)

            with open('json/inventory.json', 'w') as f:
                json.dump(inv, f, indent=4)
        else:
            await ctx.send(f"**{name}** You run out of health potion")
            return

        newData = {
            "health" : health,
            "max_health" : max_health
        }

        data['users'][str(id)].update(newData)

        with open('json/users.json', 'w') as f:
            json.dump(data, f, indent=4)
        await ctx.send(text)
        
    @client.command(name='equip')
    async def equip(ctx,*,arg):
        member = ctx.author

        id = member.id
        name = member.display_name

        with open('json/users.json', 'r') as f:
            data = json.load(f)
        user = data['users'][str(id)]

        with open('json/item.json', 'r') as i:
            item = json.load(i)

        if str(member.id) not in data['users']:
            await ctx.send(f'**{name}**`{prefix}start` to register')
            return

        add_attack = 0
        add_defense = 0
        type_item = 'sword' if 'sword' in arg else 'armor' 
        user_sword = user['equipments']['sword']
        user_armor = user['equipments']['armor']

        if user_sword == arg:
            await ctx.send(f"**{name}** You already equip `{arg}`")
            return

        if str(arg) in item['data']['item']['equipments'][type_item]:
            if 'sword' in arg:
                add_attack = item['data']['item']['equipments'][type_item][arg]['attack']
                if user_sword != None:
                    add_attack -= item['data']['item']['equipments'][type_item][user_sword]['attack']
                user_sword = arg
                text = f"Have equip `{arg}` and increase your attack :crossed_swords: by {item['data']['item']['equipments']['sword'][arg]['attack']}"
            elif 'armor' in arg:
                add_defense = item['data']['item']['equipments'][type_item][arg]['defense']
                if user_armor != None:
                    add_defense -= item['data']['item']['equipments'][type_item][user_armor]['defense']
                user_armor = arg
                text = f"Have equip `{arg}` and increase your defense :shield: by {item['data']['item']['equipments']['armor'][arg]['defense']}"
            
        else:
            text = f"**{name}** Um... We couldn`t find that item!"

        newData = {
            "attack" : user['attack'] + add_attack,
            "defense" : user['defense'] + add_defense,
            "equipments" :{
                "sword" : user_sword,
                "armor" : user_armor
            },
        }

        data['users'][str(id)].update(newData)

        with open('json/users.json', 'w') as f:
            json.dump(data, f, indent=4)

        await ctx.send(f"**{name}** {text}")

    # @client.command(name='inventory',aliases=['i','inv'])
    # async def equip(ctx):

    class Menu(View):

        @discord.ui.button(label="Equipmentss",style=discord.ButtonStyle.grey,emoji="⚔️")
        async def equipments(self, interaction: discord.Interaction, button: Button):
            embed = discord.Embed(color=discord.Color.random())
            embed.set_author(name=f'{interaction.user.name} All of your equipmentss!',icon_url=f"{interaction.user.display_avatar}\n")
            with open('json/inventory.json', 'r') as f:
                data = json.load(f) 
            e = data['data'][str(interaction.user.id)]['equipments']
            text = ''
            # print(str(interaction.user.id))
            # print(e)
            # print(len(e))
            if len(e) <= 0:
                text = "You dont have equipments, buy or craft equipments"
            for x in e:
                text += f"{e[x]['icon']} **{x}**\n"
            embed.add_field(name=f"`{prefix}equip [name equipments]` to equip",value=f"\n{text}")
            await interaction.response.edit_message(embed=embed)

        @discord.ui.button(label="Items",style=discord.ButtonStyle.grey,emoji="🎒")
        async def items(self, interaction: discord.Interaction, button: Button):
            embed = discord.Embed(color=discord.Color.random())
            embed.set_author(name=f'{interaction.user.name} All of your items!',icon_url=f"{interaction.user.display_avatar}\n")
            with open('json/inventory.json', 'r') as f:
                data = json.load(f) 
            e = data['data'][str(interaction.user.id)]['items']
            text = ''
            # print(str(interaction.user.id))
            # print(e)
            # print(len(e))
            if len(e) <= 0:
                text = "You dont have items, buy or craft items"
            for x in e:
                text += f"{e[x]['icon']} **{x}**\n"
            embed.add_field(name=f"You can use this item to craft in `{prefix}recipe`",value=f"\n{text}")
            await interaction.response.edit_message(embed=embed)

        @discord.ui.button(label="Consumables",style=discord.ButtonStyle.grey,emoji="🍎")
        async def consumables(self, interaction: discord.Interaction, button: Button):
            embed = discord.Embed(color=discord.Color.random())
            embed.set_author(name=f'{interaction.user.name} All of your consumables!',icon_url=f"{interaction.user.display_avatar}\n")
            with open('json/inventory.json', 'r') as f:
                data = json.load(f) 
            e = data['data'][str(interaction.user.id)]['consumables']
            text = ''
            # print(str(interaction.user.id))
            # print(e)
            # print(len(e))
            if len(e) <= 0:
                text = "You dont have consumables, buy or craft consumables"
            for x in e:
                text += f"{e[x]['icon']} **{x}** : {e[x]['qty']}\n"
            embed.add_field(name=f"You can eat or use and gain some buff",value=f"\n{text}")
            await interaction.response.edit_message(embed=embed)

    @client.command(name="inventory",aliases=['i','inv'])
    async def inventory(ctx):
        member = ctx.author

        id = member.id
        name = member.display_name

        with open('json/users.json', 'r') as f:
            data = json.load(f)

        if str(id) not in data['users']:
            await ctx.send(f'**{name}** `{prefix}start` to register')
            return
        embed = discord.Embed(color=discord.Color.random())
        embed.set_author(name='Select what you looking for!',icon_url=f"{member.display_avatar}")
        embed.add_field(name="Select",value=f"⚔️ Equipmentss\n🎒 Items\n🍎 Consumables")
        view = Menu(timeout=180)
        await ctx.send(embed=embed,view=view)

    @client.command(name="shop",aliases=['shops'])
    async def shop(ctx):
        member = ctx.author

        id = member.id
        name = member.display_name

        with open('json/users.json', 'r') as f:
            data = json.load(f)
        user = data['users'][str(id)]

        with open('json/shop.json', 'r') as sh:
            shop = json.load(sh)

        if str(member.id) not in data['users']:
            await ctx.send(f'**{name}** `{prefix}start` to register')
            return

        embed = discord.Embed(color=discord.Color.random())
        embed.set_author(name=f"Shop",icon_url=f"{member.display_avatar}\n")
        embed.add_field(name="\u200B",value=f"Buy anything? do {prefix}buy [name item]")

        if len(shop['data']) <= 0:
            embed.add_field(name=f"Sorry we dont sell anything yet",value=f":cry:")
        for x in shop['data']:
            embed.add_field(name=f"{shop['data'][x]['icon']} {x} | {shop['data'][x]['price']} :coin:",value=f"\n{shop['data'][x]['description']}")
        await ctx.send(embed=embed)
    
    def is_integer(n):
        try:
            float(n)
        except ValueError:
            return False
        else:
            return float(n).is_integer()
    @client.command(name="buy")
    async def buy(ctx,*,arg):
        member = ctx.author

        id = member.id
        name = member.display_name

        with open('json/users.json', 'r') as f:
            data = json.load(f)
        user = data['users'][str(id)]

        with open('json/inventory.json', 'r') as inv:
            inv = json.load(inv)

        with open('json/shop.json', 'r') as sh:
            shop = json.load(sh)

        with open('json/item.json', 'r') as i:
            item = json.load(i)

        if str(member.id) not in data['users']:
            await ctx.send(f'**{name}** `{prefix}start` to register')
            return
        split = arg.split()
        new_arg = str(arg).replace(f" {split[-1]}" if is_integer(split[-1]) else "",'')

        if new_arg in shop['data']:
            if shop['data'][new_arg]['type'] == "equipment":
                if new_arg in inv['data'][str(id)]['equipments'] and int(split[-1]) > 1: 
                    await ctx.send(f'**{name}** You already have the equipments')
                    return
                if int(split[-1]) > 1:
                    await ctx.send(f'**{name}** You can`t stack an equipments!')
                    return
                if 'sword' in new_arg:
                    inv['data'][str(member.id)]['equipments'][new_arg] = {}
                    inv['data'][str(member.id)]['equipments'][new_arg]['name'] = item['data']['item']['equipments']['sword'][new_arg]['name']
                    inv['data'][str(member.id)]['equipments'][new_arg]['icon'] = item['data']['item']['equipments']['sword'][new_arg]['icon']
                    inv['data'][str(member.id)]['equipments'][new_arg]['attack'] = item['data']['item']['equipments']['sword'][new_arg]['attack']
                elif 'armor' in new_arg:
                    inv['data'][str(member.id)]['equipments'][new_arg] = {}
                    inv['data'][str(member.id)]['equipments'][new_arg]['name'] = item['data']['item']['equipments']['sword'][new_arg]['name']
                    inv['data'][str(member.id)]['equipments'][new_arg]['icon'] = item['data']['item']['equipments']['sword'][new_arg]['icon']
                    inv['data'][str(member.id)]['equipments'][new_arg]['defense'] = item['data']['item']['equipments']['sword'][new_arg]['defense']
            elif shop['data'][new_arg]['type'] == "consumable":
                qty =(int(split[-1]) if is_integer(split[-1]) else 1)
                if new_arg in inv['data'][str(member.id)]['consumables']:
                    qty = (int(split[-1]) if is_integer(split[-1]) else 1) + (inv['data'][str(member.id)]['consumables'][new_arg]['qty'])
                icon = item['data']['item']['consumables'][new_arg]['icon']
                inv['data'][str(member.id)]['consumables'][new_arg] = {}
                inv['data'][str(member.id)]['consumables'][new_arg]['name'] = str(new_arg)
                inv['data'][str(member.id)]['consumables'][new_arg]['icon'] = icon
                inv['data'][str(member.id)]['consumables'][new_arg]['qty'] = qty
        else:
            await ctx.send('We can`t find what you looking for!')
            return
        
        total_price = (int(split[-1]) if is_integer(split[-1]) else 1) * shop['data'][new_arg]['price']
        if user['gold'] < total_price:
            await ctx.send(f"**{name}** Oops you short of gold {user['gold']}/{total_price}:coin:")
            return

        updateUser = {
            "gold": user['gold'] - total_price
        }
        data['users'][str(id)].update(updateUser)

        with open('json/users.json','w') as i:
            json.dump(data,i,indent=4)
            
        with open('json/inventory.json','w') as i:
            json.dump(inv,i,indent=4)
        
        await ctx.send(f"**{name}** bought `{arg}`")
                
    @client.command(name='use')
    async def use(ctx,*,arg):
        member = ctx.author

        id = member.id
        name = member.display_name

        with open('json/users.json', 'r') as f:
            data = json.load(f)
        user = data['users'][str(id)]

        with open('json/inventory.json', 'r') as inv:
            inv = json.load(inv)

        with open('json/shop.json', 'r') as sh:
            shop = json.load(sh)

        with open('json/item.json', 'r') as i:
            item = json.load(i)

        if str(member.id) not in data['users']:
            await ctx.send(f'**{name}** `{prefix}start` to register')
            return
        split = arg.split()
        new_arg = str(arg).replace(f" {split[-1]}" if is_integer(split[-1]) else "",'')
        if new_arg in inv['data'][str(id)]['consumables']:
            if inv['data'][str(id)]['consumables'][new_arg]['qty'] <= 0:
                text = f"**{name}** Oops you dont have that item"
            if item['data']['item']['consumables'][new_arg]['type'] == 'chest':
                totalItem = random.randint(item['data']['item']['consumables'][new_arg]['min_drop'] * (int(split[-1]) if is_integer(split[-1]) else 1),item['data']['item']['consumables'][new_arg]['max_drop'] * (int(split[-1]) if is_integer(split[-1]) else 1))
                print(totalItem)
                dropUse = item['data']['item']['consumables'][new_arg]['use']
                dropProb = ''
                dropItemChance = ''
                resultDropChest = ''
                resultDropValue = ''
                noCount = 0
                for x in dropUse.keys():
                    noCount += 1
                    dropProb += f"{x}{'' if noCount == len(dropUse) else '-'}"
                    dropItemChance += f"{dropUse[x] / 100_000}{'' if noCount == len(dropUse) else '-'}"

                dropItemChance = dropItemChance.split("-")
                drop = np.array(dropItemChance,dtype=np.float32)

                resultTotal = choices(population=dropProb.split("-"), weights=drop,k=int(totalItem))

                noCount1 = 0
                for i in dropProb.split("-"):
                    noCount1 += 1
                    resultDropChest += f"{i}{'' if noCount1 == len(dropProb.split('-')) else '-'}"
                    resultDropValue += f"{resultTotal.count(i)}{'' if noCount1 == len(dropProb.split('-')) else '-'}"
                # print(dropItemChance)
                # print(resultTotal)
                # print(resultDropValue)
                
                text = 'hai'
        await ctx.send(text)


    client.run(TOKEN)