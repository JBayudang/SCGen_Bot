# bot.py
import discord
from discord.ext import commands
import json
import os
import asyncio

# --- Configuration ---
def get_config():
    """Loads the configuration file."""
    if not os.path.exists('config.json'):
        # Create a default config file if it doesn't exist
        default_config = {
            "token": "YOUR_DISCORD_BOT_TOKEN",
            "owner_id": "YOUR_DISCORD_USER_ID",
            "gemini_api_key": "YOUR_GEMINI_API_KEY"
        }
        with open('config.json', 'w') as f:
            json.dump(default_config, f, indent=4)
        print("config.json created. Please fill in your bot token, owner ID, and Gemini API Key.")
        exit()

    with open('config.json', 'r') as f:
        return json.load(f)

config = get_config()

# --- Bot Initialization ---
# Using default intents, as slash commands don't require privileged intents for basic operation.
intents = discord.Intents.default()

bot = commands.Bot(command_prefix="/", intents=intents) # Prefix is not used for slash commands, but required.

# --- Bot Events ---
@bot.event
async def on_ready():
    """Event that fires when the bot is ready."""
    print(f'Logged in as {bot.user.name} - {bot.user.id}')
    print('------')
    # Load cogs
    await load_cogs()

    # Sync slash commands with Discord
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


# --- Cog Management ---
async def load_cogs():
    """Loads all cogs from the 'cogs' directory."""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded cog: {filename}')
            except Exception as e:
                print(f'Failed to load cog {filename}: {e}')

# --- Run Bot ---
if __name__ == "__main__":
    if any(val.startswith("YOUR_") for val in config.values()):
        print("Please fill out all the placeholder values in config.json")
    else:
        try:
            bot.run(config["token"])
        except discord.errors.LoginFailure:
            print("Improper token has been passed. Please check your config.json")

