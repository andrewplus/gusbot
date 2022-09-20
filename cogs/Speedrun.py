import discord, os, sys, constants
from datetime import datetime
from discord.ext import commands
import srcomapi, srcomapi.datatypes as dt

# init speedrun api
api = srcomapi.SpeedrunCom(); api.debug = 1

game_names = ["", "Epic Mickey", "Epic Mickey 2: The Power of Two"]
em = api.search(srcomapi.datatypes.Game, {"name": "disney epic mickey"})[0]
em2 = api.search(srcomapi.datatypes.Game, {"name": "disney epic mickey 2: the power of two"})[0]

def wr(game_id, index):
    game = em if int(game_id) == 1 else em2
    categories = game.categories
    wr = categories[index].records[0].runs[0]["run"]
    time = datetime.utcfromtimestamp(wr.times["primary_t"]).strftime('%H:%M:%S')
    ingame = datetime.utcfromtimestamp(wr.times["ingame_t"]).strftime('%H:%M:%S')
    date = wr.date
    player = player_name = wr.players[0]
    player_name = player.names["international"]
    player_link = player.weblink
    video = wr.videos["links"][0]["uri"]
    comment = wr.comment
    weblink = wr.weblink

    embed = discord.Embed(title=game_names[game_id]+" "+categories[0].name+" World Record")
    embed.add_field(name="Time", value=time, inline=True)
    embed.add_field(name="IGT", value=ingame if ingame != "00:00:00" else "N/A", inline=True)
    embed.add_field(name="Runner", value="["+player_name+"]("+player_link+")", inline=True)
    embed.add_field(name="Date", value=date, inline=True)
    embed.add_field(name="Speedrun.com", value="[Link]("+weblink+")", inline=True)
    embed.add_field(name="Video", value="[Link]("+video+")", inline=True)
    embed.add_field(name="Comment", value=comment[:1024], inline=False)
    return embed

class Select(discord.ui.Select):
    def __init__(self, categories, game_id):
        self.game_id = game_id
        super().__init__(placeholder="Select a category",max_values=1,min_values=1,options=categories)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content="", embed=wr(int(self.game_id), int(self.values[0])), view=None)

class SelectView(discord.ui.View):
    def __init__(self, categories, game_id):
        self.categories = categories
        self.game_id = game_id
        super().__init__()
        self.add_item(Select(categories, game_id))

class Speedrun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Returns the world record run of a certain category for either Epic Mickey or Epic Mickey 2.")
    async def wr(self, ctx, game_id):
        game = em if int(game_id) == 1 else em2
        categories = game.categories
        categories_list = []

        for i, category in enumerate(categories):
            if category.type == "per-game":
                categories_list.append(discord.SelectOption(label=category.name, value=i))

        await ctx.send("[This command is in development. Some functionality may be broken.]\n\nSelect an " + game_names[int(game_id)] + " speedrun category:", view=SelectView(categories_list, game_id))

async def setup(bot):
    await bot.add_cog(Speedrun(bot))