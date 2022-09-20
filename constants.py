import platform, private

def platform_slash():
    if platform.system() == "Windows":
        return "\\"
    else:
        return "/"

def get_token(prod):
    if prod:
        return production_token
    else:
        return debug_token

production = False # If true, production_token will be used instead of debug_token
version = "2.5.0" # Set manually
last_update = "20/09/2022" # Set manually
production_token = private.production_token
debug_token = private.debug_token
token = get_token(production)
log_webhook = private.log_webhook
invite = private.invite

# Cross-platform flashes
windows = platform.system() == "Windows"
slash = platform_slash()

# Bot settings
prefix = "$"
owner_id = private.owner_id