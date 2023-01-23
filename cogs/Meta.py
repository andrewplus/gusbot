import discord, psutil, constants, log
from discord.ext import commands
from platform import python_version
from datetime import datetime

# Get startup time
now = datetime.now()

class Meta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
            
    # Info command
    @commands.command(description="Information and stats about the bot.")
    async def info(self, ctx):
        embed = discord.Embed(title="Gremlin Gus Bot", description="A bot with several Epic Mickey-specific features and commands. Type $help for the command list.", color=0xe37814)
        embed.set_thumbnail(url="https://i.imgur.com/nc3kDJH.jpg")
        embed.add_field(name="Author", value="RampantLeaf#6119", inline=True)
        embed.add_field(name="Bot version", value=constants.version, inline=True)
        embed.add_field(name="Python version", value=python_version(), inline=True)
        embed.add_field(name="discord.py version", value=str(discord.__version__), inline=True)
        embed.add_field(name="Last update", value=constants.last_update, inline=True)
        embed.add_field(name="Last downtime", value=now.strftime("%d/%m/%Y"), inline=True)
        embed.set_footer(text="CPU: " + str(psutil.cpu_percent()) + "% | Memory: " + str(round(psutil.virtual_memory().used / (1024*1024*1024), 2)) + " / " + str(round(psutil.virtual_memory().total / (1024*1024*1024), 2)) + " GB | Powered by Raspberry Pi")
        await ctx.send(embed=embed)

    # Invite command
    @commands.command(description="Sends a bot invite link in the current channel.")
    async def invite(self, ctx):
        await ctx.send("Here's a link to invite me to your server: <" + constants.invite + ">")
        
async def setup(bot):
    await bot.add_cog(Meta(bot))