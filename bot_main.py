import os
import sys
import logging
import discord
from discord.ext import commands as dcommands
from dotenv import load_dotenv
if sys.version_info >= (3, 8):
    from importlib import metadata
else:
    import importlib_metadata as metadata
from model import prefix

# Import modules
import db
import commands.admin, commands.general
import events.admin, events.snitch
import server_management
import voting

log = logging.getLogger(__name__)

version = metadata.version('CosmicAC')


#@bot.event
#async def on_ready():
#    log.info(f"Logged on as {bot.user}!\nReady")



def run_bot(bot_token):
    log.info(f"Running version v{version}")

    
    # Load Database
    log.info("Loading database")
    db.load()


    # Create bot
    global bot
    bot = dcommands.Bot(command_prefix=guild_prefix, intents=discord.Intents.all(), \
                        activity=discord.Activity(name=f"v{version}", type=discord.ActivityType.playing))

    # Load modules
    bot.add_cog(commands.admin.Cog(bot))
    bot.add_cog(commands.general.Cog(bot))
    bot.add_cog(server_management.Cog(bot))
    bot.add_cog(voting.Cog(bot))

    bot.add_cog(events.admin.Cog(bot))
    bot.add_cog(events.snitch.Cog(bot))
    # TODO:: register event for logged on as bot.user

    # Run bot
    bot.run(bot_token)

    # Cleanup
    db.close()


async def guild_prefix(bot, message):
    prefix_return = await prefix.get(message.guild.id)
    return dcommands.when_mentioned_or(prefix_return)(bot, message)
