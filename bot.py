import random
import datetime
from datetime import datetime as date
import discord
import locale
import time
from random import choices
from discord.ext import commands
from discord.ui import Button, View
import numpy as np
import json
import action
import asyncio


def run_discord_bot():
    TOKEN = 'OTEzNzgzNTMyMTg1MzU0MjYx.GJ135t.mbxqzEjfEwjy89ydFizD4YrOtKBQ7gtJ4xinn0'
    prefix = "."
    client = commands.Bot(command_prefix=prefix,intents=discord.Intents.all())
    client.remove_command('help')


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


    @client.event
    async def on_command_error(ctx,error):
        id = ctx.author.id
        user = ctx.author.display_name
        if isinstance(error,commands.CommandOnCooldown):
            seconds = int(error.retry_after)
            days = seconds // 86400
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60
            cooldown = f"{f'{days}d' if days > 0 else ''}{f'{hours}h' if hours > 0 else ''}{f'{minutes}m' if minutes > 0 else ''}{f'{seconds}s' if seconds > 0 else ''}"
            # msg = f"**<@{id}>** Still on cooldown, Please try again in {cooldown}"
            msg = f"**<@{id}>** Slowdown, try again in 1 seconds"
            await ctx.send(msg)

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

            with open('json/cooldown.json', 'r') as f:
                cool = json.load(f)
            
            cool['data'][str(member.id)] = {}
            cool['data'][str(member.id)]['hunt'] = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            # cool['data'][str(member.id)][''] = {}
            # cool['data'][str(member.id)][''] = {}

            with open('json/cooldown.json','w') as i:
                json.dump(cool,i,indent=4)

            with open('json/buff.json', 'r') as f:
                buff = json.load(f)

            buff = ['drop boost','xp boost','gold boost']
            for x in buff:
                buff['data'][str(member.id)] = {}
                buff['data'][str(member.id)][x] = {}
                buff['data'][str(member.id)][x]['small'] = {}
                buff['data'][str(member.id)][x]['small']['time'] = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                
                buff['data'][str(member.id)] = {}
                buff['data'][str(member.id)][x] = {}
                buff['data'][str(member.id)][x]['medium'] = {}
                buff['data'][str(member.id)][x]['medium']['time'] = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                
                buff['data'][str(member.id)] = {}
                buff['data'][str(member.id)][x] = {}
                buff['data'][str(member.id)][x]['large'] = {}
                buff['data'][str(member.id)][x]['large']['time'] = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

            with open('json/buff.json','w') as i:
                json.dump(buff,i,indent=4)
            await ctx.send(f"Welcome **{member.name}** to our game **Dungeon Adventure**!")

    @client.command(name="help",aliases=['h'])
    @commands.cooldown(3,1,commands.BucketType.user)
    async def help(ctx,*,arg):
        member = ctx.author

        id = member.id
        name = member.display_name

        mention = f"<@{id}>"

        with open('json/users.json', 'r') as f:
            data = json.load(f)
        user = data['users'][str(id)]

        with open('json/inventory.json', 'r') as inv:
            inv = json.load(inv)

        with open('json/help.json', 'r') as h:
            help = json.load(h)
        help = help['data']
        commands = ''
        for x in help['commands']:
            if arg in help['commands'][x]:
                commands = x
            else:
                commands = x
        if arg in help['commands'][commands] or arg in help['items']:
            if arg in help['commands'][commands]:
                val = help['commands'][commands][arg]
            elif arg in help['items']:
                val = help['items'][arg]
            embed = discord.Embed(color=discord.Colour.random())
            embed.add_field(name=f"{arg}".title(),value=f"{val['description']}")
            embed.set_footer(text=f"if this not what you looking for see all command by using `{prefix}help`")
            await ctx.send(embed=embed)
            return
        else:
            await ctx.send(f"I could not find what help you looking for \ntry finding your help with `{prefix}help`")

    @client.command(name= "profile",aliases=['p','pr'])
    @commands.cooldown(3,1,commands.BucketType.user)
    async def profile(ctx,member : commands.MemberConverter = None):
        if member == None:
            member = ctx.author

        id = member.id
        name = member.display_name
        pfp = member.display_avatar

        with open('json/users.json', 'r') as f:
          data = json.load(f)

        with open('json/item.json', 'r') as f:
          item = json.load(f)

        if str(member.id) not in data['users']:
            await ctx.send(f'`{prefix}start` to register')
            return

        user = data['users'][str(id)]
        icon_eq = item['data']['item']['equipments']

        level_persentage = "0.00" if None else f"{((int(user['xp']) / (int(user['level']) * 100 * 1.35)) * 100):.2f}"
        xp_range = f"{int(user['xp'])} / {int(user['level'] * 100 * 1.35)}"

        gold = "{:,}".format(user['gold'])

        embed = discord.Embed(title="Adventure Lover",colour=discord.Colour.random())
        embed.set_author(name=f"{name}",icon_url=f"{pfp}")
        embed.set_thumbnail(url=f"{pfp}")
        embed.add_field(name="PROGRESS",value=f"**Level** : {user['level']} ({level_persentage}%)\n**Xp** : {xp_range}")
        embed.add_field(name="STATS",value=f"**:crossed_swords: Att** : {user['attack']}\n** :shield: Def** : {user['defense']}\n**:heart: Hp** : {user['health']} / {user['max_health']}")
        embed.add_field(name="EQUIPMENTS",value=f"**{('Sword not equip' if user['equipments']['sword'] == None else icon_eq['sword'][user['equipments']['sword']]['icon'])}**\n**{('Armor not equip' if user['equipments']['armor'] == None else icon_eq['armor'][user['equipments']['armor']]['icon'])}**")
        embed.add_field(name="CURRENCY",value=f"**:coin: Gold** : {gold}\n")

        await ctx.send(embed=embed)
        
    @client.command(name='hunt')
    @commands.cooldown(3,1,commands.BucketType.user)
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

        with open('json/cooldown.json', 'r') as c:
            cool = json.load(c)

        if str(member.id) not in data['users']:
            await ctx.send(f'`{prefix}start` to register')
            return
        
        cooldown = date.strptime(cool['data'][str(id)]['hunt'], '%Y-%m-%d %H:%M:%S')
        cooldown_total = datetime.timedelta(seconds=60)
        if cooldown > datetime.datetime.now():
            await ctx.send(action.cooldown_error('hunt',cooldown))
            return

        cool['data'][str(member.id)] = {}
        cool['data'][str(member.id)]['hunt'] = f"{(datetime.datetime.now() + cooldown_total).strftime('%Y-%m-%d %H:%M:%S')}"
        
        with open('json/cooldown.json', 'w') as f:
            json.dump(cool, f, indent=4)
        
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
        xp_gain = int((random.randint(monster['xp'] - 5,monster['xp'] + 5)) * action.boost('xp boost',str(id)))
        gold_gain = int((random.randint(monster['gold'] - 7,monster['gold'] + 7)) * action.boost('gold boost',str(id)))
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
                        droptext += f"\n**{name}** obtained `{mObtain}` {item['data']['item']['consumables'][mObtain]['icon']}  from {monster['name']}"
                        typeDrop = "consumables"
                    elif mObtain in item['data']['item']['items']:
                        droptext += f"\n**{name}** obtained `{mObtain}` {item['data']['item']['items'][mObtain]['icon']}  from {monster['name']}"
                        typeDrop = "items"
                    qty = 1
                    if mObtain in inv['data'][str(member.id)][typeDrop]:
                        qty = inv['data'][str(member.id)][typeDrop][mObtain]['qty'] + 1
                    inv['data'][str(member.id)][typeDrop][mObtain] = {}
                    inv['data'][str(member.id)][typeDrop][mObtain]['name'] = str(mObtain)
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
                        droptext += f"\n**{name}** obtained `{rObtain}` {item['data']['item']['consumables'][rObtain]['icon']}"
                        rtypeDrop = "consumables"
                    elif rObtain in item['data']['item']['items']:
                        droptext += f"\n**{name}** obtained `{rObtain}` {item['data']['item']['items'][rObtain]['icon']}"
                        rtypeDrop = "items"
                    qty = 1
                    if rObtain in inv['data'][str(member.id)][rtypeDrop]:
                        qty = inv['data'][str(member.id)][rtypeDrop][rObtain]['qty'] + 1
                    inv['data'][str(member.id)][rtypeDrop][rObtain] = {}
                    inv['data'][str(member.id)][rtypeDrop][rObtain]['name'] = str(rObtain)
                    inv['data'][str(member.id)][rtypeDrop][rObtain]['qty'] = qty

                    with open('json/inventory.json', 'w') as f:
                        json.dump(inv, f, indent=4)

        level_up = action.level_up(id,xp_earn)

        await ctx.send(die if die != '' else f"**{name}** found and kill **{(monster['name']).upper()}** \nEarn {xp_gain} XP and {gold_gain} gold\nLost {damage} HP, remaining {health_taken}/{max_health} HP left {level_up} {droptext}")

    @client.command(name='heal')
    @commands.cooldown(3,1,commands.BucketType.user)
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
            text = (f"**<@{id}>** health been restored")

        if "health potion" in inv['data'][str(id)]['consumables'] and inv['data'][str(id)]['consumables']['health potion']['qty'] > 0:

            invData = {
                "qty" : inv['data'][str(id)]['consumables']['health potion']['qty'] - 1,
            }
            inv['data'][str(id)]['consumables']['health potion'].update(invData)

            if inv['data'][str(id)]['consumables']['health potion']['qty'] - 1 <= 0:
                del inv['data'][str(id)]['consumables']['health potion']

            with open('json/inventory.json', 'w') as f:
                json.dump(inv, f, indent=4)
        else:
            await ctx.send(f"**<@{id}>** You run out of health potion")
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
    @commands.cooldown(3,1,commands.BucketType.user)
    async def equip(ctx,*,arg):
        member = ctx.author

        id = member.id
        name = member.display_name

        with open('json/users.json', 'r') as f:
            data = json.load(f)
        user = data['users'][str(id)]

        with open('json/item.json', 'r') as i:
            item = json.load(i)

        with open('json/inventory.json', 'r') as i:
            inv = json.load(i)


        if str(member.id) not in data['users']:
            await ctx.send(f'**{name}**`{prefix}start` to register')
            return

        if arg not in inv['data'][str(id)]['equipments']:
            await ctx.send(f"**{name}** Oops you doesn`t own that item")
            return

        add_attack = 0
        add_defense = 0
        type_item = 'sword' if 'sword' in arg else 'armor' 
        user_sword = user['equipments']['sword']
        user_armor = user['equipments']['armor']

        if user_sword == arg:
            await ctx.send(f"**{name}** You already equip `{arg}`")
            return
        elif user_armor == arg:
            await ctx.send(f"**{name}** You already equip `{arg}`")
            return

        if str(arg) in item['data']['item']['equipments'][type_item]:
            if str(arg) not in inv['data'][str(id)]['equipments']:
                text = f"Um... you dont have that item check your {prefix}inv"
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
            text = f" Um... We couldn`t find that item check your {prefix}inv"

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
        def __init__(self, author):
            self.author = author
            super().__init__()

        @discord.ui.button(label="Equipments",style=discord.ButtonStyle.grey,emoji="⚔️")
        async def equipments(self, interaction: discord.Interaction, button: Button):
            embed = discord.Embed(color=discord.Color.random())
            embed.set_author(name=f'{interaction.user.name} All of your equipments!',icon_url=f"{interaction.user.display_avatar}\n")
            with open('json/inventory.json', 'r') as f:
                data = json.load(f) 
            with open('json/item.json', 'r') as f:
                item = json.load(f) 
            item = item['data']['item']['equipments']
            e = data['data'][str(interaction.user.id)]['equipments']
            text = ''
            if len(e) <= 0:
                text = "You dont have equipments, buy or craft equipments"
            for x in e:
                split = x.split(" ")
                text += f"{item[str(split[-1])][x]['icon']} **{x}**\n"
            embed.add_field(name=f"`{prefix}equip [name equipments]` to equip",value=f"\n{text}")
            embed.set_footer(text=f"If you need some money just do `{prefix}sell [item name]`")
            await interaction.response.edit_message(embed=embed)
            self.disabled = True

        @discord.ui.button(label="Items",style=discord.ButtonStyle.grey,emoji="🎒")
        async def items(self, interaction: discord.Interaction, button: Button):
            embed = discord.Embed(color=discord.Color.random())
            embed.set_author(name=f'{interaction.user.name} All of your items!',icon_url=f"{interaction.user.display_avatar}\n")
            with open('json/inventory.json', 'r') as f:
                inv = json.load(f) 
            with open('json/item.json', 'r') as f:
                item = json.load(f) 
            item = item['data']['item']['items']
            e = inv['data'][str(interaction.user.id)]['items']
            text = ''
            count = 0
            if len(e) <= 0:
                text = "You dont have items, buy or craft items"
            for x in e:
                if e[x]['qty'] <= 0:
                    count += 1
                if len(e) <= count:
                    text = "You dont have items, buy or craft items"
                else:
                    if e[x]['qty'] > 0:
                        text += f"{item[x]['icon']} **{x}** : {e[x]['qty']}\n"

            embed.add_field(name=f"You can use this item to craft in `{prefix}recipe`",value=f"\n{text}")
            embed.set_footer(text=f"If you need some money just do `{prefix}sell [item name]`")
            await interaction.response.edit_message(embed=embed)

        @discord.ui.button(label="Consumables",style=discord.ButtonStyle.grey,emoji="🍎")
        async def consumables(self, interaction: discord.Interaction, button: Button):
            embed = discord.Embed(color=discord.Color.random())
            embed.set_author(name=f'{interaction.user.name} All of your consumables!',icon_url=f"{interaction.user.display_avatar}\n")
            with open('json/inventory.json', 'r') as f:
                data = json.load(f) 
            with open('json/item.json', 'r') as f:
                item = json.load(f) 
            item = item['data']['item']['consumables']
            e = data['data'][str(interaction.user.id)]['consumables']
            cChest = 0
            cPotion = 0
            cBoost = 0
            chest = ''
            potion = ''
            boost = ''
            count = 0
            if len(e) <= 0:
                if cPotion <= 0 :
                    potion = "You dont have potion"
                if cChest <= 0 :
                    chest = "You dont have chest"
                if cBoost <= 0 :
                    boost = "You dont have boost"
            for x in e:
                split = x.split(" ")
                if e[x]['qty'] > 0:
                    if "potion" in split:
                        potion += f"{item[x]['icon']} **{x}** : {e[x]['qty']}\n"
                        cPotion += 1
                    elif "chest" in split:
                        chest += f"{item[x]['icon']} **{x}** : {e[x]['qty']}\n"
                        cChest += 1
                    elif "boost" in split:
                        boost += f"{item[x]['icon']} **{x}** : {e[x]['qty']}\n"
                        cBoost += 1
            if cPotion <= 0 :
                potion = "You dont have potion"
            if cChest <= 0 :
                chest = "You dont have chest"
            if cBoost <= 0 :
                boost = "You dont have boost"
            embed.add_field(name="You can eat or use and gain some buff",value="\u200B",inline=False)
            embed.add_field(name=f"CHEST",value=f"\n{chest}")
            embed.add_field(name=f"BOOST",value=f"\n{boost}")
            embed.add_field(name=f"POTION",value=f"\n{potion}")
            embed.set_footer(text=f"If you need some money just do `{prefix}sell [item name]`")
            # await interaction.response.edit_message()
            await interaction.response.edit_message(embed=embed)

        async def interaction_check(self, interaction: discord.Interaction):
            return interaction.user.id == self.author.id

        # @discord.ui.button(emoji="😀", label="Button 1", style=discord.ButtonStyle.primary)
        # async def button_callback(self, interaction: discord.Interaction, button: Button):
        #     for child in self.children: # loop through all the children of the view
        #         child.disabled = True # set the button to disabled
        #     print(self)
        #     await interaction.response.edit_message(view=self)
    @client.command(name="inventory",aliases=['i','inv'])
    @commands.cooldown(3,1,commands.BucketType.user)
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
        embed.add_field(name="Select",value=f"⚔️ Equipments\n🎒 Items\n🍎 Consumables")
        view = Menu(member)
        await ctx.send(embed=embed,view=view)

    @client.command(name="shop",aliases=['shops'])
    @commands.cooldown(3,1,commands.BucketType.user)
    async def shop(ctx):
        member = ctx.author

        id = member.id
        name = member.display_name

        with open('json/users.json', 'r') as f:
            data = json.load(f)
        user = data['users'][str(id)]

        with open('json/shop.json', 'r') as sh:
            shop = json.load(sh)

        with open('json/inventory.json', 'r') as i:
            inv = json.load(i)

        if str(member.id) not in data['users']:
            await ctx.send(f'**{name}** `{prefix}start` to register')
            return

        embed = discord.Embed(color=discord.Color.random())
        embed.set_author(name=f"Shop",icon_url=f"{member.display_avatar}\n")
        embed.add_field(name=f"Buy anything? do `{prefix}buy [name item]`",value="\u200B",inline=False)

        if len(shop['data']) <= 0:
            embed.add_field(name=f"Sorry we dont sell anything yet",value=f":cry:")
        for x in shop['data']:
            if x in inv['data'][str(id)]['equipments']:
                embed.add_field(name=f"~~{shop['data'][x]['icon']} {x} | {shop['data'][x]['price']} :coin:~~",value=f"\n~~{shop['data'][x]['description']}~~")
            else:
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
    @commands.cooldown(3,1,commands.BucketType.user)
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
                if new_arg in inv['data'][str(id)]['equipments']: 
                    await ctx.send(f'**{name}** You already have the equipments')
                    return
                elif int(split[-1] if is_integer(split[-1]) else 1) > 1:
                    await ctx.send(f'**{name}** You can`t stack an equipments!')
                    return
                elif 'sword' in new_arg:
                    inv['data'][str(member.id)]['equipments'][new_arg] = {}
                    inv['data'][str(member.id)]['equipments'][new_arg]['name'] = item['data']['item']['equipments']['sword'][new_arg]['name']
                    inv['data'][str(member.id)]['equipments'][new_arg]['icon'] = item['data']['item']['equipments']['sword'][new_arg]['icon']
                    inv['data'][str(member.id)]['equipments'][new_arg]['attack'] = item['data']['item']['equipments']['sword'][new_arg]['attack']
                elif 'armor' in new_arg:
                    inv['data'][str(member.id)]['equipments'][new_arg] = {}
                    inv['data'][str(member.id)]['equipments'][new_arg]['name'] = item['data']['item']['equipments']['armor'][new_arg]['name']
                    inv['data'][str(member.id)]['equipments'][new_arg]['icon'] = item['data']['item']['equipments']['armor'][new_arg]['icon']
                    inv['data'][str(member.id)]['equipments'][new_arg]['defense'] = item['data']['item']['equipments']['armor'][new_arg]['defense']

                
                
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
                
    @client.command(name="sell")
    @commands.cooldown(3,1,commands.BucketType.user)
    async def sell(ctx,*,arg):
        member = ctx.author

        id = member.id
        name = member.display_name

        mention = f"<@{id}>"

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
        new_arg = str(new_arg).replace(f" {split[-1]}" if split[-1] == "all" else "",'')

        if new_arg in inv['data'][str(id)]['equipments'] or new_arg in inv['data'][str(id)]['items'] or new_arg in inv['data'][str(id)]['consumables']:
            if new_arg in inv['data'][str(id)]['equipments']:
                # if (int(split[-1]) if is_integer(split[-1]) else 1) > 1:
                #     await ctx.send(f'**{name}** You only have 1 item!')
                #     return
                if new_arg == user['equipments']['armor'] or new_arg == user['equipments']['sword']:
                    await ctx.send(f'**{name}** Please unequip yout equipment before selling it!')
                    return
                icon = item['data']['item']['equipments'][split[1]][new_arg]['icon']
                price = item['data']['item']['equipments'][split[1]][new_arg]['sell']
                user['gold'] = user['gold'] + price

                del inv['data'][str(id)]['equipments'][new_arg]
            elif new_arg in inv['data'][str(id)]['items']:
                if split[-1] == 'all':
                    itemHave = inv['data'][str(id)]['items'][new_arg]['qty']
                    split[-1] = itemHave
                elif (int(split[-1]) if is_integer(split[-1]) else 1) > inv['data'][str(id)]['items'][new_arg]['qty']:
                    await ctx.send(f'**{name}** You dont have that much please check your `{prefix}inv!`')
                    return
                icon = f"{f'({int(split[-1])})' if is_integer(split[-1]) else ''} {item['data']['item']['items'][new_arg]['icon']}"
                price = item['data']['item']['items'][new_arg]['sell'] * (int(split[-1]) if is_integer(split[-1]) else 1)
                user['gold'] = user['gold'] + price 

                if inv['data'][str(id)]['items'][new_arg]['qty'] - (int(split[-1]) if is_integer(split[-1]) else 1) <= 0:
                    del inv['data'][str(id)]['items'][new_arg]
                else:
                    inv['data'][str(id)]['items'][new_arg]['qty'] = inv['data'][str(id)]['items'][new_arg]['qty'] - (int(split[-1]) if is_integer(split[-1]) else 1)
            elif new_arg in inv['data'][str(id)]['consumables']:
                if split[-1] == 'all':
                    itemHave = inv['data'][str(id)]['consumables'][new_arg]['qty']
                    split[-1] = itemHave
                elif (int(split[-1]) if is_integer(split[-1]) else 1) > inv['data'][str(id)]['consumables'][new_arg]['qty']:
                    await ctx.send(f'**{name}** You dont have that much please check your `{prefix}inv!`')
                    return
                icon = f"{f'({int(split[-1])})' if is_integer(split[-1]) else ''} {item['data']['item']['consumables'][new_arg]['icon']}"
                price = item['data']['item']['consumables'][new_arg]['sell'] * (int(split[-1]) if is_integer(split[-1]) else 1)
                user['gold'] = user['gold'] + price 

                if inv['data'][str(id)]['consumables'][new_arg]['qty'] - (int(split[-1]) if is_integer(split[-1]) else 1) <= 0:
                    del inv['data'][str(id)]['consumables'][new_arg]
                else:
                    inv['data'][str(id)]['consumables'][new_arg]['qty'] = inv['data'][str(id)]['consumables'][new_arg]['qty'] - (int(split[-1]) if is_integer(split[-1]) else 1)
                
        else:
            await ctx.send(f"**{mention}** We can't find that item check your `{prefix}inv`")
            return
        with open('json/users.json', 'w') as f:
            json.dump(data, f, indent=4)
                    
        with open('json/inventory.json', 'w') as f:
            json.dump(inv, f, indent=4)

        await ctx.send(f"**{name}** You sell **{icon} {new_arg}** and got {price} :coin:")

    @client.command(name='use')
    @commands.cooldown(3,1,commands.BucketType.user)
    async def use(ctx,*,arg):
        member = ctx.author

        id = member.id
        name = member.display_name
        mention = f"<@{id}>"

        with open('json/users.json', 'r') as f:
            data = json.load(f)
        user = data['users'][str(id)]

        with open('json/inventory.json', 'r') as inv:
            inv = json.load(inv)

        with open('json/shop.json', 'r') as sh:
            shop = json.load(sh)

        with open('json/item.json', 'r') as i:
            item = json.load(i)

        with open('json/buff.json', 'r') as i:
            buff = json.load(i)

        if str(member.id) not in data['users']:
            await ctx.send(f'**{name}** `{prefix}start` to register')
            return
        text = ''
        split = arg.split()
        new_arg = str(arg).replace(f" {split[-1]}" if is_integer(split[-1]) else "",'')
        new_arg = str(new_arg).replace(f" {split[-1]}" if split[-1] == "all" else "",'')
        
        if new_arg in item['data']['item']['consumables']:
            if new_arg not in inv['data'][str(member.id)]["consumables"]:
                await ctx.send(f'**{mention}** Hmmm... You don`t have that item')
                return
            if inv['data'][str(member.id)]["consumables"][new_arg]['qty'] <= 0:

                await ctx.send(f'**{mention}** Hmmm... You don`t have that item')
                return

            if item['data']['item']['consumables'][new_arg]['open_type'] == 'multi':
                if split[-1] == 'all':
                    itemHave = inv['data'][str(id)]['consumables'][new_arg]['qty']
                    if item['data']['item']['consumables'][new_arg]['type'] == 'chest':
                        split[-1] = 100 if itemHave > 100 else itemHave
                    else:
                        split[-1] = itemHave
                elif (int(split[-1]) if is_integer(split[-1]) else 1) > inv['data'][str(id)]['consumables'][new_arg]['qty']:
                    await ctx.send(f'**{mention}** Hmmm... You don`t have that many!')
                    return
                elif item['data']['item']['consumables'][new_arg]['type'] == 'chest' and (int(split[-1]) if is_integer(split[-1]) else 1) > 100:
                    await ctx.send(f'**{mention}** 100 is the maximum of using item per time!')
                    return
            elif item['data']['item']['consumables'][new_arg]['open_type'] == 'single':
                if split[-1] == "all" and (int(split[-1]) if is_integer(split[-1]) else 1) > 1:
                    await ctx.send(f'**{mention}** This item can only be use once per time')
                    return
            if inv['data'][str(id)]['consumables'][new_arg]['qty'] <= 0:
                text = f"**{mention}** Oops you dont have that item"
            if item['data']['item']['consumables'][new_arg]['type'] == 'chest':
                totalItem = random.randint(item['data']['item']['consumables'][new_arg]['min_drop'] * (int(split[-1]) if is_integer(split[-1]) else 1),item['data']['item']['consumables'][new_arg]['max_drop'] * (int(split[-1]) if is_integer(split[-1]) else 1))
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

                itemObtained = ''
                for oChest,oValue in zip(resultDropChest.split('-'), resultDropValue.split("-")):
                    if int(oValue) != 0:
                        if oChest in item['data']['item']['consumables']:
                            itemObtained += f"{item['data']['item']['consumables'][oChest]['icon']}{oChest} : +{oValue}\n"
                            typeDrop = "consumables"
                        elif oChest in item['data']['item']['items']:
                            itemObtained += f"{item['data']['item']['items'][oChest]['icon']}{oChest} : +{oValue}\n"
                            typeDrop = "items"
                        qty = int(oValue)
                        if oChest in inv['data'][str(member.id)][typeDrop]:
                            qty = inv['data'][str(member.id)][typeDrop][oChest]['qty'] + int(oValue)
                        inv['data'][str(member.id)][typeDrop][oChest] = {}
                        inv['data'][str(member.id)][typeDrop][oChest]['name'] = str(oChest)
                        inv['data'][str(member.id)][typeDrop][oChest]['qty'] = qty

                        with open('json/inventory.json', 'w') as f:
                            json.dump(inv, f, indent=4)
                
                embed = discord.Embed(color=discord.Color.random())
                embed.set_author(name=f"{name} use chest",icon_url=f"{member.display_avatar}\n")
                embed.add_field(name=f"{item['data']['item']['consumables'][new_arg]['icon']} {new_arg} x{split[-1] if is_integer(split[-1]) else 1}",value=f"{itemObtained}")
                text = embed
            elif item['data']['item']['consumables'][new_arg]['type'] == 'stat enchantment':
                statUp = item['data']['item']['consumables'][new_arg]['stat_up']
                statUpText = ''

                for x in statUp:
                    if x == 'attack':
                        icon = ":crossed_swords:"
                    elif x == 'defense':
                        icon = ":shield:"
                    elif x == 'max_health':
                        icon = ":heart:"
                    else:
                        icon = ''
                    if x == 'level':
                        user[x] = user[x] + statUp[x] * (int(split[-1]) if is_integer(split[-1]) else 1)
                        user['attack'] = user['attack'] + 1 * (int(split[-1]) if is_integer(split[-1]) else 1)
                        user['defense'] = user['defense'] + 1 * (int(split[-1]) if is_integer(split[-1]) else 1)
                        user['max_health'] = user['max_health'] + 5 * (int(split[-1]) if is_integer(split[-1]) else 1)
                    else:
                        user[x] = user[x] + statUp[x] * (int(split[-1]) if is_integer(split[-1]) else 1)
                    statUpText += f"{icon} {x} by {statUp[x] * (int(split[-1]) if is_integer(split[-1]) else 1)}, "

                with open('json/users.json', 'w') as f:
                    json.dump(data, f, indent=4)

                text += f"*{mention}* You use **{item['data']['item']['consumables'][new_arg]['icon']} {new_arg} {(f'({int(split[-1])})' if is_integer(split[-1]) else '')}** and increase your {statUpText}"
            elif item['data']['item']['consumables'][new_arg]['type'] == 'buff':
                buffItem = item['data']['item']['consumables'][new_arg]['buff']
                buffText = ''
                typeBoost = str(new_arg).replace(f"{split[0]} ",'')
                buffTime = date.strptime(buff['data'][str(id)][typeBoost][str(split[0])]['time'], '%Y-%m-%d %H:%M:%S')
                
                seconds = buffItem["boost time"] * (int(split[-1]) if is_integer(split[-1]) else 1)
                days = seconds // 86400
                hours = (seconds % 86400) // 3600
                minutes = (seconds % 3600) // 60
                seconds = seconds % 60
                totalBuff = f"{f'{days}d' if days > 0 else ''}{f'{hours}h' if hours > 0 else ''}{f'{minutes}m' if minutes > 0 else ''}{f'{seconds}s' if seconds > 0 else ''}"

                if datetime.datetime.now() <= buffTime:
                    buff['data'][str(id)][typeBoost][str(split[0])]['time'] = (buffTime + datetime.timedelta(seconds=buffItem["boost time"] * (int(split[-1]) if is_integer(split[-1]) else 1))).strftime('%Y-%m-%d %H:%M:%S') 
                    buffText = f"increase buff time by {totalBuff}"
                elif datetime.datetime.now() >= buffTime:
                    buff['data'][str(id)][typeBoost][str(split[0])]['time'] = (datetime.datetime.now() + datetime.timedelta(seconds=buffItem["boost time"] * (int(split[-1]) if is_integer(split[-1]) else 1))).strftime('%Y-%m-%d %H:%M:%S') 
                    buffText = f"buff lasts for {totalBuff}"

                
                text = f"**{mention}** You use **{item['data']['item']['consumables'][new_arg]['icon']} {new_arg}** {(f'({int(split[-1])})' if is_integer(split[-1]) else '')} {buffText}"
                with open('json/buff.json', 'w') as f:
                    json.dump(buff, f, indent=4)

        else:
            await ctx.send(f"**{mention}** Hmm... We can`t find that item!")
            return
        qty = inv['data'][str(member.id)]["consumables"][new_arg]['qty']
        inv['data'][str(member.id)]["consumables"][new_arg] = {}
        inv['data'][str(member.id)]["consumables"][new_arg]['name'] = str(new_arg)
        inv['data'][str(member.id)]["consumables"][new_arg]['qty'] = qty - (int(split[-1]) if is_integer(split[-1]) else 1)
        if qty - (int(split[-1]) if is_integer(split[-1]) else 1) <= 0:
            del inv['data'][str(member.id)]["consumables"][new_arg]
        with open('json/inventory.json', 'w') as f:
            json.dump(inv, f, indent=4)

        if type(text) == str:
            await ctx.send(text)
        else:
            await ctx.send(embed=text)

    @client.command(name='cooldown',aliases=['cd'])
    @commands.cooldown(3,1,commands.BucketType.user)
    async def cooldown(ctx):
        member = ctx.author

        id = member.id
        name = member.display_name
        pfp = member.display_avatar

        with open('json/users.json', 'r') as f:
          data = json.load(f)
          
        with open('json/cooldown.json', 'r') as f:
          cool = json.load(f)

        if str(member.id) not in data['users']:
            await ctx.send(f'**{name}** `{prefix}start` to register')
            return
        text = ''
        text_adventure = ''
        for x in cool['data'][str(id)]:
            cd = date.strptime(cool['data'][str(id)][x], '%Y-%m-%d %H:%M:%S')
            if cd > datetime.datetime.now():
                text = f":hourglass_flowing_sand: | {x} **{action.cooldown_error('cooldown',cd)}**"
            elif cd < datetime.datetime.now():
                text = f":white_check_mark: | {x} "
            if x == 'hunt':
                text_adventure += f"{text}\n"
        embed = discord.Embed(colour=discord.Colour.random())
        embed.set_author(name=f"{name}",icon_url=f"{pfp}")
        embed.add_field(name=":crossed_swords: ADVENTURING",value=f"{text_adventure}")
        # embed.add_field(name="STATS",value=f"**:crossed_swords: Att** : {user['attack']}\n** :shield: Def** : {user['defense']}\n**:heart: Hp** : {user['health']} / {user['max_health']}",inline=False)

        await ctx.send(embed=embed)

    @client.command(name='boost',aliases=['b','buff'])
    @commands.cooldown(10,1,commands.BucketType.user)
    async def boost(ctx):
        member = ctx.author

        id = member.id
        name = member.display_name
        pfp = member.display_avatar

        with open('json/users.json', 'r') as f:
            data = json.load(f)
          
        with open('json/buff.json', 'r') as f:
            buff = json.load(f)

        with open('json/item.json', 'r') as f:
            item = json.load(f)

        if str(member.id) not in data['users']:
            await ctx.send(f'`{prefix}start` to register')
            return
        text = ''
        count = 0
        for b in buff['data'][str(id)]:
            for x in buff['data'][str(id)][b]:
                sec = datetime.datetime.now() - date.strptime(buff['data'][str(id)][b][x]['time'], '%Y-%m-%d %H:%M:%S')
                seconds = sec.seconds
                days = seconds // 86400
                hours = (seconds % 86400) // 3600
                minutes = (seconds % 3600) // 60
                seconds = seconds % 60
                totalBuff = f"{f'{days}d' if days > 0 else ''}{f'{hours}h' if hours > 0 else ''}{f'{minutes}m' if minutes > 0 else ''}{f'{seconds}s' if seconds > 0 else ''}"

                time = date.strptime(buff['data'][str(id)][b][x]['time'], '%Y-%m-%d %H:%M:%S')
                icon = item['data']['item']['consumables'][f"{x} {b}"]['icon']
                if datetime.datetime.now() <= time:
                    text += f"{icon} **{x} {b}** : {totalBuff}\n"
                    count += 1
        if count <= 0:
            text = "You dont have any booster check your inventory and use some boost"

        embed = discord.Embed(color=discord.Colour.random())
        embed.set_author(name=f"{name}",icon_url=f"{pfp}")
        embed.add_field(name=f"BOOSTER",value=f"{text}")

        await ctx.send(embed=embed)

    class Recipe(View):
        print('hai1')
        def __init__(self, author):
            self.author = author
            super().__init__()

        @discord.ui.button(label="1",style=discord.ButtonStyle.grey,emoji="<:stoneSword:1052226137184538675>")
        async def equipment1(self,interaction: discord.Interaction, button: Button):
            with open('json/item.json', 'r') as i:
                item = json.load(i)
            item = item['data']['item']
            with open('json/recipe.json', 'r') as i:
                recipe = json.load(i)
            embed = discord.Embed(color=discord.Colour.random())
            recipe = recipe['data']['equipments']
            level = [1,3,5,9,15]
            for l in level:
                text = ''
                for x in recipe:
                    itemText = ''
                    itemCount = 0
                    for key,value in recipe[x].items():
                        itemCount += 1
                        if key != 'level':
                            itemText += f"{value} {item['items'][str(key)]['icon']} {'' if itemCount >= len(recipe[x]) else '+'}"
                    if l == recipe[x]['level']:
                        if x in item['equipments']['sword']:
                            text += f"{item['equipments']['sword'][x]['icon']} **{x}** => {itemText}\n"
                        elif x in item['equipments']['armor']:
                            text += f"{item['equipments']['armor'][x]['icon']} **{x}** => {itemText}\n"
                if text == '':
                    text = 'The item doesnt not exists yet!'
                embed.add_field(name=f"Require level {l}",value=f"{text}")
            await interaction.response.edit_message(embed=embed)

        async def interaction_check(self, interaction: discord.Interaction):
            return interaction.user.id == self.author.id

    @client.command(name='recipe',aliases=['recipes'])
    @commands.cooldown(10,1,commands.BucketType.user)
    async def recipe(ctx,*,arg = 1):
        member = ctx.author

        id = member.id
        name = member.display_name

        with open('json/users.json', 'r') as f:
            data = json.load(f)

        if str(member.id) not in data['users']:
            await ctx.send(f'`{prefix}start` to register')
            return
        view = Recipe(member)
        await ctx.send('hai',view=view)
    
    @client.command(name='craft',aliases=['crafts'])
    @commands.cooldown(10,1,commands.BucketType.user)
    async def craft(ctx,*,arg):
        member = ctx.author

        id = member.id
        mention = f"<@{id}>"
        name = member.display_name

        with open('json/users.json', 'r') as f:
            data = json.load(f)

        with open('json/inventory.json', 'r') as f:
            inv = json.load(f)

        with open('json/recipe.json', 'r') as f:
            recipe = json.load(f)

        with open('json/item.json', 'r') as f:
            item = json.load(f)

        if str(member.id) not in data['users']:
            await ctx.send(f'`{prefix}start` to register')
            return

        split = arg.split()
        new_arg = str(arg).replace(f" {split[-1]}" if is_integer(split[-1]) else "",'')
        new_arg = str(new_arg).replace(f" {split[-1]}" if split[-1] == "all" else "",'')

        if new_arg in inv['data'][str(id)]['equipments']:
            await ctx.send(f'{mention} You already have that sword')
            return
        elif new_arg in inv['data'][str(id)]['equipments']:
            await ctx.send(f'{mention} You already have that armor')
            return
        if new_arg in recipe['data']['equipments'] or new_arg in recipe['data']['end'] or new_arg in recipe['data']['special']:
            
            if new_arg in recipe['data']['equipments']:
                recipe = recipe['data']['equipments']
            elif new_arg in recipe['data']['end']:
                recipe = recipe['data']['end']
            elif new_arg in recipe['data']['special']:
                recipe = recipe['data']['special']
            
            if new_arg in item['data']['item']['equipments']['sword']:
                split[-1] = (1 if is_integer(split[-1]) else 1)
            elif new_arg in item['data']['item']['equipments']['armor']:
                split[-1] = (1 if is_integer(split[-1]) else 1)

            if split[-1] == 'all':
                itemHave = inv['data'][str(id)]['consumables'][new_arg]['qty']
                split[-1] = itemHave
                

            needText = ""
            needItem = ""
            needCount = 0
            text = ''
            for key,value in recipe[new_arg].items():
                if key != "level":
                    if new_arg in item['data']['item']['equipments']['sword']:
                        icon = item['data']['item']['equipments']['sword'][new_arg]['icon']
                    elif new_arg in item['data']['item']['equipments']['armor']:
                        icon = item['data']['item']['equipments']['armor'][new_arg]['icon']
                    elif new_arg in item['data']['item']['items']:
                        icon = item['data']['item']['items'][new_arg]['icon']
                    elif new_arg in item['data']['item']['consumables']:
                        icon = item['data']['item']['consumables'][new_arg]['icon']

                    if key in item['data']['item']['equipments']['sword']:
                        if key in inv['data'][str(id)]['equipments']:
                            qty = inv['data'][str(id)]['equipments'][key]['qty']
                        else:
                            qty = 0
                        iconItem = item['data']['item']['equipments']['sword'][key]['icon']
                    elif key in item['data']['item']['equipments']['armor']:
                        if key in inv['data'][str(id)]['equipments']:
                            qty = inv['data'][str(id)]['equipments'][key]['qty']
                        else:
                            qty = 0
                        iconItem = item['data']['item']['equipments']['armor'][key]['icon']
                    elif key in inv['data'][str(id)]['items']:
                        if key in inv['data'][str(id)]['items']:
                            qty = inv['data'][str(id)]['items'][key]['qty']
                        else:
                            qty = 0
                        iconItem = item['data']['item']['items'][key]['icon']
                    elif key in inv['data'][str(id)]['consumables']:
                        if key in inv['data'][str(id)]['consumables']:
                            qty = inv['data'][str(id)]['consumables'][key]['qty']
                        else:
                            qty = 0
                        iconItem = item['data']['item']['consumables'][key]['icon']
                    if int(qty) < int(value * (int(split[-1]) if is_integer(split[-1]) else 1)):

                        needCount += 1
                    else:
                        text = f"You Craft {(int(split[-1]) if is_integer(split[-1]) else 1)} {icon} `{new_arg}` successfully"

                    needText += f"~ {iconItem} **{key}** You need {(int(qty)) if (int(qty)) < int(value * (int(split[-1]) if is_integer(split[-1]) else 1)) else int(value * (int(split[-1]) if is_integer(split[-1]) else 1))}/{value * (int(split[-1]) if is_integer(split[-1]) else 1)}"
                elif key == 'level' and value > int(data['users'][str(id)]['level']):
                    await ctx.send(f"**{mention}** Your Level is to low you can`t craft this item")
                    return
            embed = discord.Embed(color=discord.Color.random())
            if needCount >= 1:
                embed.add_field(name=f"You don't have enough materials",value=f"{needText}")
                await ctx.send(embed=embed)
                return
            else:
                await ctx.send(text)
        else:
            await ctx.send(f"{mention} Hmm... We cant what you looking for \ntry `{prefix}recipe` to find what you looking for")
            return

    client.run(TOKEN)