import random
import mysql.connector
import discord
from discord.ext import commands
import responses

def run_discord_bot():
    TOKEN = 'OTEzNzgzNTMyMTg1MzU0MjYx.GRM0ab.3zhtdddf31WtFUwlcfVakJ5rYVUG9GnJD2pLVk'
    client = commands.Bot(command_prefix=".",intents=discord.Intents.all())


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
        id = str(ctx.author.id)
        username = str(ctx.author)
        sql_where = f"SELECT * FROM user WHERE id_user = {id}"
        if sql_where:
            await ctx.send(f"You Already Registed")
        else:
            sql = "INSERT INTO user (id_user,name,level,xp,attack,defense,health) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (id,username,1,0,5,5,100)
            # val = (2,'erick',0)
            cursor.execute(sql,val)
            mydb.commit()
            await ctx.send(f"You have been registed")

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
            for x in range(100):
                if int(user_up['xp']) - need_xp <= 0:
                    break
                level_up += 1
                need_xp += (int(user_up['level']) + level_up) * 100 * 1.35
            sql_up = f"UPDATE user SET level = {int(user['level']) + level_up},xp = {(((int(user_up['level']) + level_up) * 100 * 1.35) - need_xp) + int(user_up['xp'])} WHERE id_user = {id}"
            # print(f"{((int(user_up['level']) + level_up) * 100 * 1.35) - need_xp} + {int(user_up['xp'])} = {(((int(user_up['level']) + level_up) * 100 * 1.35) - need_xp) + int(user_up['xp'])}")
            cursor.execute(sql_up)
            mydb.commit()
            level_up_text = ""if level_up <= 0 else f"\n**{name}** leveled up {level_up} times"
        await ctx.send(f"**{name}** gain {xp_gain} xp {level_up_text}")

    @client.command(name= "profile",aliases=['p','pr'])
    async def profile(ctx,member:discord.member = None):
        if member == None:
            member = ctx.author

        id = member.id
        name = member.display_name
        pfp = member.display_avatar
        cursor.execute(f"SELECT * FROM user WHERE id_user = {id}")
        user = cursor.fetchone()

        level_persentage = "00.00" if None else f"{((int(user['xp']) / (int(user['xp']) * 100 * 1.35)) * 100):.2f}"
        xp_range = f"{int(user['xp'])} / {int(user['level'] * 100 * 1.35)}"

        embed = discord.Embed(title="Adventure Lover",colour=discord.Colour.random())
        embed.set_author(name=f"{name}")
        embed.set_thumbnail(url=f"{pfp}")
        embed.add_field(name="PROGRESS",value=f"**Level** : {user['level']} ({level_persentage}%)\n**Xp** : {xp_range}")

        await ctx.send(embed=embed)
        

    client.run(TOKEN)