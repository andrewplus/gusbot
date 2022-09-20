import constants, log, discord, os
from discord.ext import commands

class GusBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=constants.prefix, intents=discord.Intents.all())
    
    # Load cogs
    async def setup_hook(self):
        for filename in os.listdir("cogs"):
            if filename[-3:] == ".py":
                cog_name = os.path.splitext(filename)[0]
                try:
                    await self.load_extension("cogs." + cog_name)
                    print(cog_name + " cog loaded.")
                except Exception as e:
                    print(cog_name + " cog not loaded.")
                    print(e)

    # On bot ready
    async def on_ready(self):
        log.put("We have logged in as " + self.user.name, "bold")
        await self.change_presence(activity=discord.Game(name="Type $help for help"))

# Start bot
bot = GusBot()
log.put("The bot has been started. Attempting to connect to Discord.", "system")
bot.run(constants.token)