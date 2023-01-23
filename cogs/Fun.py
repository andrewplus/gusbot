import discord, os, sys
from discord.ext import commands
import constants, log

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
            
    @commands.command(description="Initiates a certified Epic Mickey Moment™.")
    async def epicmickeymoment(self, ctx):
        await ctx.send("https://tenor.com/view/epic-mickey-epic-mickey-moment-disney-animation-pig-animation-gif-22760640")

async def setup(bot):
    await bot.add_cog(Fun(bot))