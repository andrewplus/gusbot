import discord, os, json, urllib, random, sys
from discord.ext import commands
from datetime import datetime
sys.path.append(os.getcwd() + '/..') # hacky workaround
from new_em_bot import constants

# Download/update image cache
# Will be saved on disk at `cache_file`
def update_image_cache(category, cache_file):
    with urllib.request.urlopen("https://epicmickey.fandom.com/api.php?action=query&list=categorymembers&cmtitle=Category:"+category+"&cmlimit=500&format=json") as url:
        f = open(cache_file, "w")
        f.write(url.read().decode('UTF-8'))
        f.close()

# Returns a random image from a category on epicmickey.fandom.com using the Fandom API
def random_category_image(category, cache_file, embed_title, embed_color=0x4aa5ff):
    # If a image cache doesn't already exist, build one
    if not os.path.exists(cache_file):
        update_image_cache(category, cache_file)

    # Open the cache file
    with open(cache_file) as fh:
        data = json.load(fh, strict=False)

    # Number of images in cache
    pic_amount = len(data["query"]["categorymembers"])
    # Select random index from image list
    rng = random.randint(0,pic_amount-1)
    # Get image_name by index
    image_name = data["query"]["categorymembers"][rng]["title"]
    # Replace spaces with underscores (mediawiki images do not have spaces)
    image_name = image_name.replace(" ", "_")
    # Url encode image_name
    image_name = urllib.parse.quote(image_name)

    # Use Fandom API to get servable image URL (File:Image.png -> https://vignette.wikia.nocookie.net/...)
    with urllib.request.urlopen("https://epicmickey.fandom.com/api.php?action=imageserving&format=json&wisTitle=" + image_name) as serveapi:
        servejson = json.loads(serveapi.read().decode())

    # Create and return Discord embed
    embed = discord.Embed(color=embed_color)
    embed.add_field(name=embed_title, value="[Image source](https://epicmickey.fandom.com/wiki/" + str(image_name + ")"), inline=False)
    embed.set_image(url=servejson["image"]["imageserving"])
    embed.set_footer(text="Images courtesy of Epic Mickey Wiki contributors")
    return embed

# Returns a fan art embed
# This is different from the generic random_category_image() so artists can be credited
def fanart_embed(artist, image, url, website):
    if website == "Twitter":
        artist_page = "https://twitter.com/" + artist
    elif website == "DeviantArt":
        artist_page = "https://deviantart.com/" + artist
    elif website == "Tumblr":
        artist_page = "https://" + artist + ".tumblr.com"
    
    embed = discord.Embed(color=0x8bd1da)
    embed.add_field(name="Random Fanart", value="Posted by [" + artist + "](" + artist_page + ") on [" + website + "](" + url + ")", inline=False)
    embed.set_image(url=image)
    embed.set_footer(text="If you enjoy the art, please support the artist!")
    return embed

class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Random concept art command
    @commands.command(description="Sends a random piece of concept art from the Epic Mickey Wiki in the current channel.")
    async def conceptart(self, ctx):
        embed = random_category_image("Concept_Art", "cache-concept-art.json", "Random Concept Art")
        await ctx.send(embed=embed)
    
    # Randon beta screenshot command
    @commands.command(description="Sends a random beta screenshot from the Epic Mickey Wiki in the current channel.")
    async def beta(self, ctx):
        embed = random_category_image("Beta_Screenshots", "cache-beta-screenshots.json", "Random Beta Screenshot")
        await ctx.send(embed=embed)
    
    # Update all caches
    @commands.command(hidden=True, description="Updates the image cache database from the wiki.")
    async def updateimagecache(self, ctx):
        if str(ctx.author.id) == str(constants.owner_id):
            # todo: make this loop through a list
            update_image_cache("Concept_Art", "cache-concept-art.json")
            update_image_cache("Beta_Screenshots", "cache-beta-screenshots.json")
            await ctx.send("Image cache updated.")

    # Send last cache update date
    @commands.command(hidden=True, description="Sends the date of the last image cache update.")
    async def lastcacheupdate(self, ctx):
        if str(ctx.author.id) == str(constants.owner_id):
            unixdate = os.path.getmtime("cache-concept-art.json") # since both are updated at once, we check the revision date of only one file
            lastedited = datetime.utcfromtimestamp(unixdate).strftime('%d/%m/%Y')
            await ctx.send(str(lastedited))
    
    # Random fanart command
    @commands.command(description="Sends a random piece of fan art in the current channel.")
    async def fanart(self, ctx):
        with open("fan-art.json") as data:
            fan_art = json.load(data)
            choice = random.choice(fan_art)
            choice_artist = choice["artist"]
            choice_image = choice["image"]
            choice_url = choice["url"]
            choice_website = choice["website"]
            
        embed = fanart_embed(choice_artist, choice_image, choice_url, choice_website)
        await ctx.send(embed=embed)
    
    # Add a piece of fanart to fan-art.json
    # Sources are currently only compatible with Twitter, DeviantArt, and Tumblr 
    # Todo: make this command less annoying to use
    @commands.command(hidden=True, description="Adds a piece of fanart to the database.")
    async def addfanart(self, ctx, artist, image, url, website):
        if str(ctx.author.id) == str(constants.owner_id):
            obj = {"artist":artist,"image":image,"url":url,"website":website}
            if website == "Twitter" or website == "DeviantArt" or website == "Tumblr":
                try:
                    # Add new item to fan-art.json
                    with open("fan-art.json", "r") as data:
                        fan_art = json.load(data)
                        fan_art.append(obj)
                    with open("fan-art.json", "w") as data:
                        json.dump(fan_art, data)

                    # Success! Post result.
                    await ctx.send("The following fanart has been saved:")
                    embed = fanart_embed(artist, image, url, website)
                    await ctx.send(embed=embed)
                except:
                    await ctx.send("Database file could not be saved.")
            else:
                 await ctx.send("Invalid website. The fanart was not added.")
    
    # Send total fanart count
    @commands.command(hidden=True, description="Sends the total count of fanart.")
    async def fanartcount(self, ctx):
        if str(ctx.author.id) == str(constants.owner_id):
            with open("fan-art.json") as data:
                fan_art = json.load(data)
                await ctx.send(str(len(fan_art)))

def setup(bot):
    bot.add_cog(Images(bot))