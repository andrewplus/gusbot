import discord, os, sys, json, urllib
from discord.ext import commands
import constants

# Gets JSON response from API request
def get_json(url):
    response = urllib.request.urlopen(url)
    return json.loads(response.read())

# Returns an URL from the Epic Mickey Wiki given a specified namespace
# Namespace should be an int (see IDs here: https://www.mediawiki.org/wiki/Extension_default_namespaces)
def get_search_result(query, ns):
    if len(query) > 0:
        try:
            url_pagename = urllib.parse.quote(query)
            results = get_json("https://epicmickey.fandom.com/api.php?action=opensearch&namespace="+str(ns)+"&search="+url_pagename)
            chosen_result = results[1][0]
            chosen_link = results[3][0]
            return chosen_link
        except:
            return "No results found."
    else:
        return "Please provide a query."

class Wiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Article search command (main namespace)
    @commands.command(name="article", aliases=["searcharticles", "wikisearch", "articlesearch", "search", "wiki"], description="Returns the first article namespace search result from the Epic Mickey Wiki.")
    async def article(self, ctx, *, query):
        await ctx.send(get_search_result(query, 0))
    
    # Category namespace search
    @commands.command(name="category", aliases=["searchcategories", "categorysearch"], description="Returns the first category namespace search result from the Epic Mickey Wiki.")
    async def category(self, ctx, *, query):
        await ctx.send(get_search_result(query, 14))
    
    # Project namespace search
    @commands.command(name="project", aliases=["searchproject", "projectsearch"], description="Returns the first project namespace search result from the Epic Mickey Wiki.")
    async def project(self, ctx, *, query):
        await ctx.send(get_search_result(query, 4))

def setup(bot):
    bot.add_cog(Wiki(bot))