import discord
import json
import math
from discord.utils import get
from discord.ext import tasks

f = open('userdata.json', 'r+')
data = json.load(f)

achievements_file = open('achievements.json')
achievements = json.load(achievements_file)
achievements_file.close()

async def set_role(message, role_s):
    member = message.author
    role = get(member.guild.roles, name=role_s)
    await member.add_roles(role)

@tasks.loop(minutes=1)
async def autosave():
    print("Saving...")
    f.seek(0)
    json.dump(data, f, ensure_ascii=False, indent=4)
    f.truncate()

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

        activity = discord.Game(name="Берлога Соскара", type=0)
        await client.change_presence(status=discord.Status.online, activity=activity)

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if str(message.author.id) not in data["users"]:
            data["users"][str(message.author.id)] = {}
            data["users"][str(message.author.id)]["xp"] = 0
            data["users"][str(message.authot.id)]["messages"] = 0
            data["users"][str(message.author.id)]["achievements"] = {}

        if message.content.startswith('-lvl'):
            embed=discord.Embed(url="", color=discord.Color.green())
            lvl = math.floor(math.sqrt(data["users"][str(message.author.id)]["xp"]))
            embed_value = "Твой уровень: **" + str(lvl) + "**"
            embed.add_field(name="Уровень",value=embed_value,inline=False)

            await message.reply(embed=embed, mention_author=True)

        if message.content.startswith('-xp'):
            embed=discord.Embed(url="", color=discord.Color.green())
    
            xp = data["users"][str(message.author.id)]["xp"]

            embed_value = "У тебя **" + str(xp) + ".0** опыта !"
            embed.add_field(name="Опыт",value=embed_value,inline=False)

            await message.reply(embed=embed, mention_author=True)

        if message.content.startswith('-stats'):
            
            lvl_tile = "Статистика для " + message.author.name
            embed=discord.Embed(title=lvl_tile, url="", color=discord.Color.green())
        
            lvl = math.floor(math.sqrt(data["users"][str(message.author.id)]["xp"]))
            xp = data["users"][str(message.author.id)]["xp"]

            xp_until_next_lvl = (lvl+1)**2 - xp

            embed_value = "Твой уровень: **" + str(lvl) + "** и у тебя **" + str(xp) + ".0** опыта !\n" + "Тебе нужно ещё: **"+str(xp_until_next_lvl) + ".0** что бы достичь **" + str(lvl + 1) + "** уровеня !"
            embed.add_field(name="Уровень и опыт",value=embed_value,inline=False)

            ach_value = ""
            for ach in achievements["xp_based"]:
                ach_title =  achievements["xp_based"][ach]["title"]
                if ach_title in data["users"][str(message.author.id)]["achievements"]:
                    ach_value += ach_title+" :white_check_mark:""\n"
                else:
                    xp_needed = achievements["xp_based"][ach]["award"]["xp_required"] - data["users"][str(message.author.id)]["xp"]
                    ach_value += ach_title+", осталось: `"+str(xp_needed)+".0` опыта"+"\n"
   
                
            embed.add_field(name="Ачивки",value=ach_value,inline=False)
            await message.reply(embed=embed, mention_author=True)



        if message.author.id != self.user.id:
            data["users"][str(message.author.id)]["xp"] += 1; 
            data["users"][str(message.author.id)]["messages"] += 1; 

            if data["users"][str(message.author.id)]["xp"] == achievements["xp_based"]["1"]["award"]["xp_required"]:
                await message.reply("Congrats with achievement!", mention_author=True)
                data["users"][str(message.author.id)]["achievements"]["Test achievement"] = True

                await set_role(message, "Test Ach")

                


            
    
client = MyClient()
autosave.start()
client.run('TOKEN')
f.close()