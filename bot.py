import os
import discord
from discord.ext import commands


bot = commands.Bot(command_prefix='/')
bot.description = "DM Bot: Playing RPG Zero"


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game('RPG Zero'))
    print(f'[•] Ready!\n')


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=999):
    await ctx.channel.purge(limit=amount+1)


if __name__ == '__main__':
    bot.load_extension('cogs.dice_cog')
    bot.load_extension('cogs.character_cog')
    bot.load_extension('cogs.game_cog')
    bot.run(os.getenv('TOKEN'))
