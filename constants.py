import platform, os

# Environment variables for instance-specific info. Set these up in your OS.
production_token_var = "PRODUCTION_TOKEN" # Bot token
debug_token_var = "DEBUG_TOKEN" # Bot token for debugging
log_webhook_var = "LOG_WEBHOOK" # Webhook URL for logging
invite_var = "INVITE" # Bot invite URL
owner_id_var = "OWNER_ID" # ID of the bot's owner (for owner-only commands)

# Version/update info
version = "2.5.1" # Set manually
last_update = "23/01/2023" # Set manually

# Cross-platform slashes
def platform_slash():
    if platform.system() == "Windows":
        return "\\"
    else:
        return "/"

windows = platform.system() == "Windows"
slash = platform_slash()

# Bot settings
production = False # If True, the production token will be used instead of the debug token. Only set this to True when you are ready to deploy.
prefix = "$"
owner_id = os.getenv(owner_id_var)
invite = os.getenv(invite_var)

# Set token_var depending on the production state
def get_token(prod):
    if prod:
        return production_token_var
    else:
        return debug_token_var

token_var = get_token(production)