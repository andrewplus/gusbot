import constants
from discord_webhook import DiscordWebhook

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