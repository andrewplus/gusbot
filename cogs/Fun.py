import discord, os, sys
from discord.ext import commands
sys.path.append(os.getcwd() + '/..') # hacky workaround
from new_em_bot import constants

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
            
    @commands.command(description="Initiates a certified Epic Mickey Moment™.")
    async def epicmickeymoment(self, ctx):
        await ctx.send("https://tenor.com/view/epic-mickey-epic-mickey-moment-disney-animation-pig-animation-gif-22760640")

def setup(bot):
    bot.add_cog(Fun(bot))