import constants
from discord_webhook import DiscordWebhook, DiscordEmbed

# Basic webhook logging functionality

def webhook_message(msg):
    webhook = DiscordWebhook(url=constants.log_webhook, content=msg)
    webhook.execute()

def put(msg, formatting_type="default"):
    affix = ""
    if formatting_type == "bold":
        affix = "**"
    elif formatting_type == "italic":
        affix = "*"
    elif formatting_type == "bolditalic" or formatting_type == "italicbold":
        affix = "***"
    elif formatting_type == "warning":
        affix = ":warning:"
    elif formatting_type == "critical":
        affix = "***:exclamation:"
    elif formatting_type == "code":
        affix = "```"
    elif formatting_type == "system":
        affix = ":desktop:"
    elif formatting_type == "default":
        affix = ""
    
    print(msg)
    webhook_message(affix + msg + affix)

def command(ctx):
    webhook = DiscordWebhook(url=constants.log_webhook)
    embed = DiscordEmbed(title='Your Title', description='Lorem ipsum dolor sit', color='03b2f8')
    embed.add_embed_field(name='Field 1', value='Lorem ipsum', inline=False)
    embed.add_embed_field(name='Field 2', value='dolor sit', inline=False)

    msg = ":keyboard: Command '"+ctx.command.name+"' has been run.\nMessage content:```"+ctx.message.content+"```Author:```"+ctx.message.author.name+"#"+ctx.message.author.discriminator+" ("+str(ctx.message.author.id)+")```"
    webhook.add_embed(embed)
    webhook.execute()