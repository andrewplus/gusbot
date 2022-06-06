import constants, log
import discord, os
from discord.ext import commands
from platform import python_version
from datetime import datetime

# Set working directory to location of bot.py
# Needed for certain python environments
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Set up the bot
bot = commands.Bot(command_prefix=constants.prefix)

# Get startup time
now = datetime.now()

# Cogs
cogs_list = []
def load_cogs():
    log.put("Loading cogs...", "bold")
    for filename in os.listdir("cogs"):
        if filename[-3:] == ".py":
            cog_name = os.path.splitext(filename)[0]
            try:
                bot.load_extension("cogs." + cog_name)
                cogs_list.append(cog_name)
                print(cog_name + " cog loaded.")
            except Exception as e:
                print(cog_name + " cog not loaded.")
                print(e)
            
def unload_cogs():
    log.put("Unloading cogs...", "bold")
    for filename in os.listdir("cogs"):
        if filename[-3:] == ".py":
            cog_name = os.path.splitext(filename)[0]
            try:
                bot.unload_extension("cogs." + cog_name)
                cogs_list.remove(cog_name)
                print(cog_name + " cog loaded.")
            except Exception as e:
                print(cog_name + " cog not loaded.")
                print(e)

@bot.command(hidden=True)
async def reloadcogs(ctx):
    if str(ctx.author.id) == str(constants.owner_id):
        unload_cogs()
        load_cogs()
        await ctx.send("Cogs reloaded.")

# Errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You're missing one or more command arguments. Type ``$help " + ctx.command.name + "`` for help with this command.")

# Info command
@bot.command(description="Information and stats about the bot.")
async def info(ctx):
    embed = discord.Embed(title="Gremlin Gus Bot", description="A bot with several Epic Mickey-specific features and commands. Type $help for the command list.")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/614928078111506459/d24a68ce142f14928b9a9438ac6b5f39.png")
    embed.add_field(name="Author", value="RampantLeaf#6119", inline=True)
    embed.add_field(name="Bot version", value=constants.version, inline=True)
    embed.add_field(name="Python version", value=python_version(), inline=True)
    embed.add_field(name="discord.py version", value=str(discord.__version__), inline=True)
    embed.add_field(name="Last update", value=constants.last_update, inline=True)
    embed.add_field(name="Last downtime", value=now.strftime("%d/%m/%Y"), inline=True)
    await ctx.send(embed=embed)

# Invite command
@bot.command(description="Sends a bot invite link in the current channel.")
async def invite(ctx):
    await ctx.send("Here's a link to invite me to your server: <" + constants.invite + ">")

# On ready event
@bot.event
async def on_ready():
    load_cogs()
    log.put("We have logged in as {0.user}".format(bot), "bold")
    await bot.change_presence(activity=discord.Game(name="Type $help for help"))
    
# Run the bot
log.put("The bot has been started. Attempting to connect to Discord.", "system")
bot.run(constants.token)