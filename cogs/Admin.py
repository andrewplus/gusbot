import discord, os, sys
from discord.ext import commands
import constants

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
            
    @commands.command(hidden=True, description="Displays the server count of the bot user.")
    async def guildcount(self, ctx):
        if str(ctx.author.id) == str(constants.owner_id):
            guildcount = len(list(self.bot.guilds))
            await ctx.send(str(guildcount))

async def setup(bot):
    await bot.add_cog(Admin(bot))