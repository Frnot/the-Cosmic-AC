import os
import sys
import asyncio
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata
from model import prefix

# Import modules
import db
import admin_cmd
import cmd_main
import snitch
import blacklist
import server_management
import voting

log = logging.getLogger(__name__)

version = metadata.version('CosmicAC')


#@bot.event
#async def on_ready():
#    log.info(f"Logged on as {bot.user}!\nReady")



def run_bot():
    log.info(f"Running version v{version}")

    
    # Load Database
    log.info("Loading database")
    db.load()

    # Get token from .env file
    load_dotenv()
    BOT_TOKEN = os.getenv("TOKEN")   

    # Create bot
    global bot
    bot = commands.Bot(command_prefix=guild_prefix, intents=discord.Intents.all(), \
                        activity=discord.Activity(name=f"v{version}", type=discord.ActivityType.playing))

    # Load modules
    bot.add_cog(admin_cmd.Cog(bot))
    bot.add_cog(cmd_main.Cog(bot))
    bot.add_cog(snitch.Cog(bot))
    bot.add_cog(blacklist.Cog(bot))
    bot.add_cog(server_management.Cog(bot))
    bot.add_cog(voting.Cog(bot))
    # TODO:: register event for logged on as bot.user

    # Run bot
    bot.run(BOT_TOKEN)

    # Cleanup
    db.close()


async def guild_prefix(bot, message):
    prefix_return = await prefix.get(message.guild.id)
    return commands.when_mentioned_or(prefix_return)(bot, message)
